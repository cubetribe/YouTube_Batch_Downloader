"use strict";

const $ = (id) => document.getElementById(id);

const els = {
  version: $("version"),
  pasteBtn: $("paste-btn"),
  urlInput: $("url-input"),
  analyzeBtn: $("analyze-btn"),
  hint: $("hint"),
  errorBanner: $("error-banner"),
  videoCard: $("video-card"),
  thumb: $("thumb"),
  badgeDuration: $("badge-duration"),
  badgeQuality: $("badge-quality"),
  videoTitle: $("video-title"),
  videoUploader: $("video-uploader"),
  controls: $("controls"),
  formatSelect: $("format-select"),
  folderInput: $("folder-input"),
  chooseFolderBtn: $("choose-folder-btn"),
  folderPresets: $("folder-presets"),
  downloadBtn: $("download-btn"),
  progressCard: $("progress-card"),
  progressStatus: $("progress-status"),
  progressPercent: $("progress-percent"),
  progressFill: $("progress-fill"),
  progressStats: $("progress-stats"),
  result: $("result"),
  resultText: $("result-text"),
  revealBtn: $("reveal-btn"),
};

const state = {
  meta: null,
  currentUrl: null,
  lastOutputDir: null,
  eventSource: null,
  analyzing: false,
};

// ---------- helpers ----------
function showError(message) {
  els.errorBanner.textContent = message;
  els.errorBanner.classList.remove("hidden");
}
function clearError() {
  els.errorBanner.classList.add("hidden");
  els.errorBanner.textContent = "";
}
function fmtBytes(n) {
  if (!n && n !== 0) return "";
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
  return `${n.toFixed(i ? 1 : 0)} ${units[i]}`;
}
function fmtEta(sec) {
  if (sec == null) return "";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return m ? `${m}m ${s}s` : `${s}s`;
}

async function api(path, body) {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Fehler (${res.status})`);
  return data;
}

// ---------- init ----------
async function init() {
  try {
    const meta = await (await fetch("/api/meta")).json();
    state.meta = meta;
    els.version.textContent = "v" + meta.version;

    meta.formats.forEach((f) => {
      const opt = document.createElement("option");
      opt.value = f.id;
      opt.textContent = f.label;
      els.formatSelect.appendChild(opt);
    });

    els.folderInput.value = meta.default_dir;
    buildPresets(meta.home || meta.default_dir.replace(/\/Downloads\/?$/, ""));

    if (!meta.is_mac) {
      els.chooseFolderBtn.style.display = "none";
    }
  } catch (e) {
    showError("Konnte App-Daten nicht laden: " + e.message);
  }
}

function buildPresets(home) {
  // Build ~/Downloads, ~/Desktop, ~/Movies from the server-provided home dir.
  const presets = [
    ["Downloads", `${home}/Downloads`],
    ["Desktop", `${home}/Desktop`],
    ["Movies", `${home}/Movies`],
  ];
  els.folderPresets.innerHTML = "";
  presets.forEach(([label, path]) => {
    const chip = document.createElement("button");
    chip.className = "preset-chip";
    chip.textContent = label;
    chip.onclick = () => { els.folderInput.value = path; };
    els.folderPresets.appendChild(chip);
  });
}

// ---------- paste ----------
async function pasteFromClipboard() {
  els.pasteBtn.classList.add("flash");
  setTimeout(() => els.pasteBtn.classList.remove("flash"), 400);
  try {
    const text = await navigator.clipboard.readText();
    if (text && text.trim()) {
      els.urlInput.value = text.trim();
      analyze();
      return;
    }
  } catch (e) {
    // Clipboard blocked (permission denied / unsupported) — tell the user.
    showError("Zwischenablage blockiert — bitte mit Cmd+V ins Feld einfügen.");
  }
  els.urlInput.focus();
}

// ---------- analyze ----------
async function analyze() {
  if (state.analyzing) return;  // single-flight: ignore overlapping triggers
  const url = els.urlInput.value.trim();
  clearError();
  if (!url) { showError("Bitte zuerst einen Link einfügen."); return; }

  state.analyzing = true;
  els.analyzeBtn.disabled = true;
  els.analyzeBtn.textContent = "Lädt…";
  els.videoCard.classList.add("hidden");
  els.controls.classList.add("hidden");
  els.progressCard.classList.add("hidden");

  try {
    const info = await api("/api/info", { url });
    state.currentUrl = info.webpage_url || url;
    renderInfo(info);
  } catch (e) {
    showError(e.message);
  } finally {
    state.analyzing = false;
    els.analyzeBtn.disabled = false;
    els.analyzeBtn.textContent = "Analysieren";
  }
}

function renderInfo(info) {
  els.videoTitle.textContent = info.title;
  els.videoUploader.textContent = info.uploader || "";
  if (info.thumbnail) {
    els.thumb.src = info.thumbnail;
    els.thumb.alt = info.title;
  } else {
    els.thumb.removeAttribute("src");
  }
  els.badgeDuration.textContent = info.duration_string || "";
  els.badgeDuration.classList.toggle("hidden", !info.duration_string);

  if (info.is_live) {
    els.badgeQuality.textContent = "LIVE";
  } else if (info.max_height) {
    els.badgeQuality.textContent = info.max_height >= 2160 ? "4K"
      : info.max_height >= 1080 ? "1080p"
      : info.max_height + "p";
  } else {
    els.badgeQuality.textContent = "";
  }
  els.badgeQuality.classList.toggle("hidden", !els.badgeQuality.textContent);

  els.videoCard.classList.remove("hidden");
  els.controls.classList.remove("hidden");
  els.hint.classList.add("hidden");

  // Live streams: yt-dlp would download open-endedly from the live edge, which
  // looks like a hang. Block it with a clear message for now.
  if (info.is_live) {
    els.downloadBtn.disabled = true;
    showError("Das ist ein Live-Stream — Download wird (noch) nicht unterstützt.");
  } else {
    els.downloadBtn.disabled = false;
  }
}

// ---------- folder ----------
async function chooseFolder() {
  try {
    const data = await api("/api/choose-folder", { current: els.folderInput.value });
    if (data.path) els.folderInput.value = data.path;
  } catch (e) {
    showError(e.message);
  }
}

// ---------- download ----------
async function startDownload() {
  if (!state.currentUrl) return;
  clearError();
  const outputDir = els.folderInput.value.trim() || state.meta.default_dir;

  els.downloadBtn.disabled = true;
  els.downloadBtn.querySelector(".dl-label").textContent = "Läuft…";
  els.progressCard.classList.remove("hidden");
  els.result.classList.add("hidden");
  setStatus("Starte Download…", null);
  setIndeterminate(true);

  try {
    const { job_id } = await api("/api/download", {
      url: state.currentUrl,
      format: els.formatSelect.value,
      output_dir: outputDir,
    });
    listenProgress(job_id);
  } catch (e) {
    showError(e.message);
    resetDownloadBtn();
  }
}

function listenProgress(jobId) {
  if (state.eventSource) state.eventSource.close();
  const es = new EventSource(`/api/progress/${jobId}`);
  state.eventSource = es;
  let terminalSeen = false;  // did we get a 'done'/'error' before the stream closed?

  es.onmessage = (ev) => {
    let data;
    try { data = JSON.parse(ev.data); } catch { return; }

    if (data.type === "ping") return;

    if (data.type === "progress") {
      handleProgress(data);
    } else if (data.type === "done") {
      terminalSeen = true;
      es.close();
      onDone(data);
    } else if (data.type === "error") {
      terminalSeen = true;
      es.close();
      showError(data.message || "Download fehlgeschlagen.");
      setStatus("Fehlgeschlagen", null);
      setIndeterminate(false);
      els.progressFill.style.width = "0%";
      resetDownloadBtn();
    }
  };

  es.onerror = () => {
    es.close();
    // If the connection dropped BEFORE any terminal event (server restart,
    // sleep, socket drop), the UI would otherwise be stuck on "Läuft…" with no
    // feedback. Surface it and let the user retry.
    if (!terminalSeen) {
      showError("Verbindung zum Download verloren. Bitte erneut versuchen.");
      setStatus("Abgebrochen", null);
      setIndeterminate(false);
      els.progressFill.style.width = "0%";
      resetDownloadBtn();
    }
  };
}

function handleProgress(d) {
  if (d.status === "downloading") {
    if (d.percent != null) {
      setIndeterminate(false);
      els.progressFill.style.width = d.percent.toFixed(1) + "%";
      els.progressPercent.textContent = d.percent.toFixed(0) + "%";
    }
    els.progressStatus.textContent = "Lädt herunter…";
    const parts = [];
    if (d.total) parts.push(`${fmtBytes(d.downloaded)} / ${fmtBytes(d.total)}`);
    if (d.speed) parts.push(`${fmtBytes(d.speed)}/s`);
    if (d.eta != null) parts.push(`ETA ${fmtEta(d.eta)}`);
    els.progressStats.textContent = parts.join("   ");
  } else if (d.status === "processing") {
    setStatus(d.message || "Verarbeite…", null);
    setIndeterminate(true);
  } else if (d.status === "retry") {
    els.progressStats.textContent = d.message || "";
  }
}

function onDone(data) {
  setIndeterminate(false);
  els.progressFill.style.width = "100%";
  els.progressPercent.textContent = "100%";
  setStatus("Fertig ✓", null);
  state.lastOutputDir = data.filepath || data.output_dir;
  const name = data.title ? `„${data.title}"` : "Datei";
  els.resultText.textContent = `${name} gespeichert.`;
  els.progressStats.textContent = data.output_dir || "";
  els.result.classList.remove("hidden");
  resetDownloadBtn();
}

async function revealResult() {
  if (!state.lastOutputDir) return;
  try { await api("/api/reveal", { path: state.lastOutputDir }); } catch (e) {}
}

// ---------- small UI utils ----------
function setStatus(text, percent) {
  els.progressStatus.textContent = text;
  els.progressPercent.textContent = percent == null ? "" : percent + "%";
}
function setIndeterminate(on) {
  els.progressFill.classList.toggle("indeterminate", on);
  if (on) els.progressPercent.textContent = "";
}
function resetDownloadBtn() {
  els.downloadBtn.disabled = false;
  els.downloadBtn.querySelector(".dl-label").textContent = "Download starten";
}

// ---------- events ----------
els.pasteBtn.addEventListener("click", pasteFromClipboard);
els.analyzeBtn.addEventListener("click", analyze);
els.urlInput.addEventListener("keydown", (e) => { if (e.key === "Enter") analyze(); });
els.chooseFolderBtn.addEventListener("click", chooseFolder);
els.downloadBtn.addEventListener("click", startDownload);
els.revealBtn.addEventListener("click", revealResult);

init();
