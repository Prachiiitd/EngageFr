from io import BytesIO
import cv2
from faceDetector import get_face_detector, find_faces, draw_faces
from faceRecognition import faceRec

face_model = get_face_detector()
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, img = cap.read()
        faces = find_faces(img, face_model)
        haveFace, faces = draw_faces(img, faces)

        if haveFace:
            print(BytesIO(faces), "have face")
            try:
                faceRec(BytesIO(faces), "WebCam")
            except Exception as e:
                print(e)
                continue
        else:
            print("No faces Found")
        cv2.imshow('WebCam', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except (KeyboardInterrupt, Exception) as e:
    print(e)
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Shutdown requested...exiting")
