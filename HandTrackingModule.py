import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,complexity=1,detectionCon=0.5,minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon=detectionCon
        self.minTrackCon=minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    if draw:
                        self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNum=0, draw = True):
        landmarkList = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNum]
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(w * lm.x), int(h * lm.y)
                landmarkList.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),10,(0,0,255),cv.FILLED)
        return landmarkList
def main():
    cTime = 0
    pTime = 0
    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])



        cTime = time.time()
        fps = 1 // (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv.imshow("Image", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()