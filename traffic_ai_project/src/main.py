import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import time
import multiprocessing
import traceback

from src.vehicle_detection import VehicleDetector
from src.lane_detection import LaneDetector
from src.vehicle_counter import VehicleCounter
from src.signal_controller import SignalController
from utils.visualization import draw_lanes, draw_detections, draw_info

def run_simulation(state_dict):
    try:
        from simulation.traffic_scene import start_simulation
        start_simulation(state_dict)
    except Exception as e:
        print("Simulation error:", e)
        traceback.print_exc()

def main():
    print("Starting Live Traffic Management System...")
    
    # 1. Configuration for Live Video Input
    # 0 = Default webcam, 1 = external, or use RTSP stream string
    video_source = 0 
    
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    # 2. Initialize AI Modules
    detector = VehicleDetector(model_path="yolov8n.pt")
    lane_detector = LaneDetector()
    counter = VehicleCounter()
    controller = SignalController(base_time=5)

    # 3. Setup IPC for Simulation
    manager = multiprocessing.Manager()
    state_dict = manager.dict()
    state_dict['signal_state'] = {
        "lane1": "GREEN", "lane2": "RED", "lane3": "RED", "lane4": "RED"
    }

    # Start 3D Simulation Process
    sim_process = multiprocessing.Process(target=run_simulation, args=(state_dict,))
    sim_process.start()

    # 4. Main Detection Loop
    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame or stream ended")
            break

        # Resize for processing speed and consistent lane layout
        frame = cv2.resize(frame, (800, 600))
        h, w = frame.shape[:2]
        
        # Initialize lane dimensions once
        if lane_detector.width == 0:
            lane_detector.set_frame_dimensions(w, h)

        # FPS calculation
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
        prev_frame_time = new_frame_time

        # 4a. Detection
        detections = detector.detect(frame)

        # 4b. Counting
        lane_counts = counter.update_counts(detections, lane_detector)

        # 4c. Signal Control
        active_lane, signal_state, time_remaining = controller.update(lane_counts)

        # Update Shared State for 3D Simulation Sync
        state_dict['signal_state'] = signal_state

        # 4d. UI Overlay
        draw_lanes(frame, lane_detector)
        draw_detections(frame, detections)
        draw_info(frame, lane_counts, active_lane, signal_state, fps, time_remaining)

        # Render OpenCV
        cv2.imshow("Live Traffic Detection", frame)

        # Exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    if sim_process.is_alive():
        sim_process.terminate()
        sim_process.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
