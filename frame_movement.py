import cv2
import mediapipe as mp
import numpy as np

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


def draw_on_image():
    cv2.circle(image, mid_point, 4, (0, 0, 255), cv2.FILLED)
    cv2.rectangle(image, bounding_boxes[0], bounding_boxes[1], (255, 255, 0), 3)


def slide_window():
    pass


with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        height, width, rgb = image.shape
        if not success:
            print("Ignoring Camera Frame!")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        y = int(height * 0.2)
        x = int(width * 0.2)
        h = int(height * 0.6)
        w = int(width * 0.6)

        crop = image

        if results.detections:
            for detection in results.detections:
                get_loc = detection.location_data.relative_bounding_box
                location = {
                    "xmin": int(get_loc.xmin * width),
                    "ymin": int(get_loc.ymin * height),
                    "width": int(get_loc.width * width),
                    "height": int(get_loc.height * height)
                }

                bounding_boxes = [(location['xmin'], location['ymin']),
                                  (location['xmin'] + location['width'], location['ymin'] + location['height'])]

                mid_point = (
                    int(location['width'] / 2) + location['xmin'], int(location['height'] / 2) + location['ymin'])

                x_axis_threshold = (np.add(np.multiply(w, 0.8), x), (np.add(np.multiply(w, 0.2), x)))  # left, right
                y_axis_threshold = (np.add(np.multiply(h, 0.3), y), (np.add(np.multiply(h, 0.7), y)))  # up, down

                if mid_point[0] > x_axis_threshold[0]:
                    x = int(x + mid_point[0] - x_axis_threshold[0])
                    print("Slide left!")

                if mid_point[0] < x_axis_threshold[1]:
                    x = int(x + mid_point[0] - x_axis_threshold[1])
                    print("Slide right!")

                if mid_point[1] > y_axis_threshold[1]:
                    y = int(y + mid_point[1] - y_axis_threshold[1])
                    print("Slide down!")

                if mid_point[1] < y_axis_threshold[0]:
                    y = int(y + mid_point[1] - y_axis_threshold[0])
                    print("Slide up!")

                crop = image[y:y + h, x:x + w]

        try:
            cv2.imshow('MediaPipe Face Detection', cv2.flip(crop, 1))
        except:
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
