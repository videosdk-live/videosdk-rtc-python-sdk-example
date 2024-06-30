import base64
import asyncio
import os
from videosdk import MeetingConfig, VideoSDK, Stream, Participant, Meeting, MeetingEventHandler, ParticipantEventHandler, PubSubPublishConfig
from openai import OpenAI
from PIL import Image
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()
VIDEOSDK_TOKEN = os.getenv("VIDEOSDK_TOKEN")
MEETING_ID = os.getenv("MEETING_ID")
NAME = os.getenv("NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

loop = asyncio.get_event_loop()
task: asyncio.Task = None
meeting: Meeting = None
participant: Participant = None


async def capture_video() -> str:
    global participant
    filepath = "capture_video.png"

    # asynchronously capture image from video
    img: Image = await participant.async_capture_image(filepath)

    # Convert the image to a base64-encoded string
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    image_frame = base64.b64encode(buffer.getvalue()).decode("utf-8")

    await vision_ai(image_frame)


async def vision_ai(image_frame: str):
    try:
        # Prepare the messages for the OpenAI API request
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    "Describe the image",
                    {"image": image_frame, "resize": 768},
                ],
            },
        ]

        # Make a request to the OpenAI API to generate a description of the image
        result = openai_client.chat.completions.create(
            model="gpt-4o",
            max_tokens=200,
            messages=messages
        )

        # Extract the description from the API response
        description = result.choices[0].message.content
        print(description)

        # Create a Pub/Sub publish configuration
        pubsub_config = PubSubPublishConfig(
            topic="CHAT",
            message=description
        )

        # Publish the description to the specified Pub/Sub topic
        await meeting.pubsub.publish(pubsub_config)

        # Write the description into the file
        with open("videosdk.txt", "w") as f:
            f.write(f"Content {result.choices[0].message.content}")
    except Exception as e:
        print("Error:", e)


class MyMeetingEventHandler(MeetingEventHandler):
    def __init__(self):
        super().__init__()

    def on_meeting_left(self, data):
        if task is not None:
            task.cancel()

    def on_participant_joined(self, p: Participant):
        global participant
        p.add_event_listener(
            MyParticipantEventHandler()
        )
        participant = p

    def on_participant_left(self, p: Participant):
        if task is not None:
            task.cancel()


class MyParticipantEventHandler(ParticipantEventHandler):
    def __init__(self):
        super().__init__()

    def on_stream_enabled(self, stream: Stream):
        global task, participant
        if stream.kind == "video":
            print("stream is video..")
            task = loop.create_task(capture_video())

    def on_stream_disabled(self, stream: Stream):
        if task is not None:
            task.cancel()


def main():
    try:
        global meeting
        # Example usage:
        meeting_config = MeetingConfig(
            meeting_id=MEETING_ID,
            name=NAME,
            mic_enabled=False,
            webcam_enabled=False,
            token=VIDEOSDK_TOKEN,
        )
        meeting = VideoSDK.init_meeting(**meeting_config)

        print("adding event listener...")
        meeting.add_event_listener(MyMeetingEventHandler())

        print("joining into meeting...")
        meeting.join()

    except Exception as e:
        print("error", e)


if __name__ == "__main__":
    main()
    loop.run_forever()
