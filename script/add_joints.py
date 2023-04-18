import numpy as np
import omni.usd
from pxr import Gf, UsdGeom

# get the stage
stage = omni.usd.get_context().get_stage()

# get wheel transform
wheel_prim = stage.GetPrimAtPath('/World/wheel_combo_04/MASTER/Wheel')

# get wheel transform
wheel_mat = UsdGeom.Xformable(wheel_prim).ComputeLocalToWorldTransform(0)
wheel_translate = wheel_mat.ExtractTranslation()

pod_idx = "{:02d}".format(1)
pod_path = f'/World/wheel_combo_04/MASTER/pods/Pod_{pod_idx}'
pod_prim = stage.GetPrimAtPath(pod_path)
pod_mat = UsdGeom.Xformable(pod_prim).ComputeLocalToWorldTransform(0)
pod_translate = pod_mat.ExtractTranslation()

distance = np.sqrt((pod_translate[0] - wheel_translate[0])**2 + (pod_translate[1] - wheel_translate[1])**2)
z_offset = pod_translate[2] - wheel_translate[2]

print("Distance: ", distance)
print("Z offset: ", z_offset)

# get next pod and dulicate it
next_pod_idx = "{:02d}".format(int(pod_idx) + 1)
next_pod_path = f'/World/wheel_combo_04/MASTER/pods/Pod_{next_pod_idx}'
next_pod_prim = stage.GetPrimAtPath(next_pod_path)
omni.usd.duplicate_prim(stage, pod_path, next_pod_path, False)
print("pod_path: ", pod_path)
print("next_pod_path: ", next_pod_path)

next_pod_translate = wheel_translate +  Gf.Vec3d(0, 0, z_offset)\
    # Gf.Vec3d(distance * np.sin(np.pi/6 * int(next_pod_idx)), distance * np.cos(np.pi/6 * int(next_pod_idx)), 0) + \

UsdGeom.Xformable(next_pod_prim).GetWorldPositionAttr().Set(next_pod_translate)