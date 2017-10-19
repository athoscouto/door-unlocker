from collections import defaultdict
from uuid import uuid4
from utils import *

import pickle
import face_recognition
import cv2

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(1)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = 0

counter = defaultdict(lambda : 0)

id_to_encoding = load_encodings()
if id_to_encoding == {}:
    uuid = []
    familiar_faces_encodings = []
else:
    uids, familiar_faces_encodings = zip(*id_to_encoding.items())
id_to_name = load_id_to_name()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


    # Only process every other frame of video to save time
    if process_this_frame == 1:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        new_counter = defaultdict(lambda : 0)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(familiar_faces_encodings, face_encoding)
            uid = int(uuid4().hex, 16)

            for i, val in enumerate(matches):
                if val:
                    uid = uids[i]
                    break

            name = id_to_name[uid]

            face_names.append(name)
            if name != "Unknown":
                new_counter[name] = counter[name] + 1

        counter = new_counter

        print face_names
        for name in face_names:
            print "Checking if {} is here. {}0% checked".format(name, counter[name])
            if counter[name] == 10:
                print "{} is here! Door unlocked.".format(name)
                counter = defaultdict(lambda : 0)

    process_this_frame = 1 + process_this_frame
    process_this_frame = process_this_frame % 10



    # # Display the results
    # for (top, right, bottom, left), name in zip(face_locations, face_names):
    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    #     top *= 4
    #     right *= 4
    #     bottom *= 4
    #     left *= 4

    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # # Display the resulting image
    # cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
