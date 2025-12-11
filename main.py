import cv2
import mediapipe as mp

#new updates

def camera():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        if not ret:
            print("cam not working")
            break
        cv2.imshow("agnik",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cam.release()
    cv2.destroyAllWindows()
            


if __name__ == "__main__":
    camera()