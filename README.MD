# CloudFetch ☁️

A Telegram bot that downloads videos from YouTube, Facebook, Instagram, TikTok, X, Reddit, and most other video sites — then sends them straight back to you in chat.

## Why I built this

My dad kept sending me video links — mostly from Facebook — asking me to download them so he could set them as his WhatsApp status. Every single time, I'd have to copy the link, open a browser, find a downloader site, and send the file back. And every time, he'd forget how to do it himself, so I'd end up doing it again next week.

He's not technical, and no amount of explaining "just paste it here and click this" was going to stick. What *would* stick was something as simple as sending a message — which he already knew how to do.

So I built a Telegram bot. Now he just sends the link to the bot, taps one button, and gets the video back. No browser, no downloader websites, nothing new to learn.

That's the whole point of this project — not to build the most feature-packed downloader out there, but to solve one specific, real problem for one specific person, and in doing so, actually learn how to build and deploy something properly: Docker, a real cloud server, CI basics, and the operational stuff that comes with keeping something running for someone who depends on it.

## What it does

- Send it a video link from YouTube, Facebook, Instagram, TikTok, X (Twitter), Reddit, Vimeo, Dailymotion, or most other sites
- It fetches the title and duration so you know it grabbed the right thing
- Tap **Download Video** or **Audio Only**
- Get the file sent right back in the chat, ready to save

Only works for whitelisted Telegram accounts — it's not a public bot, it's built for my family.

## Tech stack

- **Python** — [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the bot itself
- **yt-dlp** — does the actual heavy lifting of extracting and downloading video/audio
- **FFmpeg** — merges separate video/audio streams and converts audio-only downloads to mp3
- **Docker** — the whole app is containerized, so it runs the same on my laptop as it does on the server
- **AWS Lightsail** — where it actually lives, running 24/7

## How it's built

```
Telegram message
      ↓
main.py (registers handlers, starts polling)
      ↓
bot/handlers/message.py   → validates the link, detects the platform, fetches video info
bot/handlers/callback.py  → handles the Download/Audio/Cancel button taps
bot/services/downloader.py → wraps yt-dlp, handles format selection + file cleanup
bot/services/platform_detector.py → labels which platform a link is from
```

Every user (including button taps) gets checked against an allowlist of Telegram user IDs before anything runs — this matters because Telegram bots are publicly discoverable by username, and this one runs on a small, cost-limited cloud server. No point letting a stranger rack up my AWS bill.

## Running it locally

```bash
git clone https://github.com/muhzin124/CloudFetch.git
cd CloudFetch
cp .env.example .env
```

Fill in `.env` with your own Telegram bot token (from [@BotFather](https://t.me/BotFather)) and your Telegram user ID (from [@userinfobot](https://t.me/userinfobot)):

```
BOT_TOKEN=your_token_here
ALLOWED_USER_IDS=your_id_here,another_id_here
```

Then run it with Docker:

```bash
docker compose up --build
```

That's it — no separate Python install, no manually installing ffmpeg. Docker handles all of it.

## Deployment

This runs on an **AWS Lightsail** instance (Ubuntu 22.04, the $5/month plan) in the Mumbai region. I went with Lightsail over raw EC2 because it bundles compute, storage, and a generous data transfer allowance into one flat price — for a lightweight bot like this, EC2 + EBS + separate data transfer billing would have cost roughly 2–3x more for no real benefit.

Deployment is just:

```bash
rsync -avz --exclude='.venv' --exclude='__pycache__' -e "ssh -i your-key.pem" ./CloudFetch/ ubuntu@your-server-ip:/home/ubuntu/CloudFetch/
ssh -i your-key.pem ubuntu@your-server-ip
cd CloudFetch
docker compose up --build -d
```

One real lesson from getting this running: the $5 Lightsail plan only has 512MB of RAM, and the Docker build (installing ffmpeg + Python packages) briefly needs more than that — the build was getting killed by Linux's OOM killer partway through. Fixed it with a 1GB swap file, which gave the build enough breathing room without needing to pay for a bigger instance. Small, cheap fix, but a good reminder that "it works on my machine" doesn't always mean "it'll build on a tiny server."

## What I'd still like to add

- GitHub Actions for automatic deployment on push, instead of manually rsync-ing
- Basic logging/monitoring so I know if the bot goes down without having to check manually
- A short setup guide for anyone else who wants to run this for their own family

## License

See [LICENSE](./LICENSE).
