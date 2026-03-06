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
from utils.visualization import render_visualization

def run_simulation(state_dict):
    try:
        from simulation.traffic_scene import start_simulation
        start_simulation(state_dict)
    except Exception as e:
        print("Simulation error:", e)
        traceback.print_exc()

def main():
    print("Starting Live Traffic Management System...")
    
    video_source = 0 
    
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    detector = VehicleDetector()
    lane_detector = LaneDetector()
    counter = VehicleCounter()
    controller = SignalController(base_time=5, yellow_time=3)

    manager = multiprocessing.Manager()
    state_dict = manager.dict()
    state_dict['signal_state'] = {
        "lane1": "GREEN", "lane2": "RED", "lane3": "RED", "lane4": "RED"
    }

    # Start 3D Simulation Process
    sim_process = multiprocessing.Process(target=run_simulation, args=(state_dict,))
    sim_process.start()

    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame or stream ended")
            break

        frame = cv2.resize(frame, (800, 600))
        h, w = frame.shape[:2]
        
        if lane_detector.width == 0:
            lane_detector.set_frame_dimensions(w, h)

        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
        prev_frame_time = new_frame_time

        detections = detector.detect(frame)
        lane_counts, emergency_lanes = counter.update_counts(detections, lane_detector)
        
        active_lane, signal_state, time_remaining = controller.update(lane_counts, emergency_lanes)

        # Update Shared State for 3D Simulation Sync
        state_dict['signal_state'] = signal_state

        # Using our customized rendering engine
        render_visualization(
            frame=frame,
            lane_detector=lane_detector,
            detections=detections,
            lane_counts=lane_counts,
            signal_state=signal_state,
            emergency_lanes=emergency_lanes,
            fps=fps
        )

        cv2.imshow("Live Traffic Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if sim_process.is_alive():
        sim_process.terminate()
        sim_process.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
