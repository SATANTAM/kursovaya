from tkinter import *
from tkinter.ttk import *
import numpy as np
import math
import random
import matplotlib.pyplot as plt


def main():
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
        # rhok_arr = np.abs(R) ** 2 * structure[0]
        rhok_arr = np.round(((np.abs(R) ** 2) * rho_arr[0]), 2)
        T_arr1 = np.sqrt(T_arr)
        PhT = np.round(np.angle(R) * (180 / np.pi) - 45, 2)

        return rhok_arr, PhT, T_arr1

    def generate_model(structure_size, center, layers_sizes, layers_p, sizes_limit_height, sizes_limit_width):
        def validate_data():
            if not (isinstance(structure_size, list) and isinstance(center, list) and isinstance(layers_sizes, list) and isinstance(layers_p, list)):
                return False
            if not (isinstance(sizes_limit_height, list) and isinstance(sizes_limit_width, list)):
                return False
            if len(structure_size) != 2 or len(center) != 2 or len(layers_sizes) + 1 != len(layers_p):
                return False
            if len(sizes_limit_height) != 2 or len(sizes_limit_width) != 2:
                return False
            if sorted(list(set(layers_sizes))) != layers_sizes:
                return False
            if center[0] > structure_size[0] or center[1] > structure_size[1]:
                return False
            return True

        if not validate_data():
            print("Неправильно введены данные")
            return False, []

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

        sizes_width = np.array(
            [random.randint(sizes_limit_width[0], sizes_limit_width[1]) for i in range(structure_size[0])])
        sizes_height = np.array(
            [random.randint(sizes_limit_height[0], sizes_limit_height[1]) for i in range(structure_size[1])])

        return True, [structure, sizes_width, sizes_height]

    def read_data():
        try:
            size_x = int(e1.get())
            size_y = int(e2.get())
            center_x = int(e3.get())
            center_y = int(e4.get())
        except:
            print("В одной из первых четырех строк не число")
            return False, []
        try:
            sizes_layers = list(map(int, e5.get().split(",")))
            p_layers = list(map(int, e6.get().split(",")))
            limits_x = list(map(int, e7.get().split(",")))
            limits_y = list(map(int, e8.get().split(",")))
        except:
            print("В одной из вторых четырех строк не числа, или они не разделены запятой")
            return False, []

        return True, [[size_x, size_y], [center_x, center_y], sizes_layers, p_layers, limits_x, limits_y]

    def visual(event):
        is_not_err, params = read_data()
        if is_not_err:
            field_size = params[0]
            center_cords = params[1]
            sizes_layers = params[2]
            p_layers = params[3]
            limits_x = params[4]
            limits_y = params[5]

            is_not_err, params = generate_model(field_size, center_cords, sizes_layers, p_layers, limits_x, limits_y)

            if not is_not_err:
                return

            structure, structure_heights, structure_widths = params[0], params[1], params[2]

            figure, axs = plt.subplots(1, 1, figsize=(5, 5))

            new_structure_width = [0]
            t = 0
            for i, e in enumerate(structure_widths):
                t += e
                new_structure_width.append(t)

            new_structure_height = [0]
            t = 0
            for i, e in enumerate(structure_heights):
                t += e
                new_structure_height.append(t)

            if len(structure_widths) > 15:
                x_ticks = [0]
                x_labels = [0]
                for i in range(13):
                    x_ticks.append(len(structure_widths) // 13 * (i+1))
                    x_labels.append(new_structure_width[x_ticks[-1]])
                x_ticks.append(len(structure_widths)-1)
                x_labels.append(new_structure_width[-1])
            else:
                x_ticks = [i for i in range(0, len(structure_widths))]
                x_labels = new_structure_width

            if len(structure_heights) > 15:
                y_ticks = [0]
                y_labels = [0]
                for i in range(13):
                    y_ticks.append(len(structure_heights) // 13 * (i+1))
                    y_labels.append(new_structure_height[y_ticks[-1]])
                y_ticks.append(len(structure_heights)-1)
                y_labels.append(new_structure_height[-1])
            else:
                y_ticks = [i for i in range(0, len(structure_heights))]
                y_labels = new_structure_height

            axs.set_xticks(x_ticks)
            axs.set_xticklabels(x_labels)
            axs.set_xlim([x_ticks[0], x_ticks[-1]])
            axs.set_xlabel("Расстояние по горизонтали, м")

            axs.set_yticks(y_ticks[::-1])
            axs.set_yticklabels(y_labels)
            axs.set_ylim([y_ticks[0], y_ticks[-1]])
            axs.set_ylabel("Расстояние по вертикали, м")

            p2 = axs.imshow(structure, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
            figure.colorbar(p2)
            plt.show()

    def rho_lines(event):
        is_not_err, params = read_data()
        if is_not_err:
            field_size = params[0]
            center_cords = params[1]
            sizes_layers = params[2]
            p_layers = params[3]
            limits_x = params[4]
            limits_y = params[5]

            is_not_err, params = generate_model(field_size, center_cords, sizes_layers, p_layers, limits_x, limits_y)

            if not is_not_err:
                return

            structure, structure_heights, structure_widths = params[0], params[1], params[2]

            solutions = []

            for i in structure:
                # print(solve_model(i, structure_heights))
                solutions.append(solve_model(i, structure_heights)[0])

            t_s = solve_model(structure[0], structure_heights)[-1]

            # print(solutions)
            temp_mas = np.log10(np.array(solutions))

            figure, axs = plt.subplots(1, 1, figsize=(5, 5))

            axs.plot([i + 1 for i in range(len(temp_mas))], temp_mas)

            if len(structure_widths) > 15:
                x_ticks = [0]
                x_labels = [1]
                t = len(structure_widths)//13
                for i in range(0 + t, t * 14, t):
                    x_ticks.append(i)
                    x_labels.append(i-1)
                x_ticks.append(len(structure_widths)-1)
                x_labels.append(len(structure_widths))
            else:
                x_ticks = [i for i in range(0, len(structure_widths))]
                x_labels = [i+1 for i in range(0, len(structure_widths))]

            axs.set_xticks(x_ticks)
            axs.set_xticklabels(x_labels)
            axs.set_xlim([0, len(structure_widths)-1])

            axs.set_yscale('log')
            axs.set_xlabel("Номер пикета")
            axs.set_ylabel(r"Кажущееся сопротивление, $lg(\rho_{T})$")

            legend_marks = [round(i, 2) for i in t_s]
            axs.legend(legend_marks, title=r"Периоды, $T [с]$")
            plt.show()

    def phi_lines(event):
        is_not_err, params = read_data()
        if is_not_err:
            field_size = params[0]
            center_cords = params[1]
            sizes_layers = params[2]
            p_layers = params[3]
            limits_x = params[4]
            limits_y = params[5]

            is_not_err, params = generate_model(field_size, center_cords, sizes_layers, p_layers, limits_x, limits_y)

            if not is_not_err:
                return

            structure, structure_heights, structure_widths = params[0], params[1], params[2]

            solutions = []

            for i in structure:
                solutions.append(solve_model(i, structure_heights)[1])

            t_s = solve_model(structure[0], structure_heights)[-1]

            temp_mas = np.array(solutions)

            figure, axs = plt.subplots(1, 1, figsize=(5, 5))

            axs.plot([i + 1 for i in range(len(temp_mas))], temp_mas)

            if len(structure_widths) > 15:
                x_ticks = [0]
                x_labels = [1]
                t = len(structure_widths)//13
                for i in range(0 + t, t * 14, t):
                    x_ticks.append(i)
                    x_labels.append(i-1)
                x_ticks.append(len(structure_widths)-1)
                x_labels.append(len(structure_widths))
            else:
                x_ticks = [i for i in range(0, len(structure_widths))]
                x_labels = [i+1 for i in range(0, len(structure_widths))]

            axs.set_xticks(x_ticks)
            axs.set_xticklabels(x_labels)
            axs.set_xlim([0, len(structure_widths)-1])

            axs.set_xlabel("Номер пикета")
            axs.set_ylabel(r"Периоды, $T [с]$")

            legend_marks = [round(i, 2) for i in t_s]
            axs.legend(legend_marks, title=r"Периоды, $T [с]$")
            plt.show()

    def rho_map(event):
        is_not_err, params = read_data()
        if is_not_err:
            field_size = params[0]
            center_cords = params[1]
            sizes_layers = params[2]
            p_layers = params[3]
            limits_x = params[4]
            limits_y = params[5]

            is_not_err, params = generate_model(field_size, center_cords, sizes_layers, p_layers, limits_x, limits_y)

            if not is_not_err:
                return

            structure, structure_heights, structure_widths = params[0], params[1], params[2]

            solutions = []

            for i in structure:
                solutions.append(solve_model(i, structure_heights)[0])

            t_s = solve_model(structure[0], structure_heights)[-1]

            temp_mas = np.log10(np.array(solutions).transpose())

            figure, axs = plt.subplots(1, 1, figsize=(5, 5))

            new_structure_width = [0]
            t = 0
            for i, e in enumerate(structure_widths):
                t += e
                new_structure_width.append(t)

            if len(structure_widths) > 15:
                x_ticks = [0]
                x_labels = [0]
                for i in range(13):
                    x_ticks.append(len(structure_widths) // 13 * (i + 1))
                    x_labels.append(new_structure_width[x_ticks[-1]])
                x_ticks.append(len(structure_widths) - 1)
                x_labels.append(new_structure_width[-1])
            else:
                x_ticks = [i for i in range(0, len(structure_widths))]
                x_labels = new_structure_width

            axs.set_xticks(x_ticks)
            axs.set_xticklabels(x_labels)
            axs.set_xlim([0, len(structure_widths)-1])
            axs.set_xlabel("Расстояние по горизонтали, м")

            axs.set_ylim([len(t_s)-1, 0])
            axs.set_yticks([i for i in range(0, len(t_s))])
            axs.set_yticklabels([round(i, 2) for i in t_s])
            axs.set_ylabel(r"Периоды, $T [с]$")

            p2 = axs.imshow(temp_mas, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
            cb = figure.colorbar(p2)
            cb.set_label(r"Кажущееся сопротивление, $lg(\rho_{T})$")
            plt.show()

    def phi_map(event):
        is_not_err, params = read_data()
        if is_not_err:
            field_size = params[0]
            center_cords = params[1]
            sizes_layers = params[2]
            p_layers = params[3]
            limits_x = params[4]
            limits_y = params[5]

            is_not_err, params = generate_model(field_size, center_cords, sizes_layers, p_layers, limits_x, limits_y)

            if not is_not_err:
                return

            structure, structure_heights, structure_widths = params[0], params[1], params[2]

            solutions = []

            for i in structure:
                solutions.append(solve_model(i, structure_heights)[1])

            t_s = solve_model(structure[0], structure_heights)[-1]

            temp_mas = np.array(solutions).transpose()

            figure, axs = plt.subplots(1, 1, figsize=(5, 5))

            new_structure_width = [0]
            t = 0
            for i, e in enumerate(structure_widths):
                t += e
                new_structure_width.append(t)

            if len(structure_widths) > 15:
                x_ticks = [0]
                x_labels = [0]
                for i in range(13):
                    x_ticks.append(len(structure_widths) // 13 * (i + 1))
                    x_labels.append(new_structure_width[x_ticks[-1]])
                x_ticks.append(len(structure_widths) - 1)
                x_labels.append(new_structure_width[-1])
            else:
                x_ticks = [i for i in range(0, len(structure_widths))]
                x_labels = new_structure_width

            axs.set_xticks(x_ticks)
            axs.set_xticklabels(x_labels)
            axs.set_xlim([0, len(structure_widths)-1])
            axs.set_xlabel("Расстояние по горизонтали, м")

            axs.set_ylim([len(t_s)-1, 0])
            axs.set_yticks([i for i in range(0, len(t_s))])
            axs.set_yticklabels([round(i, 2) for i in t_s])
            axs.set_ylabel(r"Периоды, $T [с]$")

            p2 = axs.imshow(temp_mas, cmap='jet', aspect='auto', interpolation='bilinear', origin="upper")
            cb = figure.colorbar(p2)
            cb.set_label(r"Фаза импеданса, $\phi$")
            plt.show()

    master = Tk()

    l1 = Label(master, text="Длина по оси X:")
    l2 = Label(master, text="Длина по оси Y:")
    l3 = Label(master, text="Центральная точка по X")
    l4 = Label(master, text="Центральная точка по Y:")
    l5 = Label(master, text="Размеры слоев (через ',')")
    l6 = Label(master, text="p слоев (через ',')")
    l7 = Label(master, text="Лимиты размеров по X(через ',')")
    l8 = Label(master, text="Лимиты размеров по Y(через ',')")

    l1.grid(row=0, column=0, sticky="nsew", pady=2, columnspan=2)
    l2.grid(row=1, column=0, sticky="nsew", pady=2, columnspan=2)
    l3.grid(row=2, column=0, sticky="nsew", pady=2, columnspan=2)
    l4.grid(row=3, column=0, sticky="nsew", pady=2, columnspan=2)
    l5.grid(row=4, column=0, sticky="nsew", pady=2, columnspan=2)
    l6.grid(row=5, column=0, sticky="nsew", pady=2, columnspan=2)
    l7.grid(row=6, column=0, sticky="nsew", pady=2, columnspan=2)
    l8.grid(row=7, column=0, sticky="nsew", pady=2, columnspan=2)

    e1 = Entry(master)
    e2 = Entry(master)
    e3 = Entry(master)
    e4 = Entry(master)
    e5 = Entry(master)
    e6 = Entry(master)
    e7 = Entry(master)
    e8 = Entry(master)

    e1.grid(row=0, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e2.grid(row=1, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e3.grid(row=2, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e4.grid(row=3, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e5.grid(row=4, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e6.grid(row=5, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e7.grid(row=6, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)
    e8.grid(row=7, column=2, pady=2, columnspan=8, sticky="nsew", padx=5)

    e1.insert(0, "100")
    e2.insert(0, "100")
    e3.insert(0, "50")
    e4.insert(0, "50")
    e5.insert(0, "10, 20")
    e6.insert(0, "1000, 500, 100")
    e7.insert(0, "100, 100")
    e8.insert(0, "100, 200")

    b1 = Button(master, text="Визуализировать данные")
    b2 = Button(master, text="Кривые Pho кажущегося")
    b3 = Button(master, text="Карта Pho кажущегося")
    b4 = Button(master, text="Кривые phi")
    b5 = Button(master, text="Карта phi")

    b1.bind('<Button-1>', visual)
    b2.bind('<Button-1>', rho_lines)
    b3.bind('<Button-1>', rho_map)
    b4.bind('<Button-1>', phi_lines)
    b5.bind('<Button-1>', phi_map)

    b1.grid(row=8, column=0, sticky="nsew", columnspan=2, padx=4)
    b2.grid(row=8, column=2, sticky="nsew", columnspan=2, padx=4)
    b3.grid(row=8, column=4, sticky="nsew", columnspan=2, padx=4)
    b4.grid(row=8, column=6, sticky="nsew", columnspan=2, padx=4)
    b5.grid(row=8, column=8, sticky="nsew", columnspan=2, padx=4)

    mainloop()


if __name__ == "__main__":
    main()
