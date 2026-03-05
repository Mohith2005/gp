import time

class SignalController:
    def __init__(self, base_time=5):
        self.base_time = base_time
        self.active_green_lane = "lane1"
        self.signal_state = {
            "lane1": "GREEN",
            "lane2": "RED",
            "lane3": "RED",
            "lane4": "RED"
        }
        self.last_switch_time = time.time()
        self.current_green_duration = self.base_time
        self.lanes = ["lane1", "lane2", "lane3", "lane4"]

    def update(self, lane_counts):
        current_time = time.time()
        elapsed = current_time - self.last_switch_time
        time_remaining = max(0, self.current_green_duration - elapsed)

        # Check if the current green light has expired
        if elapsed >= self.current_green_duration:
            # Find the lane with the highest vehicle count
            max_lane = max(lane_counts, key=lane_counts.get)
            max_count = lane_counts[max_lane]
            
            if max_count == 0:
                 # Default round robin if no cars are detected
                 idx = self.lanes.index(self.active_green_lane)
                 self.active_green_lane = self.lanes[(idx + 1) % 4]
                 vehicle_count = 0
            else:
                 # Assign GREEN to the most congested lane
                 self.active_green_lane = max_lane
                 vehicle_count = max_count

            # green_time = base_time + vehicle_count
            self.current_green_duration = self.base_time + vehicle_count
            self.last_switch_time = current_time
            time_remaining = self.current_green_duration

            # Update signal states
            for lane in self.signal_state:
                if lane == self.active_green_lane:
                    self.signal_state[lane] = "GREEN"
                else:
                    self.signal_state[lane] = "RED"

        return self.active_green_lane, self.signal_state, time_remaining
