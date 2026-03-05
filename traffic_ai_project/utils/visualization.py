import cv2

def draw_lanes(frame, lane_detector):
    h, w = lane_detector.height, lane_detector.width
    mx, my = lane_detector.mid_x, lane_detector.mid_y
    cv2.line(frame, (mx, 0), (mx, h), (0, 255, 255), 2)
    cv2.line(frame, (0, my), (w, my), (0, 255, 255), 2)
    # Put labels
    cv2.putText(frame, "Lane 1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Lane 2", (mx + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Lane 3", (50, my + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Lane 4", (mx + 50, my + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def draw_detections(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, det['center'], 5, (0, 0, 255), -1)

def draw_info(frame, lane_counts, active_lane, signal_state, fps, time_remaining):
    y_offset = 30
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Active Lane: {active_lane} ({time_remaining:.1f}s)", (10, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    y = y_offset + 60
    for lane, count in lane_counts.items():
        state = signal_state.get(lane, "RED")
        color = (0, 255, 0) if state == "GREEN" else (0, 0, 255)
        text = f"{lane}: {count} vehicles - {state}"
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        y += 25
