from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path="yolov8n.pt"):
        # Load the YOLOv8 model (nano for ~20 FPS on CPU)
        self.model = YOLO(model_path)
        # COCO classes: 2: car, 3: motorcycle, 5: bus, 7: truck
        self.target_classes = [2, 3, 5, 7]
        
    def detect(self, frame):
        # Run YOLO inference
        results = self.model(frame, classes=self.target_classes, verbose=False)
        
        detections = []
        if len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                # Bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Append detection info
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'class': cls,
                    'confidence': conf,
                    'center': ((x1 + x2) // 2, (y1 + y2) // 2)
                })
                
        return detections
