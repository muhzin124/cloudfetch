# ---------------------------------------------------------
# Base image: official Python slim image.
# "slim" = smaller size than the full python image, since we
# don't need extras like build tools that a full desktop
# Python install would include. Smaller image = faster to
# build, faster to deploy, less disk usage on the server.
# ---------------------------------------------------------
FROM python:3.13-slim

# ---------------------------------------------------------
# Make Python print output immediately instead of buffering
# it internally. Without this, logs (like our startup
# message and yt-dlp's download progress) only show up in
# `docker logs` in batches or at shutdown, which makes
# debugging on the server confusing. This makes logs appear
# in real time, exactly like running `python main.py` directly.
# ---------------------------------------------------------
ENV PYTHONUNBUFFERED=1

# ---------------------------------------------------------
# Install ffmpeg.
# yt-dlp needs this to merge separate video+audio streams
# into one file (we saw this happen with the YouTube test:
# f299 video + f140 audio -> merged into one .mp4).
# The python:slim image is Debian-based, so we use apt-get.
# --no-install-recommends keeps the image smaller by skipping
# optional packages we don't need.
# We clean up apt's cache afterward to keep the image lean.
# ---------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl unzip && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------
# Install Deno.
# yt-dlp needs an actual JavaScript runtime to decode
# YouTube's signature-scrambling scheme on some videos
# (without it, yt-dlp can only fetch thumbnail images, not
# real video/audio formats — this is what caused the
# "Requested format is not available" error on some links).
# Deno is yt-dlp's recommended lightweight JS runtime for
# this purpose.
# ---------------------------------------------------------
RUN curl -fsSL https://deno.land/install.sh | sh
ENV PATH="/root/.deno/bin:${PATH}"

# ---------------------------------------------------------
# Set the working directory inside the container.
# All following commands (COPY, RUN, CMD) run relative to
# this path unless stated otherwise.
# ---------------------------------------------------------
WORKDIR /app

# ---------------------------------------------------------
# Copy requirements.txt FIRST, before the rest of the code.
# This is a deliberate ordering trick: Docker caches each
# step. If only your bot code changes (not requirements.txt),
# Docker can reuse the cached "pip install" step instead of
# re-downloading every package on every build. Saves a lot
# of time during development.
# ---------------------------------------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------
# Now copy the rest of the application code.
# Note: .env is NOT copied here — see .dockerignore.
# Secrets should never be baked into an image; they're
# passed in at container run-time instead (see
# docker-compose.yml or the `docker run -e` flag).
# ---------------------------------------------------------
COPY . .

# ---------------------------------------------------------
# Create the folders the app expects to exist at runtime
# (downloads/ is used as temp scratch space per-download).
# ---------------------------------------------------------
RUN mkdir -p downloads logs

# ---------------------------------------------------------
# Command that runs when the container starts.
# This just runs your existing main.py exactly like you do
# locally with `python main.py`.
# ---------------------------------------------------------
CMD ["python", "main.py"]
