import cv2
from ultralytics import YOLO
from datetime import datetime

# Character map for license plate recognition
CHARACTER_MAP = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

# Load YOLO models
LICENSE_PLATE_MODEL = YOLO("main/weights/detection.pt")  # Replace with your license plate model
CHARACTER_MODEL = YOLO("main/weights/recognition.pt")    # Replace with your character model

def detect_license_plates():
    """Continuously detects license plates using YOLO models."""
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened!")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Detect license plates in the frame
            license_plates = LICENSE_PLATE_MODEL(frame)
            for plate in license_plates[0].boxes:
                x1, y1, x2, y2 = map(int, plate.xyxy[0])  # Get bounding box coordinates
                cropped_license_plate = frame[y1:y2, x1:x2]

                # Detect characters in the cropped license plate
                characters = CHARACTER_MODEL(cropped_license_plate)

                # Collect detected characters and their x-coordinates
                detected_characters = []
                for char in characters[0].boxes:
                    x1_char, _, _, _ = map(int, char.xyxy[0])
                    character_class = int(char.cls[0])  # Detected character class index
                    detected_characters.append((character_class, x1_char))

                # Sort characters by x-coordinate and build license text
                detected_characters.sort(key=lambda char: char[1])
                license_text = ''.join([CHARACTER_MAP[char[0]] for char in detected_characters])

                yield license_text

    finally:
        cap.release()
        cv2.destroyAllWindows()
