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
meeting: Meeting = None

TRANSFORM = "blur-face-mediapipe"
# TRANSFORM = "blur-face"
# TRANSFORM = "blur"


class TransformVideoProcessor():
    def __init__(self) -> None:
        print("Processor initialized")
        self.transform = TRANSFORM
        if self.transform == "blur-face":
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if self.transform == "blur-face-mediapipe":
            self.face_detection = mp.solutions.face_detection.FaceDetection(
                min_detection_confidence=0.5)

    def process(self, frame: VideoFrame) -> VideoFrame:
        if self.transform == "blur":
            # implement blur
            img = frame.to_ndarray(format="bgr24")
            img = cv2.GaussianBlur(img, (15, 15), 10)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "blur-face":
            img = frame.to_ndarray(format="bgr24")

            # Detect faces
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Blur each face
            for (x, y, w, h) in faces:
                face = img[y:y+h, x:x+w]
                face = cv2.GaussianBlur(face, (25, 25), 20)
                img[y:y+h, x:x+w] = face

            # Rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "blur-face-mediapipe":
            img = frame.to_ndarray(format="bgr24")

            # Convert the BGR image to RGB before processing.
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Perform face detection
            results = self.face_detection.process(img_rgb)

            if results.detections:
                for detection in results.detections:
                    # Get bounding box coordinates
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = img.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin *
                                                           ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    x, y = max(0, x), max(0, y)
                    w, h = min(w, iw - x), min(h, ih - y)

                    # Apply Gaussian blur to the face region
                    face = img[y:y+h, x:x+w]
                    face = cv2.GaussianBlur(face, (25, 25), 30)
                    img[y:y+h, x:x+w] = face

            # Rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        else:
            return frame


class ProcessedVideoTrack(CustomVideoTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track
        self.processor = TransformVideoProcessor()

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
