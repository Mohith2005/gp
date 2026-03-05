class LaneDetector:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mid_x = 0
        self.mid_y = 0

    def set_frame_dimensions(self, width, height):
        self.width = width
        self.height = height
        self.mid_x = width // 2
        self.mid_y = height // 2

    def get_lane(self, center_point):
        cx, cy = center_point
        # Top-left -> lane1, Top-right -> lane2, Bottom-left -> lane3, Bottom-right -> lane4
        if cx < self.mid_x and cy < self.mid_y:
            return "lane1"
        elif cx >= self.mid_x and cy < self.mid_y:
            return "lane2"
        elif cx < self.mid_x and cy >= self.mid_y:
            return "lane3"
        else:
            return "lane4"
