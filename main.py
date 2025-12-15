import cv2
import mediapipe as mp

#new updates
#adding mediapipe for hand dect

mp_hand = mp.solutions.hands #loading the model
hands = mp_hand.Hands(max_num_hands = 1, min_detection_confidence = 0.7,min_tracking_confidence = 0.7)
mp_draw = mp.solutions.drawing_utils

def camera():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if not ret:
            print("cam not working")
            break
        if result.multi_hand_landmarks:
            for hands_landmark in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hands_landmark,
                    mp_hand.HAND_CONNECTIONS
                )
        cv2.imshow("agnik",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cam.release()
    cv2.destroyAllWindows()
            
#main chekcing

if __name__ == "__main__":
    camera()