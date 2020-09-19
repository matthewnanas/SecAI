# Import things and stuff
import face_recognition
import numpy as np
import cv2
import os
import datetime
import uploadfile # Pycharm gives error but call works fine.
from flask import Response
from flask import Flask
from flask import render_template
import threading
import notifications

# Create some variables
face_locations = []
face_encodings = []
face_names = []
process_frame = True
datasets = []
app = Flask(__name__)
processedFrame = None
lock = threading.Lock()
personDetected = False
frameCounter = 0
name = ""
threatCounter = 0
notificationSent = False

# Video input object
cap = cv2.VideoCapture(0)

# Initialize human detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Array of knowns
known_faces = []
known_names = []

def faceReg():
    global processedFrame, lock, face_locations, face_encodings, face_names, process_frame, datasets, known_faces, known_names, personDetected, name, threatCounter, notificationSent
    # Find all people and datasets for each person
    os.chdir("../")
    for filename in os.listdir("assets"):
        if filename == "numbers.txt":
            continue
        images = []
        for image in os.listdir(f"assets/{filename}"):
            if image.lower().endswith(".jpg") or image.lower().endswith(".png"):
                my_image = face_recognition.load_image_file("assets/" + str(filename) + "/" + image)
                print("assets/" + str(filename) + "/" + image)
                try:
                    datasets.append(face_recognition.face_encodings(my_image)[0])
                except:
                    print("For image, " + str(image) + ", could not find face... Image deleted.")
                    os.remove("assets/" + str(filename) + "/" + image)
                    continue
                known_names.append(str(filename))
    os.chdir("./nodes") # store cwd before changing?

    # Add all images to known lists

    for data in datasets:
        known_faces.append(data)

    # Video setup
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while True:
        # Get video input frames
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create contours for humans
        boxes, weights = hog.detectMultiScale(frame, winStride=(4, 4), padding=(4, 4), scale=1.05 )
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            # draw contours
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # Write the flipped frame
        out.write(frame)

        # Compress frames
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
            cv2.rectangle(frame, (left, bottom - 45), (right, bottom), (0, 0, 100), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if len(weights) != 0:
            print('Human detected!')
            frameCounter = 0
            personDetected = True
            if name == "Unknown":
                threatCounter += 1
            elif name == "":
                threatCounter += 1
                pass
            else:
                print("Known person found!")

            if threatCounter >= 10 and not notificationSent:
                print("Threat detected")
                # Send twilio message
                notifications.sendMsg("SecAI notification: Threat detected!")
                notificationSent = True
        elif len(weights) == 0 and personDetected:
            frameCounter += 1
            if frameCounter >= 10:
                print("Person Left")
                personDetected = False
                notificationSent = False

        cv2.imshow('Face detection', frame)

        with lock:
            processedFrame = frame.copy()

        # Kill code on ESC
        k = cv2.waitKey(30)
        if k == 27:
            break

    # Kill video
    cap.release()
    out.release()
    upload_file_videoname = datetime.datetime.now().strftime("%m-%d-%y-%H-%M-%S")
    uploadfile.upload_video(upload_file_videoname + ".avi")
    cv2.destroyAllWindows()

def processFrames():
    global processedFrame, lock
    while True:
        with lock:
            if processedFrame is None:
                continue
            
            (flag, encodedImage) = cv2.imencode(".jpg", processedFrame)
            
            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(processFrames(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    recognize = threading.Thread(target=faceReg)
    recognize.daemon = True
    recognize.start()

    # start the flask app
    app.run(host="0.0.0.0", port="1337", debug=True,
        threaded=True, use_reloader=False)
