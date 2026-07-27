import os
import time
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# -----------------------------
# Optional cookies file
# -----------------------------
# Some sites (notably YouTube) sometimes block requests from
# cloud/datacenter IPs unless they look like they're coming
# from a signed-in browser. If a cookies.txt file is present
# (exported from a logged-in browser session), we use it.
# This file is gitignored and never required — if it's not
# present, downloads just proceed without it as before.
COOKIES_FILE = "cookies.txt"


def _cookies_opt():
    if os.path.exists(COOKIES_FILE):
        return {"cookiefile": COOKIES_FILE}
    return {}


# -----------------------------
# YouTube JS-challenge solving
# -----------------------------
# YouTube scrambles some of its video URLs behind a signature
# scheme that requires actually running a bit of JavaScript to
# decode. Without this, yt-dlp can silently fall back to only
# offering thumbnail/storyboard "formats" and nothing playable
# (this is what caused "Requested format is not available").
#
# js_runtimes tells yt-dlp to use Deno (installed in the Docker
# image) to execute that JS.
# remote_components allows yt-dlp to fetch the small challenge
# solver script it needs from yt-dlp's own GitHub releases.
# These are the Python-API equivalents of the CLI flags
# `--js-runtimes deno` and `--remote-components ejs:github`.
_JS_CHALLENGE_OPTS = {
    "js_runtimes": {"deno": {}},
    "remote_components": {"ejs:github"},
}


def get_video_info(url: str):
    """
    Fetch metadata without downloading.
    """

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        **_cookies_opt(),
        **_JS_CHALLENGE_OPTS,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def download_video(url: str, quality: str = "best"):
    """
    Download video according to selected quality.

    Supported qualities:
    - 360
    - 720
    - 1080
    - audio
    - best
    """

    # -----------------------------
    # Select format
    # -----------------------------
    if quality == "360":
        video_format = (
            "bestvideo[vcodec^=avc1][height<=360]"
            "+bestaudio[ext=m4a]/best[height<=360]"
        )

    elif quality == "720":
        video_format = (
            "bestvideo[vcodec^=avc1][height<=720]"
            "+bestaudio[ext=m4a]/best[height<=720]"
        )

    elif quality == "1080":
        video_format = (
            "bestvideo[vcodec^=avc1][height<=1080]"
            "+bestaudio[ext=m4a]/best[height<=1080]"
        )

    elif quality == "audio":
        video_format = "bestaudio"

    else:
        video_format = (
            "bestvideo[vcodec^=avc1]"
            "+bestaudio[ext=m4a]/best"
        )

    # -----------------------------
    # Sanitized output filename
    # -----------------------------
    # Avoid emoji / special characters / super long titles from
    # breaking things on Linux servers or inside Docker.
    # Each download gets a unique timestamp-based name.
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_basename = f"video_{timestamp}"

    # -----------------------------
    # yt-dlp options
    # -----------------------------
    # For audio-only requests, we don't want an mp4 container —
    # there's no video stream to merge into one. Instead we use
    # yt-dlp's FFmpegExtractAudio postprocessor to convert
    # whatever audio stream we got into a standard mp3 file,
    # which plays everywhere (WhatsApp, any phone, any player).
    ydl_opts = {
        "format": video_format,

        "outtmpl": os.path.join(
            DOWNLOAD_DIR,
            f"{output_basename}.%(ext)s"
        ),

        "noplaylist": True,

        "quiet": False,

        **_cookies_opt(),
        **_JS_CHALLENGE_OPTS,
    }

    if quality == "audio":
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ]
    else:
        ydl_opts["merge_output_format"] = "mp4"

    # -----------------------------
    # Download
    # -----------------------------
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    # -----------------------------
    # Find the actual downloaded file
    # -----------------------------
    # prepare_filename() is unreliable after yt-dlp merges
    # separate video+audio streams (it may point to a .webm
    # or intermediate file that no longer exists). Since we
    # control the exact output basename above, we just look
    # for whichever file actually landed on disk with it.
    for filename in os.listdir(DOWNLOAD_DIR):
        if filename.startswith(output_basename):
            return os.path.join(DOWNLOAD_DIR, filename)

    raise FileNotFoundError(
        "Download finished but the output file could not be found."
    )