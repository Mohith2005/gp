from ursina import Ursina, EditorCamera, Entity, color, window, Vec3
from simulation.traffic_light import TrafficLight
from simulation.car_controller import CarController
import time

def start_simulation(state_dict):
    app = Ursina(development_mode=False)
    window.title = '3D Traffic Simulation'
    window.fps_counter.enabled = False
    
    # Simple road
    Entity(model='plane', scale=(6, 1, 30), color=color.dark_gray)
    Entity(model='plane', scale=(30, 1, 6), color=color.dark_gray)
    
    # Traffic lights
    lights = {
        "lane1": TrafficLight(position=(3.5, 1, 3.5), lane_name="lane1"),
        "lane2": TrafficLight(position=(3.5, 1, -3.5), lane_name="lane2"),
        "lane3": TrafficLight(position=(-3.5, 1, -3.5), lane_name="lane3"),
        "lane4": TrafficLight(position=(-3.5, 1, 3.5), lane_name="lane4")
    }
    
    car_ctrl = CarController()
    
    camera_controller = EditorCamera()
    camera_controller.position = (0, 20, -20)
    camera_controller.look_at((0,0,0))

    last_spawn_time = time.time()

    def update():
        nonlocal last_spawn_time
        
        try:
            signal_state = state_dict.get('signal_state', {
                "lane1": "RED", "lane2": "RED", "lane3": "RED", "lane4": "RED"
            })
        except:
            signal_state = { "lane1": "RED", "lane2": "RED", "lane3": "RED", "lane4": "RED" }

        for lane, light in lights.items():
            light.update_state(signal_state.get(lane, "RED"))
            
        if time.time() - last_spawn_time > 1.2:
            import random
            lanes = ["lane1", "lane2", "lane3", "lane4"]
            # Spawn multiple lanes sometimes for more realistic traffic
            for _ in range(random.randint(1, 2)):
                car_ctrl.spawn_car(random.choice(lanes))
            last_spawn_time = time.time()
            
        car_ctrl.update_cars(signal_state)
        
    app.update = update
    app.run()
