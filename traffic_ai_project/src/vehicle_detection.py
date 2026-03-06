from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path="yolov8n.pt"):
        # Load the YOLOv8 model (nano for ~20 FPS on CPU)
        self.model = YOLO(model_path)
        # COCO classes: 2: car, 3: motorcycle, 5: bus, 7: truck
        self.target_classes = [2, 3, 5, 7]
        
        # We will use 'bus' (5) and 'truck' (7) to act as proxies for emergency vehicles
        # since standard yolov8 nano doesn't have an explicitly trained 'ambulance' class 
        # out of the box. You can swap these with custom models later.
        self.emergency_classes = [5, 7]
        
        self.class_names = {
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck"
        }
        
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
                
                is_emergency = cls in self.emergency_classes
                
                # Append detection info
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'class': cls,
                    'class_name': self.class_names.get(cls, str(cls)),
                    'confidence': conf,
                    'center': ((x1 + x2) // 2, (y1 + y2) // 2),
                    'is_emergency': is_emergency
                })
                
        return detections
