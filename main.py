import cv2
import mediapipe as mp
import math

#new updates
#adding mediapipe for hand dect
#testing

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

        #mediapipe draw hand loop
        if result.multi_hand_landmarks:
            for hands_landmark in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hands_landmark,
                    mp_hand.HAND_CONNECTIONS
                )

                #setting up the hands coords
                hand = result.multi_hand_landmarks[0]

                wrist = hand.landmark[0]
                index = hand.landmark[8]

                w_x , w_y = wrist.x , wrist.y 
                i_x , i_y = index.x , index.y 

                prev_x = None
                prev_y = None
                #code from here 19/12/2025

                wist_json = {
                    "wrist_x" : w_x,
                    "wrist_y" : w_y,
                }

                index_json = {
                    "index_x" : i_x,
                    "index_y" : i_y,
                }

        frame = cv2.resize(frame, (1000, 700))
        cv2.imshow("agnik",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cam.release()
    cv2.destroyAllWindows()
            
#main chekcing

if __name__ == "__main__":
    camera()