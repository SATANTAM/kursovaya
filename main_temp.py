import numpy as np
import matplotlib.pyplot as plt
import math


def generate_model(structure_size, center, layers_sizes, layers_p):
    def validate_data():
        if not(isinstance(structure_size, list) and isinstance(center, list) and isinstance(layers_sizes, list) and isinstance(layers_p, list)):
            return False
        if len(structure_size) != 2 or len(center) != 2 or len(layers_sizes) + 1 != len(layers_p):
            return False
        if center[0] > structure_size[0] or center[1] > structure_size[1]:
            return False
        return True

    if not validate_data():
        print("Неправильно введены данные")
        return False

    structure = np.zeros(structure_size)

    structure[center[0]][center[1]] = layers_p[-1]

    false_detections = []

    def p_layer_recur(n_center, r, v):
        cells = []

        # print(n_center)

        for i in range(n_center[0]-1, n_center[0]+2):
            for j in range(n_center[1]-1, n_center[1]+2):
                cells.append([i, j])

        con = 0
        for i, e in enumerate(cells):
            try:
                temp = structure[e[0]][e[1]]
            except IndexError:
                con += 1
                continue

            if structure[e[0]][e[1]] != 0:
                con += 1
                continue

            diff_y = abs(e[0] - center[0])
            diff_x = abs(e[1] - center[1])

            dist = math.sqrt(diff_x**2 + diff_y**2)

            if dist < r + 1:
                structure[e[0]][e[1]] = v
                # print("here", n_center, dist, r+1, cells)
                tt = p_layer_recur([e[0], e[1]], r, v)
                if tt[0]:
                    false_detections.append(tt[1])
            else:
                con += 1
        # print(con)
        if con != 9:
            return True, [n_center[0], n_center[1]]
        else:
            return False, [n_center[0], n_center[1]]


    yy = p_layer_recur(center, layers_sizes[0], layers_p[0])

    if yy[0]:
        false_detections.append(yy[1])
    new_false_detections = []
    for i in false_detections:
        if i not in new_false_detections:
            new_false_detections.append(i)

    for i in new_false_detections:
        structure[i[0]][i[1]] = 400

    figure, axs = plt.subplots(1, 1, figsize=(5, 5))
    p2 = axs.imshow(structure, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
    figure.colorbar(p2)
    figure.show()

generate_model([20, 100], [10, 50], [2, 2], [1000, 500, 100])

# structure_size (rows, columns)