import asyncio
import os
from videosdk import (
    MeetingConfig,
    VideoSDK,
    Participant,
    Stream,
    MeetingEventHandler,
    ParticipantEventHandler,
    Meeting,
)

from dotenv import load_dotenv

load_dotenv()
VIDEOSDK_TOKEN = os.getenv("VIDEOSDK_TOKEN")
MEETING_ID = os.getenv("MEETING_ID")
NAME = os.getenv("NAME")

loop = asyncio.get_event_loop()

meeting: Meeting = None


class MyMeetingEventHandler(MeetingEventHandler):
    def __init__(self):
        super().__init__()

    def on_meeting_left(self, data):
        print("meeting left")

    def on_participant_joined(self, participant: Participant):
        print("participant joined")
        participant.add_event_listener(ParticipantEventHandler(participant=participant))

    def on_participant_left(self, participant: Participant):
        print("participant left")


class ParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant: Participant):
        super().__init__()
        self.participant = participant

    def on_stream_enabled(self, stream: Stream):
        print("stream enabled", stream.kind)

    def on_stream_disabled(self, stream: Stream):
        print("stream disabled", stream.kind)


def main():
    global meeting

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


if __name__ == "__main__":
    main()
    loop.run_forever()
