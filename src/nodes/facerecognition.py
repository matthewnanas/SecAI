# Import things and stuff
import face_recognition
import numpy as np
import cv2

# Create some variables
face_locations = []
face_encodings = []
face_names = []
process_frame = True

# Video input object
cap = cv2.VideoCapture(0)

# Load samples
my_image = face_recognition.load_image_file("me.jpg")
encoded_image = face_recognition.face_encodings(my_image)[0]

# Array of knowns
known_faces = [
    encoded_image,
]
known_names = [
    "matthew",
]

while(True) :
    # Get video input frames
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Compress frames
    compressed = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert frames to RGB from HSV
    rgb_frames = compressed[:, :, ::-1]

    # Find faces every 2 frames
    if process_frame:
        face_locations = face_recognition.face_locations(rgb_frames)
        face_encodings = face_recognition.face_encodings(rgb_frames, face_locations)

        face_names = []
        for face_encodings in face_encodings:
            # See if any faces are detected
            matches = face_recognition.compare_faces(known_faces, face_encodings)
            name = "Unknown"

            face_distance = face_recognition.face_distance(known_faces, face_encodings)
            best_match = np.argmin(face_distance)
            if matches[best_match]:
                name = known_names[best_match]

            face_names.append(name)

    process_frame = not process_frame

    # Display in opencv window
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Upscale back to original size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Box face
        cv2.rectangle(frame, (left, bottom - 50), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Face detection', frame)

    # Kill code on ESC
    k = cv2.waitKey(30)
    if k == 27:
        break

# Kill video
cap.release()
cv2.destroyAllWindows()
