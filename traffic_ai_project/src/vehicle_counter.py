class VehicleCounter:
    def __init__(self):
        self.lane_counts = {
            "lane1": 0,
            "lane2": 0,
            "lane3": 0,
            "lane4": 0
        }
        self.emergency_lanes = {
            "lane1": False,
            "lane2": False,
            "lane3": False,
            "lane4": False
        }

    def reset_counts(self):
        for key in self.lane_counts:
            self.lane_counts[key] = 0
            self.emergency_lanes[key] = False

    def update_counts(self, detections, lane_detector):
        self.reset_counts()
        for det in detections:
            lane = lane_detector.get_lane(det['center'])
            self.lane_counts[lane] += 1
            if det.get('is_emergency', False):
                self.emergency_lanes[lane] = True
                
        return self.lane_counts, self.emergency_lanes
