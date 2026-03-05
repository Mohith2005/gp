# Edge-Based Traffic Congestion Management

An intermediate-level AI project that uses YOLOv8 for vehicle detection and an adaptive signal control algorithm to manage traffic congestion. Includes a live 3D visualization of the traffic intersection using Ursina.

## Features
- **Live Video Input**: Supports laptop webcams, USB cameras, and IP/CCTV streams.
- **Real-Time Detection**: YOLOv8n optimized for CPU inference (~20 FPS).
- **Lane Segmentation**: Divides video feed into 4 virtual lanes.
- **Adaptive Signals**: Assigns GREEN light based on lane vehicle density.
- **3D Traffic Simulation**: Visualizes traffic lights and moving cars in a synchronized 3D space.

## Installation
1. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Python path settings (if running from main directory root):
   Ensure your Python execution can locate the `src` and `simulation` packages, typically run the program from the `traffic_ai_project` root folder.

## Usage
Run the main script:
```bash
python src/main.py
```
Two windows will open:
1. **Live Traffic Detection**: OpenCV window displaying YOLO bounding boxes, lane areas, and current metrics (FPS, active lane, vehicle counts).
2. **3D Traffic Simulation**: Ursina engine window visualizing real-time traffic light states synced with the AI model. Cars will spawn and respect the traffic light logic.

Press `q` within the OpenCV window to exit cleanly.
