from ursina import Entity, color

class TrafficLight(Entity):
    def __init__(self, position, lane_name, **kwargs):
        super().__init__(
            model='cube',
            scale=(0.5, 2, 0.5),
            position=position,
            color=color.red,
            **kwargs
        )
        self.lane_name = lane_name
        self.state = "RED"
        
    def update_state(self, state):
        self.state = state
        if state == "GREEN":
            self.color = color.green
        elif state == "YELLOW":
            self.color = color.yellow
        else:
            self.color = color.red
