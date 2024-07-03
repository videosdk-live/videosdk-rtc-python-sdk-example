# Video SDK for Python - Participant Image Capture

[![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/python/api/sdk-reference/classes/participant/methods#capture_image)
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

At Video SDK, we’re building tools to help companies create world-class collaborative products with capabilities of live audio/videos, compose cloud recordings/RTMP/HLS, and interaction APIs.

## Real-Time Participant Image Capture

This repository provides an example of capturing images of participants in real-time using the Video SDK with Python. The example captures an image when a participant's video stream is enabled and saves it locally.

## Features

- Real-time participant video stream monitoring
- Capture and save participant images locally
- Easy setup and integration

## Prerequisites

- Python 3.11 or later
- Valid [Video SDK Account](https://app.videosdk.live/signup)

## Setup Guide

### Step 1: Clone the Repository

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/videosdk-rtc-python-sdk-example.git
cd videosdk-rtc-python-sdk-example/capture-image
```

### Step 2: Install necessary libraries

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

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

Execute the script to start the participant image capture example.

```bash
python capture_image.py
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
