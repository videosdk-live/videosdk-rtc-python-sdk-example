import asyncio
import fractions
import os
import cv2
from videosdk import (MeetingConfig, VideoSDK, Meeting, Participant,
                      Stream, ParticipantEventHandler, MeetingEventHandler, CustomVideoTrack)
from av import VideoFrame

VIDEOSDK_TOKEN = os.getenv("VIDEOSDK_TOKEN")
MEETING_ID = os.getenv("MEETING_ID")
NAME = os.getenv("NAME")

#
TRANSFORM = "rotate"

loop = asyncio.get_event_loop()
meeting: Meeting = None

VIDEO_PTIME = 1 / 30
VIDEO_CLOCK_RATE = 90000
VIDEO_TIME_BASE = fractions.Fraction(1, VIDEO_CLOCK_RATE)


class VideoTransformTrack(CustomVideoTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "rotate":
            # rotate image
            img = frame.to_ndarray(format="bgr24")
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D(
                (cols / 2, rows / 2), frame.time * 45, 1)
            img = cv2.warpAffine(img, M, (cols, rows))

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame

        else:
            return frame


def transform_video(track: CustomVideoTrack):
    global meeting
    meeting.add_custom_video_track(
        track=VideoTransformTrack(track=track, transform=TRANSFORM)
    )


def stop_transform_video():
    global meeting
    meeting.disable_webcam()


class MyMeetingEventHandler(MeetingEventHandler):
    def __init__(self):
        super().__init__()

    def on_meeting_joined(self, data):
        print("meeting joined")

    def on_meeting_left(self, data):
        print("meeting left")

    def on_participant_joined(self, participant: Participant):
        print("participant joined ", participant)
        participant.add_event_listener(
            ParticipantEventHandler(participant_id=participant.id)
        )

    def on_participant_left(self, participant: Participant):
        print("participant left ", type(participant))
        stop_transform_video()


class ParticipantEventHandler(ParticipantEventHandler):
    def __init__(self, participant_id: str):
        super().__init__()
        self.participant_id = participant_id

    def on_stream_enabled(self, stream: Stream):
        print(self.participant_id, "paricipant :: stream enabled", stream.kind)
        if stream.kind == "video":
            transform_video(stream.track)

    def on_stream_disabled(self, stream: Stream):
        print(self.participant_id, "paricipant :: stream disabled", stream.kind)
        if stream.kind == "video":
            stop_transform_video()


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
