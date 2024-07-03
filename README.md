# Video SDK for Python

[![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/python/guide/video-and-audio-calling/ai-and-ml/face-detection)
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

At Video SDK, we’re building tools to help companies create world-class collaborative products with capabilities of live audio/videos, compose cloud recordings/RTMP/HLS, and interaction APIs.

## Table of Contents

- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Community](#community)

## Documentation

For more detailed information, visit the [Video SDK Documentation](https://docs.videosdk.live/python/guide/video-and-audio-calling/ai-and-ml/vision-ai).

## Structure

The repository is organized as follows:

- **capture-image**: Contains [scripts](./capture-image) for capturing images.

- **face-detection-and-landmarks**: Includes [scripts](./face-detection-and-landmarks/) for face detection and landmark identification.

- **face-recognition**: face recognition feature on participant stream. _coming soon_

- **python-rtc**: Basic Python RTC to join VideoSDK Meeting.

- **transform-audio**: audio transformation. _coming soon_

- **transform-video**: Contains [scripts](./transform-video/) for video transformation.

- **vision-ai**: Contains vision AI related [scripts](./vision-ai).

## Getting Started

To get started with the Video SDK Face Detection, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/videosdk-live/videosdk-rtc-python-sdk-example.git
   ```

2. **Change Directory:**

   Let's run a example that detects the face from the stream. change the directory to `face-detection-and-landmarks`.

   ```bash
   cd videosdk-rtc-python-sdk-example/face-detection-and-landmarks
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

- Copy the example environment file:
  ```bash
  cp .env.example .env
  ```
- Update `.env` with your credentials and configurations.

5. **Run a sample script:**

- For example, to run the face detection script:
  ```bash
  python face_detection.py
  ```

## Community

- [Discord](https://discord.gg/Gpmj6eCq5u) - Join the Video SDK community, ask questions, and share tips.
- [Twitter](https://twitter.com/video_sdk) - Follow us for updates, announcements, blog posts, and general tips.
