import asyncio
import os
from videosdk import MeetingConfig, VideoSDK, Participant, Stream, MeetingEventHandler, ParticipantEventHandler, CustomVideoTrack, Meeting
import mediapipe as mp
import cv2
from av import VideoFrame
from dotenv import load_dotenv
load_dotenv()

VIDEOSDK_TOKEN = os.getenv("VIDEOSDK_TOKEN")
MEETING_ID = os.getenv("MEETING_ID")
NAME = os.getenv("NAME")
loop = asyncio.get_event_loop()
task: asyncio.Task = None

meeting: Meeting = None

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


class EdgeVideoProcessor():
    def __init__(self) -> None:
        print("Processor initialized")

    def process(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

        # rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame


class ProcessedVideoTrack(CustomVideoTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track
        self.processor = EdgeVideoProcessor()

    async def recv(self):
        frame = await self.track.recv()
        new_frame = self.processor.process(frame)
        return new_frame


def process_video(track: CustomVideoTrack):
    global meeting
    meeting.add_custom_video_track(
        track=ProcessedVideoTrack(track=track)
    )


class MyMeetingEventHandler(MeetingEventHandler):
    def __init__(self):
        super().__init__()

    def on_meeting_left(self, data):
        if task is not None:
            task.cancel()

    def on_participant_joined(self, participant: Participant):
        participant.add_event_listener(
            MyParticipantEventHandler(participant_id=participant.id)
        )

    def on_participant_left(self, participant: Participant):
        if task is not None:
            task.cancel()


class MyParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant_id: str):
        super().__init__()
        self.participant_id = participant_id

    def on_stream_enabled(self, stream: Stream):
        global task
        if stream.kind == "video":
            process_video(track=stream.track)

    def on_stream_disabled(self, stream: Stream):
        if task is not None:
            task.cancel()


def main():
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


if __name__ == "__main__":
    main()
    loop.run_forever()
