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
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# Define the lip connections
LIPS = mp_face_mesh.FACEMESH_LIPS

meeting: Meeting = None


class LipDetectionProcessor():
    def __init__(self) -> None:
        print("Processor initialized")
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def process(self, frame: VideoFrame) -> VideoFrame:
        # Convert frame to image
        # Convert frame to image
        img = frame.to_ndarray(format="bgr24")

        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform face landmark detection
        results = self.face_mesh.process(img_rgb)

        # Draw only the lip landmarks on the image
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=LIPS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                )

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
        self.processor = LipDetectionProcessor()

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
            ParticipantEventHandler(participant_id=participant.id)
        )

    def on_participant_left(self, participant: Participant):
        print("on_participant_left")


class ParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant_id: str):
        super().__init__()
        self.participant_id = participant_id

    def on_stream_enabled(self, stream: Stream):
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
