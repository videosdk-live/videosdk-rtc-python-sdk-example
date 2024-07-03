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

# Initialize Mediapipe face detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

meeting: Meeting = None


class FaceDetectionProcessor():
    def __init__(self) -> None:
        print("Processor initialized")

    def process(self, frame: VideoFrame) -> VideoFrame:
        # Convert frame to image
        img = frame.to_ndarray(format="bgr24")

        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform face detection
        with mp_face_detection.FaceDetection(
            min_detection_confidence=0.2
        ) as face_detection:
            results = face_detection.process(img_rgb)

            # Draw face detections on the image
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(img, detection)

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
        self.processor = FaceDetectionProcessor()

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
        print("on_meeting_left")

    def on_participant_joined(self, participant: Participant):
        participant.add_event_listener(
            MyParticipantEventHandler(participant_id=participant.id)
        )

    def on_participant_left(self, participant: Participant):
        print("on_participant_left")


class MyParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant_id: str):
        super().__init__()
        self.participant_id = participant_id

    def on_stream_enabled(self, stream: Stream):
        print("on_stream_enabled", stream.kind)
        if stream.kind == "video":
            process_video(track=stream.track)

    def on_stream_disabled(self, stream: Stream):
        print("on_stream_disabled")


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
