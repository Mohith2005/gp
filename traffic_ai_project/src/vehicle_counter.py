class VehicleCounter:
    def __init__(self):
        self.lane_counts = {
            "lane1": 0,
            "lane2": 0,
            "lane3": 0,
            "lane4": 0
        }

    def reset_counts(self):
        for key in self.lane_counts:
            self.lane_counts[key] = 0

    def update_counts(self, detections, lane_detector):
        self.reset_counts()
        for det in detections:
            lane = lane_detector.get_lane(det['center'])
            self.lane_counts[lane] += 1
        return self.lane_counts
