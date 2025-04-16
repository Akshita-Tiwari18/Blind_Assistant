import cv2
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Load YOLO config and weights
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # You can use tiny weights too
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Load classes
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Start webcam
cap = cv2.VideoCapture(0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = int(np.argmax(scores))
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in indexes.flatten():
        label = str(classes[class_ids[i]])
        if label in ['person', 'car', 'bicycle', 'truck', 'motorbike']:
            speak(f"Obstacle ahead: {label}")
            print(f"Detected: {label}")

    # Show camera feed (optional)
    cv2.imshow("Smart Blind Assistant", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
