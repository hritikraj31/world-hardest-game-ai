import numpy as np


def line_ray_intersection(ray_origin, ray_direction, point1, point2):
    ray_origin = np.array(ray_origin, dtype=np.float)
    ray_direction = np.array(ray_direction, dtype=np.float)
    point1 = np.array(point1, dtype=np.float)
    point2 = np.array(point2, dtype=np.float)

    v1 = ray_origin - point1
    v2 = point2 - point1
    v3 = np.array([-ray_direction[1], ray_direction[0]])
    dot = np.dot(v2, v3)
    if abs(dot) < 0.0000001:
        return [-1, [-1, -1]]
    t1 = np.cross(v2, v1) / dot
    t2 = np.dot(v1, v3) / dot

    if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
        return [t1, ray_origin + t1 * ray_direction]

    return [-1, [-1, -1]]
