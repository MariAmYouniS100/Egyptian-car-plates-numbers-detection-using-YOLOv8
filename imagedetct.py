import cv2
import json
from ultralytics import YOLO
from myutil import myformat, car_type_dic
import requests

# Path to the folder containing the frames
folder_path = "plates_images"

# model car type detection
vehicle_type_detector = YOLO("yolov8n.pt")

# model for plate detection
car_Plate_reconizer = YOLO('./models/car_Plate_reconizer.pt')

# model for plate finding
license_plate_detector = YOLO('./models/license_plate_detector.pt')

# Classes names of car types
vehicles = [2, 3, 5, 7]  # 2 >> car , 3 >> motorbike , 5 >> bus , 7 >> truck else skip

# final results
results_list = []

cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Capture a single frame
ret, frame = cap.read()
cv2.imshow("Webcam", frame)
# Check if the frame is captured successfully
if not ret:
    print("Error: Could not capture frame")
    exit()

# Here, you can directly send the 'frame' variable to your model for further processing
# For example:
# model.process_frame(frame)

# Release the camera
# frame_no = int(os.path.splitext(file_name)[0])

# Read the frame
# frame_path = os.path.join(folder_path, file_name)
# frame = cv2.imread(frame_path)

# Perform vehicle type detection on the frame and get the results
car_type_results = vehicle_type_detector(frame)
counter = 1
# Process the results
frame_results = {"frame_no": counter, "car_type": None, "numbers": None, "chars": None}
counter = counter + 1
for i, r in enumerate(car_type_results):
    for index, box in enumerate(r.boxes):
        car_type_id = int(box.cls.item())
        # Get the class name
        if car_type_id in vehicles:
            car_type = car_type_id
            car_type = car_type_dic.get(car_type, "Unknown")
            frame_results["car_type"] = car_type
            break

# detect license plates
license_plates = license_plate_detector(frame)[0]
for license_plate in license_plates.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = license_plate
    # crop license plate
    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

    # Perform plate detection model on the frame and get the results
    cv2.imshow('im', license_plate_crop)
    cv2.waitKey()
    results = car_Plate_reconizer(license_plate_crop)
    if results is not None:
        nums, chars = myformat(results)
        frame_results["numbers"] = nums
        frame_results["chars"] = chars


results_list.append(frame_results)


# Save the results in JSON format
json_results = json.dumps(results_list, ensure_ascii=False, indent=4)
with open("results_injson_frame_info_tracker.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_results)

# Send JSON file to  server
# r = requests.post('https://reqbin.com/echo/post/json', json=json_file)
