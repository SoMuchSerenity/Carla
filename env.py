import carla
import os
import numpy as np
import cv2
import math

class CarEnv:

    def __init__(self):
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.load_world('Town01')
        self.blueprint_library = self.world.get_blueprint_library()
        self.vehicle_bp = self.blueprint_library.find('vehicle.audi.tt')

    @staticmethod
    def img_process(image):
        """

        :param image:
        """
        data = np.array(image.raw_data)
        data = data.reshape((1920, 1080, 4))
        data = data[:, :, :, 3]
        cv2.imshow('', data)
        return data/255.0

    def collision(self, event):
        self.collision.append(event)

    def reward(self, cur_dis):
        pass


    def reset(self):
        self.collision = []
        self.actor_list = []
        self.transform = self.world.get_map().get_spawn_points()[0]
        self.vehicle = self.world.spawn_actor(self.vehicle_bp, self.transform)
        self.actor_list.append(self.vehicle)

        self.col_bp = self.blueprint_library.find('sensor.other.collision')
        self.col_location = carla.Location(0, 0, 0)
        self.col_transform = carla.Transform(self.col_location)
        self.colsensor = self.world.spawn_actor(self.col_bp, self.col_transform, attach_to=self.vehicle)
        self.actor_list.append(self.colsensor)
        self.colsensor.listen(lambda event: self.collision)

        self.cam_bp = self.blueprint_library.find('sensor.camera.rgb')
        self.cam_bp.set_attribute("image_size_x", str(1920))
        self.cam_bp.set_attribute("image_size_y", str(1080))
        self.cam_bp.set_attribute("fov", str(105))
        self.cam_location = carla.Location(0.8, 0, 1.7)
        self.cam_transform = carla.Transform(self.cam_location)
        self.cam_rgb = self.world.spawn_actor(self.cam_bp, self.cam_transform, attach_to=self.vehicle,
                                              attachment_type=carla.AttachmentType.Rigid)
        self.actor_list.append(self.cam_rgb)
        if not os.path.exists(os.path.join(os.getcwd(), 'Data/RGB')):
            os.makedirs(os.path.join(os.getcwd(), 'Data/RGB'))
        self.cam_rgb.listen(
            lambda image: image.save_to_disk(os.path.join(os.getcwd(), 'Data/RGB/%.6d.jpg') % image.frame))

        self.target_transform = self.world.get_map().get_spawn_points()[1]

        self.target_dis = self.target_transform.location.distance(self.vehicle.get_location())

    def step(self, action):
        cur_dis = self.target_dis

        self.vehicle.apply_control(carla.VehicleControl(throttle=action[0], steer=action[1], brake=action[2]))
        self.target_dis = self.target_transform.location.distance(self.vehicle.get_location())
        v = self.vehicle.get_velocity()
        kmh = int(3.6 * math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2))

        self.reward(cur_dis)
