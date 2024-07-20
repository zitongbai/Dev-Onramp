import numpy as np
import os
import time

import mujoco
import mujoco.viewer

from dm_control import mjcf

from robot_descriptions import ur5e_mj_description, robotiq_2f85_mj_description

# ###############################################################################
# helper functions
# ###############################################################################
def attach_hand_to_arm(
    arm_mjcf: mjcf.RootElement,
    hand_mjcf: mjcf.RootElement,
) -> None:
  """Attaches a hand to an arm.

  The arm must have a site named "attachment_site".
  
  https://github.com/google-deepmind/mujoco_menagerie/blob/main/FAQ.md#how-do-i-attach-a-hand-to-an-arm

  Args:
    arm_mjcf: The mjcf.RootElement of the arm.
    hand_mjcf: The mjcf.RootElement of the hand.

  Raises:
    ValueError: If the arm does not have a site named "attachment_site".
  """
  physics = mjcf.Physics.from_mjcf_model(hand_mjcf)

  attachment_site = arm_mjcf.find("site", "attachment_site")
  if attachment_site is None:
    raise ValueError("No attachment site found in the arm model.")

  # Expand the ctrl and qpos keyframes to account for the new hand DoFs.
  arm_key = arm_mjcf.find("key", "home")
  if arm_key is not None:    
    hand_key = hand_mjcf.find("key", "home")
    if hand_key is None:
      arm_key.ctrl = np.concatenate([arm_key.ctrl, np.zeros(physics.model.nu)])
      arm_key.qpos = np.concatenate([arm_key.qpos, np.zeros(physics.model.nq)])
    else:
      arm_key.ctrl = np.concatenate([arm_key.ctrl, hand_key.ctrl])
      arm_key.qpos = np.concatenate([arm_key.qpos, hand_key.qpos])

  attachment_site.attach(hand_mjcf)

def add_box(
    parent : mjcf.RootElement, 
    body_size = [0.02, 0.02, 0.02],
    pos = [0.5, 0.0, 0.03],
    euler = [0, 0, 0],
  ):
  """add a box in the scene

  Args:
      parent (mjcf.RootElement): the parent element to attach the box to
      body_size (list, optional): box size. Defaults to [0.03, 0.03, 0.03].
      pos (list, optional): box position. Defaults to [0.5, 0.0, 0.03].
      euler (list, optional): box orientation. Defaults to [0, 0, 0].
  """
  name = f"box_{hash(time.time())}"
  body = parent.worldbody.add('body', name=name)
  
  box_rgb = [0.8, 0.1, 0.1]
  box_rgba = np.append(box_rgb, 1.0)
  body.add('freejoint')
  body.add('geom', name='mybox', size=body_size, type='box', rgba=box_rgba)
  
  # expand the qpos in keyframes
  keys = parent.find_all('key')
  for key in keys:
    quat = np.zeros(4)
    mujoco.mju_euler2Quat(quat, euler, 'xyz')
    q = np.concatenate([pos, quat])
    key.qpos = np.concatenate([key.qpos, q])

# ###############################################################################
# mujoco scene
# ###############################################################################

scene = mjcf.RootElement()
scene.asset.add('texture', type="skybox", builtin="gradient", rgb1="0.8 0.8 0.8", rgb2="0 0 0", width="32", height="512")
scene.asset.add('texture', type="2d", name="groundplane", builtin="checker", mark="edge", rgb1="0.2 0.3 0.4", rgb2="0.1 0.2 0.3", markrgb="1 1 1", width="300", height="300")
scene.asset.add('material', name="groundplane", texture="groundplane", texuniform="true", texrepeat="5 5", reflectance="0.2")

scene.worldbody.add('light', pos="0 0 1")
scene.worldbody.add('light', pos="0 -0.2 1", dir="0 0.2 -0.8", directional="true")
scene.worldbody.add('geom', name='floor', size="0 0 0.05", type='plane', material='groundplane')

# camera
# https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-camera 
scene.worldbody.add('camera', name='sideview', pos="-0.3 0.5 0.2", xyaxes="-0.5 -0.8 0 0.1 -0.1 1")

# ###############################################################################
# robot arm and hand
# ###############################################################################

# load robot arm and hand
arm_mjcf = mjcf.from_path(ur5e_mj_description.MJCF_PATH)
hand_mjcf = mjcf.from_path(robotiq_2f85_mj_description.MJCF_PATH)

joint_names = []
joints = arm_mjcf.worldbody.find_all('joint')
for joint in joints:
  joint_names.append(joint.name)

# change the actuator type of the robot arm
del arm_mjcf.actuator
motor_class = arm_mjcf.default.add('default', dclass='motor')
motor_class.motor.set_attributes(ctrlrange='-1000 1000')
for jnt_name in joint_names:
  # add motor actuator
  arm_mjcf.actuator.add('motor', dclass='motor', name= jnt_name+'_motor', joint=jnt_name)
  
for jnt_name in joint_names:
  # add position sensor
  arm_mjcf.sensor.add('jointpos', name=jnt_name+'_pos', joint=jnt_name)
for jnt_name in joint_names:
  # add velocity sensor
  arm_mjcf.sensor.add('jointvel', name=jnt_name+'_vel', joint=jnt_name)
  
# add end effector site to hand 
base_mount = hand_mjcf.find("body", "base_mount")
base_mount.add('site', name='end_effector', pos="0 0 0.15")

base_mount.add('camera', name='ee_view', pos="0 -0.05 0", xyaxes="1 0 0 0 -1 0")

# attach hand to arm 
attach_hand_to_arm(arm_mjcf, hand_mjcf)

# attach arm to scene
fixed_base_site = scene.worldbody.add('site', name='fixed_base_site', pos="0 0 0", euler="0 0 0")
fixed_base_site.attach(arm_mjcf)

# add box
add_box(scene, pos = [0.5, 0.1, 0.03], euler = [0, 0, 0])

# export
out_dir = "ur5e_with_robotiq_2f85"
out_file = "ur5e_with_robotiq_2f85.xml"
# delete existing files
if os.path.exists(out_dir):
  os.system(f"rm -rf {out_dir}")
# export
mjcf.export_with_assets(scene, out_dir, out_file)
print(f"Exported to {out_dir}/{out_file}")