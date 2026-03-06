import time

class SignalController:
    def __init__(self, base_time=5, yellow_time=3):
        self.base_time = base_time
        self.yellow_time = yellow_time
        self.active_green_lane = "lane1"
        # States can be: GREEN, YELLOW, RED
        self.signal_state = {
            "lane1": "GREEN",
            "lane2": "RED",
            "lane3": "RED",
            "lane4": "RED"
        }
        self.last_switch_time = time.time()
        self.current_phase_duration = self.base_time
        
        # internal tracking 
        self.is_yellow_phase = False
        self.next_green_lane = "lane1"
        self.lanes = ["lane1", "lane2", "lane3", "lane4"]

        # To avoid flipping back and forth immediately if emergency vehicle is present for long
        self.emergency_override_active = False

    def update(self, lane_counts, emergency_lanes):
        current_time = time.time()
        elapsed = current_time - self.last_switch_time
        time_remaining = max(0, self.current_phase_duration - elapsed)
        
        # 1. Check for Emergency Vehicles (Priority Override)
        target_emergency_lane = None
        for lane, has_emergency in emergency_lanes.items():
            if has_emergency:
                target_emergency_lane = lane
                break
                
        if target_emergency_lane:
            # If we are already green for this lane, just hold it
            if self.active_green_lane == target_emergency_lane and not self.is_yellow_phase:
                self.emergency_override_active = True
                self.last_switch_time = current_time # Reset timer to hold GREEN
                time_remaining = self.base_time
                return self.active_green_lane, self.signal_state, time_remaining
            # If not green, force a yellow transition immediately (if not already yellowing)
            elif self.active_green_lane != target_emergency_lane and not self.is_yellow_phase:
                self.emergency_override_active = True
                self.is_yellow_phase = True
                self.next_green_lane = target_emergency_lane
                self.signal_state[self.active_green_lane] = "YELLOW"
                self.last_switch_time = current_time
                self.current_phase_duration = self.yellow_time
                time_remaining = self.yellow_time
                return self.active_green_lane, self.signal_state, time_remaining
                
        else:
            self.emergency_override_active = False

        # 2. Normal Timing Logic (Triggered when current phase expires)
        if elapsed >= self.current_phase_duration:
            
            # If we just finished a YELLOW phase, we now switch to GREEN for the next lane
            if self.is_yellow_phase:
                self.is_yellow_phase = False
                self.active_green_lane = self.next_green_lane
                
                # Determine how long the new GREEN phase should be
                vehicle_count = lane_counts.get(self.active_green_lane, 0)
                self.current_phase_duration = self.base_time + vehicle_count
                
                # Update lights
                for lane in self.lanes:
                    if lane == self.active_green_lane:
                        self.signal_state[lane] = "GREEN"
                    else:
                        self.signal_state[lane] = "RED"
                        
            # If we just finished a GREEN phase, we switch to YELLOW
            else:
                self.is_yellow_phase = True
                
                # Determine the *next* lane to get green
                if not self.emergency_override_active:
                    max_lane = max(lane_counts, key=lane_counts.get)
                    max_count = lane_counts[max_lane]
                    
                    if max_count == 0:
                        idx = self.lanes.index(self.active_green_lane)
                        self.next_green_lane = self.lanes[(idx + 1) % 4]
                    else:
                        self.next_green_lane = max_lane
                
                self.signal_state[self.active_green_lane] = "YELLOW"
                self.current_phase_duration = self.yellow_time
            
            self.last_switch_time = current_time
            time_remaining = self.current_phase_duration

        return self.active_green_lane, self.signal_state, time_remaining
