"""In-memory job manager bridging download threads to SSE streams.

A download runs in a background thread; its progress events are pushed onto a
thread-safe queue. The SSE endpoint drains that queue and forwards each event
to the browser. Jobs are ephemeral — fine for a single-user local app.
"""

from __future__ import annotations

import queue
import threading
import time
import uuid
from typing import Iterator, Optional

# Sentinel marking the end of a job's event stream.
_DONE = object()

# Drop finished jobs from memory after this many seconds.
_JOB_TTL = 600


class Job:
    def __init__(self, job_id: str) -> None:
        self.id = job_id
        self.events: "queue.Queue" = queue.Queue()
        self.finished_at: Optional[float] = None


class JobManager:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(self) -> Job:
        job = Job(uuid.uuid4().hex)
        with self._lock:
            self._reap()
            self._jobs[job.id] = job
        return job

    def get(self, job_id: str) -> Optional[Job]:
        with self._lock:
            return self._jobs.get(job_id)

    def publish(self, job_id: str, event: dict) -> None:
        job = self.get(job_id)
        if job:
            job.events.put(event)

    def finish(self, job_id: str, event: dict) -> None:
        job = self.get(job_id)
        if job:
            job.events.put(event)
            job.events.put(_DONE)
            job.finished_at = time.monotonic()

    def stream(self, job_id: str) -> Iterator[dict]:
        """Yield events for ``job_id`` until the terminal event is seen.

        Emits periodic ``{"type": "ping"}`` heartbeats so the browser's
        EventSource connection (and any proxy) stays alive during long stalls.
        """
        if self.get(job_id) is None:
            return
        while True:
            job = self.get(job_id)
            if job is None:  # reaped — nothing more will ever arrive
                return
            try:
                event = job.events.get(timeout=15)
            except queue.Empty:
                # Hard terminal condition independent of the _DONE sentinel: if
                # the job already finished and its queue is drained, stop. This
                # prevents a second/duplicate consumer (which missed the single
                # _DONE) from pinging forever.
                if job.finished_at is not None and job.events.empty():
                    return
                yield {"type": "ping"}
                continue
            if event is _DONE:
                return
            yield event

    def _reap(self) -> None:
        now = time.monotonic()
        stale = [
            jid
            for jid, job in self._jobs.items()
            if job.finished_at and (now - job.finished_at) > _JOB_TTL
        ]
        for jid in stale:
            self._jobs.pop(jid, None)


# Module-level singleton used by the Flask app.
manager = JobManager()
