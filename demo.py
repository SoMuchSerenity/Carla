import carla
import random
import time
import os

# A list to store actors, which will be destroyed at the end
actor_list = []

try:
    # Connect the client to the server at port 2000
    client = carla.Client('localhost', 2000)
    # Set timeout to limit the networking operations so that the these don't block the client forever.
    # An error will be returned if connection fails.
    client.set_timeout(10.0)
    # Available maps are Town 01,02,03,04,05,06,07,10
    #    world = client.get_world()
    print(client.get_available_maps())
    #    world = client.get_world()
    world = client.load_world('Town01')

    '''
    TODO: Apply synchronous mode
    '''
    # settings = world.get_settings()
    # settings.synchronous_mode = True
    # settings.fixed_delta_seconds = 0.05
    # world.apply_settings(settings)

    '''
    No-rendering mode
    '''
    # settings = world.get_settings()
    # settings.no_rendering_mode = True
    # world.apply_settings(settings)


    # Get blueprint library, which contains all actors and their attributes.
    blueprint_library = world.get_blueprint_library()
    # Here we choose Audi TT
    vehicle_bp = blueprint_library.find('vehicle.audi.tt')
    vehicle_bp.set_attribute('role_name', 'ego')
    # Get spawn point using carla's built in functions.
    spawn_point = random.choice(world.get_map().get_spawn_points())
    # Spawn the vehicle

    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    # Remember to add the vehicle to actor list for the convenience of destroying them later on
    actor_list.append(vehicle)

    '''
    Conveniently locating the vehicle 
    '''
    spectator = world.get_spectator()
    world_snapshot = world.wait_for_tick()
    spectator.set_transform(vehicle.get_transform())

    '''
    RGB camera
    '''

    cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    cam_bp.set_attribute("image_size_x", str(1920))
    cam_bp.set_attribute("image_size_y", str(1080))
    cam_bp.set_attribute("fov", str(105))
    cam_location = carla.Location(0.8, 0, 1.7)
    cam_transform = carla.Transform(cam_location)
    cam_rgb = world.spawn_actor(cam_bp, cam_transform, attach_to=vehicle,
                                attachment_type=carla.AttachmentType.Rigid)
    actor_list.append(cam_rgb)
    if not os.path.exists(os.path.join(os.getcwd(), 'Data/RGB')):
        os.makedirs(os.path.join(os.getcwd(), 'Data/RGB'))
    cam_rgb.listen(lambda image: image.save_to_disk(os.path.join(os.getcwd(), 'Data/RGB/%.6d.jpg') % image.frame))

    '''
    Semantic Segmentation camera
    '''

#     cam_ss_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
#     cam_ss_bp.set_attribute("image_size_x", str(1920))
#     cam_ss_bp.set_attribute("image_size_y", str(1080))
#     cam_ss_bp.set_attribute("fov", str(105))
# #    cam_ss_bp.set_attribute('sensor_tick', '1.0')
#     cam_ss_location = carla.Location(0.8, 0, 1.7)
#     cam_ss_transform = carla.Transform(cam_ss_location)
#     cam_ss = world.spawn_actor(cam_ss_bp, cam_ss_transform, attach_to=vehicle,
#                                attachment_type=carla.AttachmentType.Rigid)
#     actor_list.append(cam_ss)
#     if not os.path.exists(os.path.join(os.getcwd(), 'Data/SS')):
#         os.makedirs(os.path.join(os.getcwd(), 'Data/SS'))
#     cam_ss.listen(lambda image: image.save_to_disk(os.path.join(os.getcwd(), 'Data/SS/%.6d.jpg') % image.frame,
#                                                     carla.ColorConverter.CityScapesPalette))

    '''
    Depth camera
    '''

    # depth_bp = world.get_blueprint_library().find('sensor.camera.depth')
    # depth_bp.set_attribute("image_size_x", str(1920))
    # depth_bp.set_attribute("image_size_y", str(1080))
    # depth_bp.set_attribute("fov", str(105))
    # depth_location = carla.Location(0.8, 0, 1.7)
    # depth_transform = carla.Transform(depth_location)
    # depth_cam = world.spawn_actor(depth_bp, depth_transform, attach_to=vehicle,
    #                               attachment_type=carla.AttachmentType.Rigid)
    # actor_list.append(depth_cam)
    # if not os.path.exists(os.path.join(os.getcwd(), 'Data/Depth')):
    #     os.makedirs(os.path.join(os.getcwd(), 'Data/Depth'))
    #
    # depth_cam.listen(lambda image: image.save_to_disk(os.path.join(os.getcwd(), 'Data/Depth/%.6d.jpg') % image.frame,
    #                                                   carla.ColorConverter.LogarithmicDepth))
    #
    # Simple and straight control applied to vehicle.
    vehicle.apply_control(carla.VehicleControl(throttle=0.7, steer=0))
    time.sleep(10)
finally:
    for actor in actor_list:
        actor.destroy()

    print('End')
