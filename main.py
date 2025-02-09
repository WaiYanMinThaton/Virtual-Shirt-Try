import cv2
import os
from cvzone.PoseModule import PoseDetector
import cvzone

# Initialize Camera and Pose Detector
def initialize_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    detector = PoseDetector()
    return cap, detector

# Setup Fullscreen Window
def setup_window():
    cv2.namedWindow("Virtual Try-On", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Virtual Try-On", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Load Shirt Images
def load_shirts(folder_path):
    if not os.path.exists(folder_path) or not os.listdir(folder_path):
        print("Error: Shirt folder is empty or does not exist!")
        exit()
    return [f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg", ".jpeg"))]

# Load Button Images
def load_buttons():
    try:
        img_button_right = cv2.imread("Resource/button.png", cv2.IMREAD_UNCHANGED)
        img_button_left = cv2.flip(img_button_right, 1)
        return img_button_right, img_button_left
    except:
        print("Error: Button image not found!")
        return None, None

# Overlay Shirt Image
def overlay_shirt(img, img_shirt, lm11, lm12, offsetX, offsetY, fixedRatio):
    if img_shirt is None:
        return img

    shoulderWidth = abs(lm11[0] - lm12[0])
    shirtWidth = int(shoulderWidth * fixedRatio)
    shirtHeight = int(shirtWidth * 1.3)

    if shirtWidth > 50 and shirtHeight > 50:  # Ensure valid size
        img_shirt = cv2.resize(img_shirt, (shirtWidth, shirtHeight))
        try:
            img = cvzone.overlayPNG(img, img_shirt, (lm12[0] - offsetX, lm11[1] - offsetY))
        except Exception as e:
            print("Overlay error:", e)
    return img

# Process Frame
def process_frame(img, detector, listShirts, imageNumber, img_button_right, img_button_left, fixedRatio):
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if lmList and len(lmList) > 23:
        lm11, lm12 = lmList[11][1:3], lmList[12][1:3]  # Shoulders

        offsetX = int(abs(lm11[0] - lm12[0]) * 0.3)
        offsetY = int(abs(lm11[1] - lm12[1]) * 0.5)  # Adjust vertical offset

        imgShirt = cv2.imread(os.path.join("Resource/Shirts", listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        img = overlay_shirt(img, imgShirt, lm11, lm12, offsetX, offsetY, fixedRatio)

    # Overlay Buttons
    if img_button_right is not None and img_button_left is not None:
        img = cvzone.overlayPNG(img, img_button_right, (1220, 300))  # Right button
        img = cvzone.overlayPNG(img, img_button_left, (50, 300))  # Left button

    return img, lmList

# Handle Shirt Switching
def switch_shirt(lmList, imageNumber, listShirts, counterRight, counterLeft, selectionSpeed):
    if len(lmList) > 16:  # Ensure hand landmarks are detected
        right_hand = lmList[16][1:3]
        left_hand = lmList[15][1:3]

        if right_hand[1] < 150:  # Raise right hand to switch forward
            counterRight += 1
            if counterRight * selectionSpeed > 360 and imageNumber < len(listShirts) - 1:
                counterRight = 0
                imageNumber += 1
        elif left_hand[1] < 150:  # Raise left hand to switch backward
            counterLeft += 1
            if counterLeft * selectionSpeed > 360 and imageNumber > 0:
                counterLeft = 0
                imageNumber -= 1
        else:
            counterRight, counterLeft = 0, 0
    return imageNumber, counterRight, counterLeft

# Main Function
def main():
    global imageNumber, listShirts
    cap, detector = initialize_camera()
    setup_window()
    listShirts = load_shirts("Resource/Shirts")
    img_button_right, img_button_left = load_buttons()

    fixedRatio, imageNumber = 1.2, 0
    counterRight, counterLeft, selectionSpeed = 0, 0, 10

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)  # Mirror the image for natural feel
        img, lmList = process_frame(img, detector, listShirts, imageNumber, img_button_right, img_button_left, fixedRatio)

        if lmList:
            imageNumber, counterRight, counterLeft = switch_shirt(lmList, imageNumber, listShirts, counterRight, counterLeft, selectionSpeed)

        cv2.imshow("Virtual Try-On", img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
