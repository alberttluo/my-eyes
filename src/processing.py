import cv2
import pickle
import torch
import os
import time
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from heapq import heapify, heappop, heappush, nlargest


q = {
    "person", "bicycle", "motorcycle", "bus", "truck", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "chair", 
    "couch", "potted plant", "bed", "dining table", "toilet", 
    "refrigerator", "book", "clock", "vase", "teddy bear"
}

model = YOLO("yolov8n.pt")

def priority(area, object):
    return 0.4 * area + 0.6 * (int(object in q))

## for frame-by-frame input:
def process(image_path):
    image = cv2.imread(image_path)

    results = model(image)

    detected = set()

    heap = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            detected.add(f"{model.names[cls]}")
            cv2.rectangle(image, (x1, y1), (x2, y2), 255, 2)
            area = abs((x1 - x2) * (y1 - y2))
            cv2.putText(image, f"area: {area/100000}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            p = priority(area, model.names[cls])
            heappush(heap, p)

    print(f"detected the following items: {detected}\n")
    print(f"top priority objects: {list(heap[:3])}")
    time.sleep(1)
    cv2.destroyAllWindows()

    ## for video input:

    # # Open the video file
    # video_path = "/Users/albertluo/Desktop/edu/cmu/my-eyes/random-test-stuff/People Walking Free Stock Footage, Royalty-Free No Copyright Content 720.mp4"
    # cap = cv2.VideoCapture(video_path)

    # # Get video properties
    # frame_width = int(cap.get(3))
    # frame_height = int(cap.get(4))
    # fps = int(cap.get(cv2.CAP_PROP_FPS))

    # # Define the codec and create VideoWriter to save output
    # out = cv2.VideoWriter("random_people_walking_output_video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # # Process video frame by frame
    # while cap.isOpened():
    #     success, frame = cap.read()
    #     if not success:
    #         break  # Break if video ends

    #     # Run YOLO on the frame
    #     results = model(frame)

    #     # Draw bounding boxes
    #     for result in results:
    #         for box in result.boxes:
    #             x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
    #             conf = box.conf[0].item()  # Confidence score
    #             cls = int(box.cls[0])  # Class index
    #             label = f"{model.names[cls]} {conf:.2f}"

    #             # Draw rectangle and label
    #             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #             cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    #     # Write the frame to output video
    #     out.write(frame)

    #     # Display the frame (optional)
    #     cv2.imshow("YOLO Video", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit early
    #         break

    # # Release resources
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()

def __main__():
    for root, _, files in os.walk('/Users/albertluo/Desktop/edu/cmu/my-eyes/server_myeyes/uploads'):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Extracted: {filename} from {root}")
            process(file_path)

while True:
    __main__()