# CloudFetch ☁️

CloudFetch is a private Telegram bot I built to automate a repetitive task for my family while learning Docker, Linux, and AWS deployment.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![AWS Lightsail](https://img.shields.io/badge/AWS-Lightsail-orange)
![License](https://img.shields.io/badge/License-MIT-green)

It downloads videos from YouTube, Facebook, Instagram, TikTok, X, Reddit, Vimeo, Dailymotion, and hundreds of other sites supported by `yt-dlp` — then sends them straight back in the same Telegram chat.

---

## Features

- Download videos from YouTube, Facebook, Instagram, TikTok, X (Twitter), Reddit, Vimeo, Dailymotion, and hundreds of other sites supported by **yt-dlp**
- Shows video title and duration before downloading
- Choose to download video or audio only
- Automatic cleanup of temporary files after each download
- Dockerized for consistent, repeatable deployment
- Runs 24/7 on AWS Lightsail
- Private bot with a Telegram user allowlist — not open to the public

---

## Why I Built This

My dad kept sending me video links — mostly Facebook videos — and asking me to download them so he could use them as his WhatsApp status.

Every time, I'd copy the link, open a downloader website, download the video, and send it back to him. A few days later, we'd end up doing the exact same thing again.

I realized I was repeating the same manual task over and over. Instead of downloading videos by hand every time, I built **CloudFetch**.

Now he simply sends a video link to the Telegram bot, taps **Download**, and gets the video back in the same chat.

No browser. No downloader websites. No extra steps.

The project started as a small solution for my family, but it also became an opportunity to learn how to build and operate a real application — from development all the way to deployment on the cloud.

---

## About This Project

I'm interested in Cloud Engineering and DevOps, and I built this project as a way to learn by solving a real problem while gaining hands-on experience with deploying and operating software.

I have a basic understanding of Python, so I used AI as a development assistant to help me write, refactor, and understand parts of the codebase. I was responsible for designing the project, deciding the architecture, testing features, debugging issues, deploying the application, and making the technical decisions throughout.

For me, the real learning wasn't just writing Python code — it was understanding how all the pieces fit together: Docker, Linux, AWS, networking, deployment, configuration, troubleshooting, and running an application that someone actually depends on.

My goal with CloudFetch wasn't to become an expert Python developer overnight. It was to build a complete application from idea to production while developing the practical cloud and infrastructure skills I'm pursuing as a future Cloud/DevOps Engineer.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Main application |
| python-telegram-bot | Telegram Bot API |
| yt-dlp | Video extraction & downloading |
| FFmpeg | Merging video/audio streams and audio conversion |
| Docker | Containerization |
| AWS Lightsail | Hosting |
| Ubuntu | Operating system |

---

## Architecture

```
Telegram
     │
     ▼
main.py
     │
     ▼
Message Handler
     │
     ▼
Platform Detector
     │
     ▼
Video Metadata
     │
     ▼
Download Service (yt-dlp)
     │
     ▼
FFmpeg
     │
     ▼
Temporary File
     │
     ▼
Telegram Upload
     │
     ▼
Cleanup
```

---

## Project Structure

```
CloudFetch/

bot/
├── handlers/
│   ├── start.py
│   ├── message.py
│   └── callback.py
│
├── services/
│   ├── downloader.py
│   └── platform_detector.py
│
├── keyboards/
│   └── quality.py
│
├── security/
│
└── utils/

downloads/
logs/

config.py
main.py
requirements.txt
Dockerfile
docker-compose.yml
```

---

## Security

Although Telegram bots are publicly discoverable by username, this bot is intentionally **private**.

Every request — including button taps — is checked against a whitelist of Telegram user IDs before any download begins.

```
Telegram User
      │
      ▼
   Allowed?
   │        │
  Yes       No
   │        │
   ▼        ▼
Download  Access Denied
```

This matters because the bot runs on a small, cost-limited cloud server — without this check, anyone who discovered the bot's username could consume server resources or run up hosting costs.

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/muhzin124/CloudFetch.git
cd CloudFetch
```

Copy the environment file:

```bash
cp .env.example .env
```

Fill in your own values:

```text
BOT_TOKEN=your_bot_token
ALLOWED_USER_IDS=123456789,987654321
```

Run it with Docker:

```bash
docker compose up --build
```

No separate Python install or manual FFmpeg setup needed — Docker handles all of it.

---

## Deployment

CloudFetch runs on an **AWS Lightsail** Ubuntu instance using Docker.

Since this bot is only used by my father and me, I wanted to keep hosting cost as low as possible. Instead of using EC2 — which bills compute, storage, and data transfer as separate line items — I chose **AWS Lightsail's $5/month plan**, which bundles compute, storage, networking, and data transfer into one predictable monthly price. For a small private bot with only two users, it provides more than enough resources while keeping the infrastructure simple and inexpensive.

Deployment itself is intentionally simple:

```bash
rsync -avz \
  --exclude='.venv' \
  --exclude='__pycache__' \
  -e "ssh -i your-key.pem" \
  ./CloudFetch/ \
  ubuntu@SERVER_IP:/home/ubuntu/CloudFetch/

ssh -i your-key.pem ubuntu@SERVER_IP

cd CloudFetch
docker compose up --build -d
```

---

## A Real Deployment Challenge

The bot runs on the $5/month AWS Lightsail plan, which has only **512 MB of RAM**.

During the initial deployment, Docker needed to install FFmpeg and Python dependencies, but the build kept failing because Linux's Out-Of-Memory (OOM) killer terminated the Docker process partway through.

Instead of moving to a larger, more expensive server, I created a **1 GB swap file**, which gave the build enough temporary memory to finish successfully.

It was a simple fix, but it reinforced an important lesson: software that works perfectly on a development machine doesn't always build successfully on resource-constrained production servers — and the fix doesn't always mean paying for more hardware.

---

## What I Learned

Building CloudFetch helped me gain hands-on experience with:

- Python fundamentals
- Working with third-party libraries (`python-telegram-bot`, `yt-dlp`)
- Docker and containerized applications
- Linux server administration
- AWS Lightsail deployment
- Environment variables and configuration management
- Debugging deployment issues on resource-constrained servers
- Using AI as a development assistant while understanding, testing, and iterating on the solution

---

## Future Improvements

- GitHub Actions for automatic deployment on push
- Health monitoring
- Log rotation
- Better error reporting
- Download progress updates
- A setup guide for others who want to self-host this

---

## License

See [LICENSE](./LICENSE).

## Author

**Muhzin Muneer**

If you have suggestions or improvements, feel free to open an issue or submit a pull request.
