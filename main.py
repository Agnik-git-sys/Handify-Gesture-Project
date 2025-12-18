import cv2
import mediapipe as mp
import math
import numpy as np

mp_hand = mp.solutions.hands
hands = mp_hand.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


def camera():
    cam = cv2.VideoCapture(0)

    canvas = None
    prev_x = None
    prev_y = None

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1000, 700))
        h, w, _ = frame.shape

        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hand.HAND_CONNECTIONS)

            thumb = hand.landmark[4]
            index = hand.landmark[8]

            ix, iy = int(index.x * w), int(index.y * h)
            tx, ty = int(thumb.x * w), int(thumb.y * h)

            pinch = math.hypot(ix - tx, iy - ty)
            pinch_threshold = 70   # ✅ increased

            # debug
            cv2.circle(frame, (ix, iy), 6, (0, 255, 0), -1)
            cv2.putText(frame, f"Pinch: {int(pinch)}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if pinch < pinch_threshold:
                if prev_x is not None:
                    cv2.line(canvas, (prev_x, prev_y), (ix, iy), (0, 0, 255), 4)
                prev_x, prev_y = ix, iy
            else:
                prev_x, prev_y = None, None

        frame = cv2.addWeighted(frame, 0.6, canvas, 0.4, 0)
        cv2.imshow("agnik", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera()
