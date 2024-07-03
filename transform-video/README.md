# Video SDK for Python - Transform Video

[![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/python/guide/video-and-audio-calling/ai-and-ml/transform-video)
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

At Video SDK, we’re building tools to help companies create world-class collaborative products with capabilities of live audio/videos, compose cloud recordings/RTMP/HLS, and interaction APIs.

## Transform Video Frames in Real-Time

This repository provides an example of transforming video frames into a cartoon-like appearance using the Video SDK with Python.

## Features

- Real-time video transformation
- Face detection
- Cartoon-like filter application
- Easy setup and integration
- transform: `cartoon`, `edges`, `blur`, `face-blur`, `rotate`

## Prerequisites

- Python 3.11 or later
- Valid [Video SDK Account](https://app.videosdk.live/signup)
- Install necessary libraries

```bash
pip install -r requirements.txt
```

## Setup Guide

### Step 1: Clone the Repository

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/videosdk-python-transform-video-example.git
```

### Step 2: Configure Environment Variables

Copy the `.env.example` file to `.env` and add your Video SDK token, meeting ID, and name.

```bash
cp .env.example .env
```

Modify the `.env` file with your details:

```env
VIDEOSDK_TOKEN="YOUR_VIDEOSDK_TOKEN"
MEETING_ID="YOUR_MEETING_ID"
NAME="YOUR_NAME"
```

### Step 4: Run the Example

Execute the script to start transforming video frames.

```bash
python cartoon.py
```

## Key Concepts

- **Meeting**: Represents real-time audio and video communication.
- **Session**: The duration spent in a meeting, multiple sessions can be part of a single meeting.
- **Participant**: Someone attending the meeting's session. The local participant refers to yourself, and others are remote participants.
- **Stream**: Video or audio media content published by participants.

## Token Generation

Tokens are used to create and validate meetings using the API and initialize a meeting.

### Development Environment

Use a temporary token for development. To create a temporary token, go to the VideoSDK [dashboard](https://app.videosdk.live/api-keys).

### Production Environment

Set up an authentication server to authorize users for production. Refer to our example repositories for setting up an authentication server: [videosdk-rtc-api-server-examples](https://github.com/videosdk-live/videosdk-rtc-api-server-examples).

## Documentation

For more detailed information, visit the [Video SDK Documentation](https://docs.videosdk.live/python/guide/video-and-audio-calling/ai-and-ml/transform-video).

Feel free to modify the transformation logic inside the `recv` method of the `ProcessedVideoTrack` class to apply different kinds of video transformations.

## Community

- [Discord](https://discord.gg/Gpmj6eCq5u) - Join the Video SDK community, ask questions, and share tips.
- [Twitter](https://twitter.com/video_sdk) - Follow us for updates, announcements, blog posts, and general tips.
