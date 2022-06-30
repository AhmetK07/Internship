import os
import cv2
import uuid
from glob import glob


def MkDirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"There has been an error while creating directory, we have an already {path} path defined.")


def SaveFrames(VideoPath, SaveDirs, frameGap):
    NameOfVid = VideoPath.split("/")[-1].split(".")[0]
    SaveLoc = os.path.join(SaveDirs, NameOfVid)
    MkDirs(SaveLoc)

    CapVid = cv2.VideoCapture(VideoPath)
    Index = 0

    while True:
        ReturnedFrame, frame = CapVid.read()
        myuuid = uuid.uuid4()

        if ReturnedFrame == False:
            CapVid.release()
            break

        if Index == 0:
            cv2.imwrite(f"{SaveLoc}/{Index}_{myuuid}.jpg", frame)

        else:
            if Index % frameGap == 0:
                cv2.imwrite(f"{SaveLoc}/{Index}_{myuuid}.jpg", frame)

        Index += 1


if __name__ == "__main__":
    VideoPath = glob("Videos/*")
    SaveDirs = "save"

    for path in VideoPath:
        SaveFrames(path, SaveDirs, frameGap=10)
