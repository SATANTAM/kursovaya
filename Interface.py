from tkinter import *
from tkinter.ttk import *


def main():
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
    e6.insert(0, "1000, 500, 0")
    e7.insert(0, "100, 100")
    e8.insert(0, "100, 200")

    b1 = Button(master, text="Визуализировать данные")
    b2 = Button(master, text="Кривые Pho кажущегося")
    b3 = Button(master, text="Карта Pho кажущегося")
    b4 = Button(master, text="Кривые phi")
    b5 = Button(master, text="Карта phi")

    b1.grid(row=8, column=0, sticky="nsew", columnspan=2, padx=4)
    b2.grid(row=8, column=2, sticky="nsew", columnspan=2, padx=4)
    b3.grid(row=8, column=4, sticky="nsew", columnspan=2, padx=4)
    b4.grid(row=8, column=6, sticky="nsew", columnspan=2, padx=4)
    b5.grid(row=8, column=8, sticky="nsew", columnspan=2, padx=4)

    mainloop()


if __name__ == "__main__":
    main()
