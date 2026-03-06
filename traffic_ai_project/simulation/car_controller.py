from ursina import Entity, color, Vec3, time, destroy
import random

class CarController:
    def __init__(self):
        self.cars = []
        # Define lane origins, movement vectors, and stop positions
        self.lane_configs = {
            "lane1": {"start": Vec3(1, 0.25, 10), "dir": Vec3(0, 0, -1), "stop_pos": 3, "axis": "z", "sign": 1},
            "lane2": {"start": Vec3(10, 0.25, -1), "dir": Vec3(-1, 0, 0), "stop_pos": 3, "axis": "x", "sign": 1},
            "lane3": {"start": Vec3(-1, 0.25, -10), "dir": Vec3(0, 0, 1), "stop_pos": -3, "axis": "z", "sign": -1},
            "lane4": {"start": Vec3(-10, 0.25, 1), "dir": Vec3(1, 0, 0), "stop_pos": -3, "axis": "x", "sign": -1}
        }
        self.speed = 4

    def spawn_car(self, lane_name):
        cfg = self.lane_configs[lane_name]
        offset = random.uniform(-0.2, 0.2)
        pos = Vec3(cfg["start"])
        if cfg["axis"] == "z": pos.x += offset
        else: pos.z += offset
            
        car = Entity(
            model='cube',
            scale=(0.8, 0.5, 1.6) if cfg["axis"] == "z" else (1.6, 0.5, 0.8),
            color=color.random_color(),
            position=pos
        )
        car.lane = lane_name
        self.cars.append(car)

    def update_cars(self, signal_state):
        to_remove = []
        for car in self.cars:
            cfg = self.lane_configs[car.lane]
            state = signal_state.get(car.lane, "RED")
            
            pos_val = car.position.z if cfg["axis"] == "z" else car.position.x
            dist_to_stop = pos_val * cfg["sign"] - cfg["stop_pos"] * cfg["sign"]
            
            should_stop = False
            # Cars should start braking if they see RED *or* YELLOW ahead if they haven't crossed yet
            stop_condition = state in ["RED", "YELLOW"]
            if stop_condition and 0 < dist_to_stop < 2.5:
                # To prevent cars overlapping
                should_stop = True
                
            # A simple collision avoidance for cars in the same lane
            for other_car in self.cars:
                if other_car != car and other_car.lane == car.lane:
                    other_pos_val = other_car.position.z if cfg["axis"] == "z" else other_car.position.x
                    dist_to_car = pos_val * cfg["sign"] - other_pos_val * cfg["sign"]
                    if 0 < dist_to_car < 2.5:
                        should_stop = True

            if not should_stop:
                car.position += cfg["dir"] * self.speed * time.dt
                
            if abs(car.position.x) > 15 or abs(car.position.z) > 15:
                to_remove.append(car)
                
        for car in to_remove:
            self.cars.remove(car)
            destroy(car)
