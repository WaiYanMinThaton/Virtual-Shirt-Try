import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import os

cap = cv2.VideoCapture(0)
detector = PoseDetector()

# Lấy path của các file image shirt
shirtFolderPath = "Resource/Shirts"
listShirts = os.listdir(shirtFolderPath)

# Các tỉ lệ kích thước giữa file ảnh so với áo trên video
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440

imageNumber = 0   # Index của shirt image hiện tại

# Button image
imgButtonRight = cv2.imread("Resource/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

# Counter khi nhấn button left, right
counterRight = 0
counterLeft = 0

# Tốc độ quyết định khi nhấn chọn bên trái, phải
selectionSpeed = 10

while True:
    success, img = cap.read()
    # Vẽ các landmard pose lên image
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        # Vị trí các landmark để đặt shirt lên
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        # Load shirt image
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        # Điều chỉnh lại kích thước shirt cho vừa khung hình
        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        if widthOfShirt > 0:
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        else:
            print("Invalid shirt width, skipping resize.")

        # imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        # Draw shirt image
        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        # Draw 2 button image
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)

            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)