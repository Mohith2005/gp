import cv2

def draw_lanes(frame, lane_detector):
    h, w = lane_detector.height, lane_detector.width
    mx, my = lane_detector.mid_x, lane_detector.mid_y
    cv2.line(frame, (mx, 0), (mx, h), (0, 255, 255), 2)
    cv2.line(frame, (0, my), (w, my), (0, 255, 255), 2)
    
    cv2.putText(frame, "Lane 1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Lane 2", (mx + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Lane 3", (50, my + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Lane 4", (mx + 50, my + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def draw_vehicle_boxes(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        is_emergency = det.get('is_emergency', False)
        cls_name = det.get('class_name', str(det['class']))
        
        # Color: Red for emergency, Blue for standard
        color = (0, 0, 255) if is_emergency else (255, 0, 0)
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, det['center'], 5, color, -1)
        
        label = f"{cls_name} {det['confidence']:.2f}"
        cv2.putText(frame, label, (x1, max(y1-10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def display_vehicle_counts(frame, lane_counts):
    y = 50
    # Placing it below the lane labels but clearly on the left side
    for i, (lane, count) in enumerate(lane_counts.items()):
        text = f"{lane.capitalize()} Vehicles: {count}"
        if i == 0: y_pos = 90
        elif i == 1: y_pos = 120
        elif i == 2: y_pos = 150
        else: y_pos = 180
        cv2.putText(frame, text, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def display_signal_state(frame, signal_state):
    y = 220
    for lane, state in signal_state.items():
        if state == "GREEN":
            color = (0, 255, 0)
        elif state == "YELLOW":
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)
            
        text = f"{lane.capitalize()}: {state}"
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        y += 30

def display_emergency_alert(frame, emergency_lanes):
    detected = False
    for lane, has_emergency in emergency_lanes.items():
        if has_emergency:
            detected = True
            text = f"EMERGENCY VEHICLE DETECTED IN {lane.upper()} - PRIORITY SIGNAL ACTIVATED"
            cv2.putText(frame, text, (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Render only the first one to avoid overlapping texts
            break 

def display_fps(frame, fps):
    h, w = frame.shape[:2]
    # Place in top-right corner
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 150, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

def render_visualization(frame, lane_detector, detections, lane_counts, signal_state, emergency_lanes, fps):
    # Consolidate all drawing functions
    draw_lanes(frame, lane_detector)
    draw_vehicle_boxes(frame, detections)
    display_vehicle_counts(frame, lane_counts)
    display_signal_state(frame, signal_state)
    display_emergency_alert(frame, emergency_lanes)
    display_fps(frame, fps)
