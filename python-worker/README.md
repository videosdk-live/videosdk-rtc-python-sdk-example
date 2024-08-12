# Video SDK for Python - Dockerization of Python Worker

[![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/python/api/sdk-reference/classes/participant/methods#capture_image)
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

At Video SDK, we’re building tools to help companies create world-class collaborative products with capabilities of live audio/videos, compose cloud recordings/RTMP/HLS, and interaction APIs.

## Dockerizing Python Worker

This repository provides a minimalistic example for how to dockerize python worker using the Video SDK with Python. This minimalistic example demostrates how to listen for meeting and participant events with Python Worker.

## Features

- Dockerization
- Listening meeting events
- Listening participant events
- Easy setup and integration

## Prerequisites

- [Docker Runtime](https://docs.docker.com/engine/install)
- Valid [Video SDK Account](https://app.videosdk.live/signup)

## Setup Guide

### Step 1: Clone the Repository

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/videosdk-rtc-python-sdk-example.git
cd videosdk-rtc-python-sdk-example/python-worker
```

### Step 2: Build docker image

```bash
docker build -t videosdk-python-worker .
```

### Step 3: Configure Environment Variables

Copy the `.env.example` file to `.env` and add your Video SDK token, meeting ID, and name.

```bash
cp ../.env.example .env
```

Modify the `.env` file with your details:

```env
VIDEOSDK_TOKEN="YOUR_VIDEOSDK_TOKEN"
MEETING_ID="YOUR_MEETING_ID"
NAME="YOUR_NAME"
```

### Step 4: Run the docker container

Execute the command to run the python-worker docker container.

```bash
docker run --env ENV_VARS="$(cat ./.env)" videosdk-python-worker
```

## Key Concepts

- **Meeting**: Represents real-time audio and video communication.
- **Participant**: Someone attending the meeting's session. The local participant refers to yourself, and others are remote participants.
- **Stream**: Video or audio media content published by participants.

## Token Generation

Tokens are used to create and validate meetings using the API and initialize a meeting.

### Development Environment

Use a temporary token for development. To create a temporary token, go to the VideoSDK [dashboard](https://app.videosdk.live/api-keys).

### Production Environment

Set up an authentication server to authorize users for production. Refer to our example repositories for setting up an authentication server: [videosdk-rtc-api-server-examples](https://github.com/videosdk-live/videosdk-rtc-api-server-examples).

## Documentation

For more detailed information, visit the [Video SDK Documentation](https://docs.videosdk.live/python/api/sdk-reference/classes/participant/methods#capture_image).

Feel free to modify the code to suit your specific use case.

## Community

- [Discord](https://discord.gg/Gpmj6eCq5u) - Join the Video SDK community, ask questions, and share tips.
- [Twitter](https://twitter.com/video_sdk) - Follow us for updates, announcements, blog posts, and general tips.

```

Let me know if you need any further modifications or additional information included!
```
