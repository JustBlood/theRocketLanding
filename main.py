import time
import tkinter as tk
from calculation import Calculation
from PIL import Image, ImageTk

calc = None
now_dm = 0

class StartButton:
    name = []
    def __init__(self, frame, bg, name):
        self.name = name
        self.b = tk.Button(frame, text='Начать вычисления',
                                 bg=bg,
                                 activebackground=bg,
                                 activeforeground='white',
                                 foreground='white',
                                 font=('Courier-New', 15, 'bold'),
                                 )
        self.b.pack(pady=20)

    def get_entry(self, event):
        entry_list = []
        for i in range(len(self.name)):
            # to-do: добавить валидацию
            value = self.name[i].get()
            if value:
                entry_list.append(value)
            else:
                return 0
        global calc
        calc = Calculation(*map(float, entry_list))



class Example(tk.Frame):
    h = 800
    w = 1200
    bg = "#044857"
    rocket = None
    entrys_names = ("Масса топлива(кг)", "Масса корпуса(кг)", "Ускорение свободного падения(м/с2)", "Скорость газов относительно ракеты(м/с)", "Начальная высота(м)", "Разрешенная посадочная скорость(м/с)", "Шаг по времени(сек)", "Максимальный расход топлива(кг)")
    entrys_vals = (30000, 6000, 1.62, 2500, 10000, 5, 0.5, 300)
    btn_start = None

    speed_x = 0.5
    speed_y = 0.5

    def __init__(self, win):
        tk.Frame.__init__(self, master=win)

    def initUI(self):

        photo = tk.PhotoImage(file='C:\\Users\\User\\Downloads\\img.png')
        self.master.iconphoto(False, photo)
        self.master.config(bg=self.bg)
        self.master.title('Посадка на луну')
        self.master.geometry(f"{self.w}x{self.h}+200+100")
        self.master.resizable(False, False)

        #хранит фреймы
        name = []
        '''С помощью pack()'''
        frame = tk.Frame(self.master, bg=self.bg)
        for i in range(len(self.entrys_names)):
            n_frame = tk.Frame(frame, bg=self.bg)
            tk.Label(n_frame, text=self.entrys_names[i],
                     padx=10, pady=15,
                     width=25, height=1,
                     bg=self.bg, foreground='white',
                     anchor='w', justify="left",
                     wraplength=150).pack(side=tk.LEFT)
            name.append(tk.Entry(n_frame))
            name[i].insert(0, self.entrys_vals[i])
            name[i].pack(side=tk.RIGHT)
            n_frame.pack()
        self.btn_start = StartButton(frame, self.bg, name)
        frame.pack(side=tk.LEFT, anchor='nw', fill=tk.Y, ipady=60, ipadx=10)

        canvas = tk.Canvas(self.master, bg='white', height=self.h, width=self.w-343, highlightthickness=0)
        canvas.pack()

        img_bg = ImageTk.PhotoImage(Image.open("clouds.png").resize((1300, 1000), Image.LANCZOS))
        canvas.image = [img_bg]
        imgRocket = tk.PhotoImage(file="rocket1.png")
        canvas.image.append(imgRocket)

        imgRocket_1 = tk.PhotoImage(file="rocket1_1.png")

        canvas.image.append(imgRocket_1)

        print(canvas.__dict__)
        self.bg_canvas = canvas.create_image(0, 0, anchor='nw', image=img_bg)
        self.rocket = canvas.create_image(int(canvas['width']) / 2, self.h / 2, image=imgRocket)
        self.rocket_1 = canvas.create_image(int(canvas['width']) / 2, self.h / 2, image=imgRocket_1)

    def update(self):
        self.animation()
        self.master.update()

    def animation(self):
        coords = self.master.pack_slaves()[1].coords(self.rocket)
        # добавляет движение ракеты вправо-влево, всегда
        if coords[0] > self.master.pack_slaves()[1].winfo_width()/2+10: self.speed_x = -self.speed_x
        elif coords[0] < self.master.pack_slaves()[1].winfo_width()/2-10: self.speed_x = -self.speed_x
        # добавляет движение ракеты вверх-вниз, всегда
        if coords[1] > self.master.pack_slaves()[1].winfo_height() / 2 + 3: self.speed_y = -self.speed_y
        elif coords[1] < self.master.pack_slaves()[1].winfo_height() / 2 - 3: self.speed_y = -self.speed_y
        #добавляет движение фона
        # print(self.master.pack_slaves()[1].image)

        self.master.pack_slaves()[1].move(self.rocket, self.speed_x, self.speed_y)



def close():
    global running
    running = False

def change_dm(event):
    global now_dm
    if calc:
        if event.keysym == "Up":
            if now_dm < calc.allow_max_dm:
                now_dm += calc.allow_max_dm/100*1
                if now_dm > calc.allow_max_dm:
                    now_dm = calc.allow_max_dm
            return now_dm
        elif event.keysym == "Down":
            if now_dm >= 0:
                now_dm -= calc.allow_max_dm/100
                if now_dm < 0:
                    now_dm = 0
            return now_dm

running = True

now_dm = 10

def main():

    win = tk.Tk()
    app = Example(win)
    app.initUI()
    win.protocol("WM_DELETE_WINDOW", close)
    app.btn_start.b.bind('<Button-1>', app.btn_start.get_entry)
    win.bind('<Up>', change_dm)
    win.bind('<Down>', change_dm)

    while running:
        app.update()
        # if now_dm != 0:
            # print(app.master.pack_slaves()[1].__dict__)

        if calc:
            if calc.h[-1] > 0 and calc.m_fuel > 0:
                calc.calculate(now_dm)
        # time.sleep(0.01)

    win.destroy()


if __name__ == '__main__':
    main()