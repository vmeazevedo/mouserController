import cv2
import numpy as np
import handTracking as htm
import time
import autopy

wCam, hCam = 640, 480
frameR = 90
smoothening = 3
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (28,28,28), 2)

        if fingers[1] == 1 and fingers[2] == 0:

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (28,28,28), cv2.FILLED)
            plocX, plocY = clocX, clocY

        if fingers[1] == 1 and fingers[2] == 1:

            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, "FPS: ", (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (28, 28, 28), 2)
    cv2.putText(img, str(int(fps)), (90, 60), cv2.FONT_HERSHEY_PLAIN, 2, (28, 28, 28), 2)
    cv2.putText(img, "Pressione ESC para fechar a tela.", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (28, 28, 28), 1)

    cv2.imshow("Mouse Controller - Vinicius Azevedo", img)
    if cv2.waitKey(5) & 0xFF == 27:
        break