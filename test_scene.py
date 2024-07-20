import time
import numpy as np

import cv2

import mujoco
import mujoco.viewer

xml_path = "ur5e_with_robotiq_2f85/ur5e_with_robotiq_2f85.xml"
model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model)

mujoco.mj_resetDataKeyframe(model, data, 0)


with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()
    
    # set viewing camera
    mujoco.mjv_defaultFreeCamera(model, viewer.cam)
    viewer.cam.distance = 1.2
    viewer.cam.elevation = -15
    viewer.cam.azimuth = 70
    viewer.cam.lookat = (0.3, 0, .3)
    
    
    while viewer.is_running():
        step_start = time.time()
        
        # data.ctrl[0:6] = data.qpos[0:6]
        
        mujoco.mj_step(model, data)
        
        viewer.sync()
        
        # get camera image
        camera_name = 'ur5e/robotiq_2f85/ee_view'
        renderer.update_scene(data, camera_name)
        frame = renderer.render()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)