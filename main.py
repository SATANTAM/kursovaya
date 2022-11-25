from tkinter import *
from tkinter import messagebox
import random


instr = 'Программа '

zach = 'd'

def File():
    messagebox.showinfo("Справка", instr)

def Spravka():
    messagebox.showinfo("Справка", zach)



root = Tk()
root.geometry('450x250')
root.title("Kursovaya")
root.resizable(False, False)
root.configure(background="#E6F0D5")

# Начало блока меню
menu1 = Menu(root)
root.configure(menu=menu1)
menu1.add_command(label="Справка", command=File)
# Конец блока меню


but1 = Button(root, text='Загрузить данные', font=("Ubuntu", 15), height=1, width=25, bg='#F8F8F8')
but2 = Button(root, text='Визуализировать', font=("Ubuntu", 15), height=1, width=25, bg='#F8F8F8')
but3 = Button(root, text='Визуализировать карту ρₖ', font=("Ubuntu", 15), height=1, width=25, bg='#F8F8F8')
but4 = Button(root, text='Визуализировать карту ρₖ', font=("Ubuntu", 15), height=1, width=25, bg='#F8F8F8')

but1.place(x=82, y=17)
but2.place(x=82, y=45)
but3.place(x=82, y=75)
but4.place(x=82, y=140)

root.mainloop()