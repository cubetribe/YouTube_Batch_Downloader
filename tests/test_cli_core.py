from unittest.mock import Mock, call

import pytest

from start import extract_youtube_urls
from src import downloader, downloader_enhanced


def test_extract_youtube_urls_normalizes_duplicate_watch_urls_and_preserves_forms():
    text = """
    https://youtube.com/watch?v=abc123XYZ&feature=share
    https://www.youtube.com/watch?v=abc123XYZ&t=42
    https://youtu.be/shortId-1?si=token
    https://www.youtube.com/embed/embedId_2
    https://youtube.com/v/legacyId-3
    """

    assert extract_youtube_urls(text) == [
        "https://www.youtube.com/watch?v=abc123XYZ",
        "https://youtu.be/shortId-1?si=token",
        "https://www.youtube.com/embed/embedId_2",
        "https://youtube.com/v/legacyId-3",
    ]


@pytest.mark.parametrize(
    ("mode", "active_name", "inactive_name"),
    [
        ("video", "download_video", "download_audio"),
        ("audio", "download_audio", "download_video"),
    ],
)
def test_batch_download_accounts_successes_failures_and_dispatches_offline(
    monkeypatch,
    tmp_path,
    mode,
    active_name,
    inactive_name,
):
    urls = [
        "https://youtu.be/success",
        "https://youtu.be/false-failure",
        "https://youtu.be/exception-failure",
    ]
    active_download = Mock(side_effect=[True, False, RuntimeError("offline failure")])
    inactive_download = Mock()
    monkeypatch.setattr(downloader, active_name, active_download)
    monkeypatch.setattr(downloader, inactive_name, inactive_download)

    result = downloader.batch_download(urls, mode=mode, output_dir=str(tmp_path))

    assert result == {
        "total": 3,
        "successful": 1,
        "failed": 2,
        "failed_urls": [
            "https://youtu.be/false-failure",
            "https://youtu.be/exception-failure",
        ],
    }
    assert active_download.call_args_list == [
        call(urls[0], str(tmp_path)),
        call(urls[1], str(tmp_path)),
        call(urls[2], str(tmp_path)),
    ]
    inactive_download.assert_not_called()


def test_enhanced_attempt_download_tries_without_cookies_then_chrome(monkeypatch, tmp_path):
    calls = []

    class FakeYoutubeDL:
        def __init__(self, opts):
            self.opts = opts
            calls.append(opts)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def extract_info(self, url, download):
            assert url == "https://www.youtube.com/watch?v=abc123XYZ"
            assert download is True
            if len(calls) == 1:
                raise downloader_enhanced.yt_dlp.utils.DownloadError("format unavailable")
            return {"id": "abc123XYZ"}

    monkeypatch.setattr(downloader_enhanced.yt_dlp, "YoutubeDL", FakeYoutubeDL)

    instance = object.__new__(downloader_enhanced.EnhancedDownloader)
    instance.output_dir = str(tmp_path)
    instance.logger = Mock()

    result = instance._attempt_download(
        "https://www.youtube.com/watch?v=abc123XYZ",
        "bestvideo+bestaudio",
        "Test Quality",
    )

    assert result is True
    assert len(calls) == 2
    assert "cookiesfrombrowser" not in calls[0]
    assert calls[1]["cookiesfrombrowser"] == ("chrome", None)
