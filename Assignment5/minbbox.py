from qhull_2d import *
from min_bounding_rect import *
import json
import os



def points2Str(corner_points):
    x_center = ((corner_points[0][0] + corner_points[1][0] + corner_points[2][0] + corner_points[3][0]) / 4) / 2592

    y_center = ((corner_points[0][1] + corner_points[1][1] + corner_points[2][1] + corner_points[3][1]) / 4) / 1520

    height_yolo = (corner_points[3][1] - corner_points[1][1]) / 2592

    width_yolo = (corner_points[0][0] - corner_points[2][0]) / 1520

    return f"{x_center}, {y_center}, {height_yolo}, {width_yolo}"

if __name__ == "__main__":

    path_to_json = '/home/ahmet/Desktop/Labels/cornetto_ask_atesi_second/'
    path_to_class = '/home/ahmet/Desktop/Labels/class & bboxes/'
    shapeArr = []

    for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
        with open(f"{path_to_json}{file_name}") as json_file:
            data = json.load(json_file)
            shapes = [data["shapes"][i] for i in range(len(data["shapes"]))]
            shapeArr.append(shapes)
            print(shapes)
            for y in range(len(shapes)):
                if "points" in shapes[y]:
                    xy_points = array(shapes[y]["points"])

                    hull_points = qhull2D(xy_points)

                    # Reverse order of points, to match output from other qhull implementations
                    hull_points = hull_points[::-1]

                    # Find minimum area bounding rectangle
                    (rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)


                    print("Corner points: \n", corner_points[0][0], corner_points[0][1], corner_points[1][0],
                          corner_points[1][1], corner_points[2][0], corner_points[2][1], corner_points[3][0],
                          corner_points[3][1], "\n")


                    for class_name in [file for file in os.listdir(path_to_class) if file.endswith('.txt')]:
                        with open(path_to_class + class_name) as class_file:
                            lines = class_file.readlines()
                            print(shapes[y])
                            print(lines[0][0:len(lines[0]) - 1])
                            if shapes[y]["label"] == lines[0][0:len(lines[0]) - 1]:
                                idx = 1
                            elif shapes[y]["label"] == lines[1][0:len(lines[0]) - 1]:
                                idx = 2

                            with open(f"{file_name.split('.')[0]}.txt", "a") as txt:
                                str1 = ""
                                txt.write(f"{idx} {points2Str(corner_points)}\n")

    # --------------------------------------------------------------------------#


