import cv2
import mediapipe as mp
import numpy as np

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


def draw_on_image():
    cv2.circle(image, mid_point, 4, (0, 0, 255), cv2.FILLED)
    cv2.rectangle(image, bounding_boxes[0], bounding_boxes[1], (255, 255, 0), 3)

    cv2.rectangle(image, (int(width / 2), 0), (int(width/2), int(height)), (255, 255, 0), 1)
    cv2.rectangle(image, (0, int(height / 2)), (int(width), int(height/2)), (255, 255, 0), 1)

    cv2.rectangle(image, (int(width / 2) - 80, 0), (int(width / 2) - 80, int(height)), (255, 255, 0), 1)
    cv2.rectangle(image, (int(width / 2) + 80, 0), (int(width / 2) + 80, int(height)), (255, 255, 0), 1)

    cv2.rectangle(image, (0, int(height / 2) - 80), (int(width), int(height / 2) - 80), (255, 255, 0), 1)
    cv2.rectangle(image, (0, int(height / 2) + 80), (int(width), int(height / 2) + 80), (255, 255, 0), 1)



with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)
        height, width, rgb = image.shape
        if not success:
            print("Ignoring Camera Frame!")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


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


                height_range = (int(height / 2) - 80, int(height / 2) + 80)
                width_range = (int(width / 2) - 80, int(width / 2) + 80)

                draw_on_image()

                if mid_point[0] in range(width_range[0], width_range[1]):
                    print("In Range Horizontally!")
                else:
                    if mid_point[0] < width_range[0]:
                        print("Go left!")
                    else:
                        print("Go Right!")

                if mid_point[1] in range(height_range[0], height_range[1]):
                    print("In Range Vertically!")
                else:
                    if mid_point[1] < height_range[0]:
                        print("Go Up!")
                    else:
                        print("Go Down!")



        cv2.imshow('MediaPipe Face Detection', image)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
