import cv2
import dlib
import numpy as np
import imutils

# Load the pre-trained facial landmarks model
landmark_model_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(landmark_model_path)

def extract_landmarks(image_path):
    # Read the image
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=600)

    if image is None:
        print("Hello")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = detector(gray)
    if len(faces) == 0:
        print("No faces detected!")
        return None

    # Assume the first face detected is the target face
    landmarks = predictor(gray, faces[0])

    # Extract (x, y) coordinates of the landmarks
    points = []
    for n in range(68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        points.append((x, y))

    return points

def compute_features(front_landmarks, side_landmarks=None):
    # Cheek-to-Jaw Width Ratio (CJWR)
    jaw_width = np.linalg.norm(np.array(front_landmarks[3]) - np.array(front_landmarks[13]))
    cheek_width = np.linalg.norm(np.array(front_landmarks[1]) - np.array(front_landmarks[15]))
    cjwr = cheek_width / jaw_width

    # Width to Upper Facial Height Ratio (WHR)
    width = np.linalg.norm(np.array(front_landmarks[1]) - np.array(front_landmarks[15]))
    upper_height = np.linalg.norm(np.array(front_landmarks[27]) - np.array(front_landmarks[8]))
    whr = width / upper_height

    # Perimeter to Area Ratio (PAR)
    contour_points = np.array(front_landmarks[:17])  # Jawline points
    perimeter = cv2.arcLength(contour_points, True)
    area = cv2.contourArea(contour_points)
    par = perimeter / area if area != 0 else None

    # Eye Size (ES)
    left_eye_width = np.linalg.norm(np.array(front_landmarks[36]) - np.array(front_landmarks[39]))
    left_eye_height = np.linalg.norm(np.array(front_landmarks[37]) - np.array(front_landmarks[41]))
    right_eye_width = np.linalg.norm(np.array(front_landmarks[42]) - np.array(front_landmarks[45]))
    right_eye_height = np.linalg.norm(np.array(front_landmarks[43]) - np.array(front_landmarks[47]))
    es = ((left_eye_width * left_eye_height) + (right_eye_width * right_eye_height)) / 2

    # Lower Face to Face Height Ratio (FW/FH)
    lower_face_height = np.linalg.norm(np.array(front_landmarks[33]) - np.array(front_landmarks[8]))
    face_height = np.linalg.norm(np.array(front_landmarks[27]) - np.array(front_landmarks[8]))
    fw_fh = lower_face_height / face_height

    # Mean Eyebrow Height (MEH)
    left_eyebrow_mean_height = np.mean([np.linalg.norm(np.array(front_landmarks[19]) - np.array(front_landmarks[37])),
                                        np.linalg.norm(np.array(front_landmarks[20]) - np.array(front_landmarks[38]))])
    right_eyebrow_mean_height = np.mean([np.linalg.norm(np.array(front_landmarks[23]) - np.array(front_landmarks[43])),
                                         np.linalg.norm(np.array(front_landmarks[24]) - np.array(front_landmarks[44]))])
    meh = (left_eyebrow_mean_height + right_eyebrow_mean_height) / 2

    return {
        "CJWR": cjwr,
        "WHR": whr,
        "PAR": par,
        "ES": es,
        "FW/FH": fw_fh,
        "MEH": meh
    }

# Example usage
front_photo_path = "A00147_front.jpg"
side_photo_path = "A00147_side.jpg"  # Optional for advanced features

front_landmarks = extract_landmarks(front_photo_path)
if front_landmarks:
    features = compute_features(front_landmarks)
    print("Computed Facial Features:")
    for key, value in features.items():
        print(f"{key}: {value}")
