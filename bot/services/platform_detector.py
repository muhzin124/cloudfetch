from urllib.parse import urlparse


def detect_platform(url: str):
    """
    Identifies which platform a URL belongs to, purely for
    display purposes (the message shown to the user).

    Download behavior is NOT limited to this list — yt-dlp
    itself supports hundreds of sites. This function just
    decides whether we recognize + label the platform, and
    whether to reject obviously unsupported links early.
    """

    domain = urlparse(url).netloc.lower()

    if "youtube.com" in domain or "youtu.be" in domain:
        return "YouTube"

    if "instagram.com" in domain:
        return "Instagram"

    if "facebook.com" in domain or "fb.watch" in domain:
        return "Facebook"

    if "tiktok.com" in domain:
        return "TikTok"

    if "twitter.com" in domain or "x.com" in domain:
        return "X"

    if "reddit.com" in domain or "redd.it" in domain:
        return "Reddit"

    if "vimeo.com" in domain:
        return "Vimeo"

    if "dailymotion.com" in domain or "dai.ly" in domain:
        return "Dailymotion"

    if "twitch.tv" in domain:
        return "Twitch"

    if "snapchat.com" in domain:
        return "Snapchat"

    if "pinterest.com" in domain or "pin.it" in domain:
        return "Pinterest"

    if "threads.net" in domain:
        return "Threads"

    if "linkedin.com" in domain:
        return "LinkedIn"

    if "soundcloud.com" in domain:
        return "SoundCloud"

    # Unknown domain — we don't recognize it, but let yt-dlp try
    # anyway rather than blocking it outright. If yt-dlp doesn't
    # support it either, the download step will fail with a
    # clear error message instead of a silent rejection here.
    return "Other"
