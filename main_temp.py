import numpy as np
import matplotlib.pyplot as plt
import math
import random


def generate_model(structure_size, center, layers_sizes, layers_p, sizes_limit_height, sizes_limit_width):
    def validate_data():
        if not(isinstance(structure_size, list) and isinstance(center, list) and isinstance(layers_sizes, list) and isinstance(layers_p, list)):
            return False
        if not(isinstance(sizes_limit_height, list) and isinstance(sizes_limit_width, list)):
            return False
        if len(structure_size) != 2 or len(center) != 2 or len(layers_sizes) + 1 != len(layers_p):
            return False
        if len(sizes_limit_height) != 2 or len(sizes_limit_width) != 2:
            return False
        if center[0] > structure_size[0] or center[1] > structure_size[1]:
            return False
        return True

    if not validate_data():
        print("Неправильно введены данные")
        return False, False, False

    structure = np.zeros(structure_size)

    for i, e in enumerate(structure):
        for j in range(len(e)):
            diff_y = abs(i - center[0])
            diff_x = abs(j - center[1])

            dist = math.sqrt(diff_x ** 2 + diff_y ** 2)

            is_found = False
            for k, c in enumerate(layers_sizes):
                if dist < c:
                    is_found = True
                    structure[i][j] = layers_p[k]
                    break
            if not is_found:
                structure[i][j] = layers_p[-1]

    sizes_width = np.array([random.randint(sizes_limit_width[0], sizes_limit_width[1]) for i in range(structure_size[0])])
    sizes_height = np.array([random.randint(sizes_limit_height[0], sizes_limit_height[1]) for i in range(structure_size[1])])

    return structure, sizes_width, sizes_height


def solve_model(structure, heights):
    N = len(structure)
    M = 5
    T1 = 0.01
    Q = 2

    rho_arr = structure
    h_arr = heights

    T_arr = np.array([T1 * Q ** i for i in range(M)])
    Omega_arr = (2 * np.pi / np.asarray(T_arr))
    mu = 4 * np.pi * 1e-07
    R = np.empty(M, dtype=complex)
    for i in range(M):
        Rc = 1
        for m in (range(N - 1)):
            K = np.sqrt((-1j * Omega_arr[i] * mu) / (rho_arr[m]))
            A = np.sqrt(rho_arr[m] / rho_arr[m + 1])
            B = (np.exp(-2 * K * h_arr[m])) * ((Rc - A) / (Rc + A))
            Rc = (1 + B) / (1 - B)
        R[i] = (Rc)
    rhok_arr = np.empty(M, dtype=float)
    rhok_arr = np.round(((np.abs(R) ** 2) * rho_arr[0]), 2)
    T_arr1 = np.sqrt(T_arr)
    PhT = np.round(np.angle(R) * (180 / np.pi) - 45, 2)

    return rhok_arr, PhT, T_arr1


def main():
    structure, structure_heights, structure_widths = generate_model([100, 100], [50, 50], [10, 30, 40], [1000, 500, 3000, 0], [10, 10], [10, 10])

    figure, axs = plt.subplots(1, 1, figsize=(5, 5))
    p2 = axs.imshow(structure, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
    figure.colorbar(p2)
    plt.show()


if __name__ == "__main__":
    main()
