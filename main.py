from tkinter import *
from tkinter import ttk as ttk
from tkinter import messagebox as mbox
from tkinter.ttk import Combobox

import numpy as np


# Класс для точки
class tkPoint:
    X = 0
    Y = 0

    def __init__(self, gx, gy):
        self.X = gx
        self.Y = gy
        return


class tkLine:
    A = tkPoint(0, 0)
    B = tkPoint(0, 0)
    color = "#000000"

    def __init__(self, ax, ay, bx, by, c="#000000"):
        self.A = tkPoint(ax, ay)
        self.B = tkPoint(bx, by)
        self.color = c
        return


def vAngle(A, B, C, D):
    v1 = [B.X - A.X, B.Y - A.Y]
    v2 = [D.X - C.X, D.Y - C.Y]
    i = (v1[0] * v2[0] + v1[1] * v2[1]) / (
                np.sqrt(v1[0] * v1[0] + v1[1] * v1[1]) * np.sqrt(v2[0] * v2[0] + v2[1] * v2[1]))
    return i


# Возвращает угол поворота вектора,
def rotate(A, B, C):
    return (B.X - A.X) * (-C.Y + B.Y) - (-B.Y + A.Y) * (C.X - B.X)


# Возвращает истину, если AB пересекает CD
def intersect(A, B, C, D):
    print("checking intersection")
    return rotate(A, B, C) * rotate(A, B, D) <= 0 and rotate(C, D, A) * rotate(C, D, B) < 0

# Окно для отсечения отрезков
class SectWin():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.centreWindow()
        self.top.wm_title("Отсечение отрезков")

        menubar = Menu(self.top)

        menubar.add_command(label="Очистить поле", command=self.ClearWin)
        menubar.add_command(label="Создать отрезок", command=self.modeLine)
        menubar.add_command(label="Создать окно", command=self.modeSect)
        menubar.add_command(label="Удалить сечение", command=self.ClearSec)

        self.top.config(menu=menubar)

        self.tmp = None
        self.lines = []
        self.sc = []
        self.C = False
        self.fin = False

        self.canvas = Canvas(self.top, bg="white", width=900, height=900)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.mouseGrabLine)  # Создание новой точки

        self.canvas.focus_set()
# Режим создания отрезков
    def modeLine(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<ButtonPress-1>", self.mouseGrabLine)  # Создание новой точки
# Режим создания сечения
    def modeSect(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.mouseGrabSect)  # Создание новой точки

# Перерисовка сцены
    def redraw(self):
        self.canvas.delete("lineMain")
        self.canvas.delete("lineSec")
        self.canvas.delete("tempSec")
        if len(self.sc) > 2 and len(self.lines) > 0:
            self.linesLocate()

        for i in range(len(self.lines)):
            self.canvas.create_line(self.lines[i].A.X, self.lines[i].A.Y, self.lines[i].B.X, self.lines[i].B.Y,
                                    tag="lineMain", width=2,fill = self.lines[i].color)

        for i in range(len(self.sc) - 1):
            self.canvas.create_line(self.sc[i].X, self.sc[i].Y, self.sc[i + 1].X, self.sc[i + 1].Y, width=2,
                                    fill="#3e25b0", tag="lineSec")
        if (len(self.sc) > 2) and (self.fin == False):
            self.canvas.create_line(self.sc[len(self.sc) - 1].X, self.sc[len(self.sc) - 1].Y, self.sc[0].X,
                                    self.sc[0].Y,
                                    width=2, fill="#3e25b0", tag="tempSec", dash=5)
        elif (self.fin == True):
            self.canvas.create_line(self.sc[len(self.sc) - 1].X, self.sc[len(self.sc) - 1].Y, self.sc[0].X,
                                    self.sc[0].Y,
                                    width=2, fill="#3e25b0", tag="lineSec")

        return
# Функция нахождения точки
    def pointLocate(self, A):
        print("locating point", A.X, A.Y)
        if rotate(self.sc[0], self.sc[1], A) < 0 or rotate(self.sc[0], self.sc[len(self.sc) - 1], A) > 0:
            print("case 1")
            return False
        p = 1
        r = len(self.sc) - 1
        while r - p > 1:
            q = (p + r) // 2
            if rotate(self.sc[0], self.sc[q], A) < 0:
                r = q
            else:
                p = q
        return not intersect(self.sc[0], A, self.sc[p], self.sc[r])
# Функция нахождения отрезка
    def lineLocate(self,L):
        res = False
        res = res or self.pointLocate(L.A) or self.pointLocate(L.B)
        for i in range(len(self.sc)-1):
            res = res or intersect(self.sc[i],self.sc[i+1],L.A,L.B)
        print(res)
        return res
# Функция нахождения отрезков из памяти
    def linesLocate(self):
        for i in range (len(self.lines)):
            if self.lines[i].color != "#b7eb34":
                print("locating line ", i)
                if self.lineLocate(self.lines[i]):
                    self.lines[i].color = "#b7eb34"
        return

# Захват мыши для создания отрезка
    def mouseGrabLine(self, event):
        self.tmp = tkPoint(event.x, event.y)
        self.canvas.bind("<ButtonRelease-1>", self.mouseReleaseLine)
        self.canvas.bind("<Motion>", self.mouseMoveLine)
        return

# Перемещение мыши для создания отрезка

    def mouseMoveLine(self, event):
        self.redraw()
        self.canvas.create_line(self.tmp.X, self.tmp.Y, event.x, event.y, tag="lineMain", width=2)
        return

# Отпускание мыши для создания отрезка

    def mouseReleaseLine(self, event):
        self.canvas.unbind("<Motion>")
        self.lines.append(tkLine(self.tmp.X, self.tmp.Y, event.x, event.y))
        self.redraw()
        self.canvas.unbind("<ButtonRelease-1>")
        return

# Захват мыши для создания сечения

    def mouseGrabSect(self, event):

        self.sc.append(tkPoint(event.x, event.y))

        self.tmp = self.sc[len(self.sc) - 1]
        self.canvas.bind("<Button-1>", self.mouseReleaseSect)
        self.canvas.bind("<Motion>", self.mouseMoveSect)
        return

# Перемещение мыши для создания сечения

    def mouseMoveSect(self, event):
        if (len(self.sc)) > 2:
            if (abs(event.x - self.sc[0].X) < 5) or (abs(event.y - self.sc[0].X) < 5):
                self.C = True
            else:
                self.C = False

        if self.C:
            self.canvas.bind("<Button-1>", self.mouseReleaseSect)
            self.redraw()
            self.canvas.create_line(self.tmp.X, self.tmp.Y, self.sc[0].X, self.sc[0].Y, tag="lineSec", width=2,
                                    fill="#3e25b0")
        else:
            if (len(self.sc)) > 1:
                V = True
                for k in range(len(self.sc) - 1):
                    p2 = self.sc[k].Y - self.sc[k + 1].Y
                    p1 = self.sc[k].X - self.sc[k + 1].X
                    x0 = self.sc[k].X
                    y0 = self.sc[k].Y
                    V = V and (event.x * p2 - event.y * p1 <= x0 * p2 - y0 * p1)
                if (len(self.sc)) > 2:
                    p2 = self.sc[len(self.sc) - 1].Y - self.sc[0].Y
                    p1 = self.sc[len(self.sc) - 1].X - self.sc[0].X
                    x0 = self.sc[len(self.sc) - 1].X
                    y0 = self.sc[len(self.sc) - 1].Y
                    V = V and (event.x * p2 - event.y * p1 > x0 * p2 - y0 * p1)
                if V:
                    self.canvas.bind("<Button-1>", self.mouseReleaseSect)
                    self.redraw()
                    self.canvas.create_line(self.tmp.X, self.tmp.Y, event.x, event.y, tag="lineSec", width=2,
                                            fill="#3e25b0")
                if not V:
                    self.canvas.unbind("<Button-1>")
            else:
                self.redraw()
                self.canvas.create_line(self.tmp.X, self.tmp.Y, event.x, event.y, tag="lineSec", width=2,
                                        fill="#3e25b0")

        return

# Отпускание мыши для создания сечения

    def mouseReleaseSect(self, event):
        self.canvas.unbind("<Motion>")
        if not self.C:
            self.mouseGrabSect(event)
        else:
            self.fin = True
            print("fin")
            self.redraw()
            t = self.sc.index(min(self.sc, key=lambda tkPoint: tkPoint.X))
            for i in range(t):
                self.sc.insert(0, self.sc.pop())
            self.canvas.unbind("<Button-1>")
            self.redraw()
        return

# Очистка сечения

    def ClearSec(self):
        self.canvas.delete("lineSec")
        self.canvas.delete("tempSec")
        for i in range(len(self.lines)):
            self.lines[i].color = "#000000"
        self.sc = []
        self.C = False
        self.fin = False
        self.redraw()

#Очистка окна
    def ClearWin(self):
        self.canvas.delete("all")
        self.lines = []
        self.sc = []
        self.C = False
        self.fin = False

    def DestWin(self):
        self.top.destroy()

    def centreWindow(self):
        w = 900
        h = 900

        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2 - 50
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Окно для построения кривой Безье
class BezField:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.centreWindow()
        self.top.wm_title("Рисование кривой Безье")
        menubar = Menu(self.top)

        menubar.add_command(label="Очистить поле", command=self.ClearWin)
        self.top.config(menu=menubar)

        self.dragged = None
        self.points = []
        self.pointsBez = []

        self.count = 0

        self.canvas = Canvas(self.top, bg="white", width=900, height=900)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.processMouseEvent)  # Создание новой точки
        self.canvas.bind("<Button-3>", self.moveMouseEvent)  # Перемещение точки
        self.canvas.bind("<Button-2>", self.getInfo)  # Просмотр информации об объекте
        self.canvas.bind("<Delete>", self.delPointAction)  # Удаление точки

        self.canvas.focus_set()

    # Функция создания точки
    def processMouseEvent(self, event):
        tmp = len(self.points)
        self.points.append(tkPoint(event.x, event.y))
        self.canvas.create_rectangle(event.x - 5, event.y + 5, event.x + 5, event.y - 5, width=1,
                                     tag=(tmp, "rectangle"), fill="black")
        self.redraw()

    # Функция отпускания точки
    def releaseEvent(self, event):
        self.canvas.unbind("<Motion>")
        self.canvas.bind("<Button-3>", self.moveMouseEvent)
        self.canvas.bind("<Button-1>", self.processMouseEvent)
        self.dragged = None

    # Функция захвата точки
    def moveMouseEvent(self, event):

        if self.canvas.find_withtag("current") == () or \
                self.canvas.gettags(self.canvas.find_withtag("current"))[0] == "line":
            return

        self.dragged = self.canvas.find_withtag("current")
        self.count = self.delCounter()
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-3>", self.releaseEvent)
        self.canvas.bind("<Motion>", self.moveAction)

        self.redraw()


    # Пересчет номера точки (при удалении и перемещении)
    def delCounter(self):
        t = 0
        while self.canvas.find_withtag("rectangle")[t] != self.canvas.find_withtag("current")[0]:
            t = t + 1

        print("deleting: ", self.canvas.gettags(self.canvas.find_withtag("current")[0])[0], t)
        return t

    # Функция просмотра информации
    def getInfo(self, event):
        print(self.canvas.gettags(self.canvas.find_withtag("current")))
        print(self.delCounter())

    # Функция удаления точки
    def delPointAction(self, event):
        if self.canvas.find_withtag("current") == () or \
                self.canvas.gettags(self.canvas.find_withtag("current"))[0] == "line":
            return

        self.dragged = self.canvas.find_withtag("current")

        self.points.pop(self.delCounter())

        self.canvas.delete("current")
        self.dragged = None
        self.redraw()

    # Функция перемещения
    def moveAction(self, event):
        self.canvas.coords(self.dragged, event.x - 5, event.y + 5, event.x + 5, event.y - 5)
        i = self.count
        self.points[i].X = event.x
        self.points[i].Y = event.y
        self.redraw()

    # Перерисовка сцены
    def redraw(self):
        self.canvas.delete('line')

        self.pointsBez = []
        if len(self.points) > 1:
            i = 0
            while i < 1:
                self.bezline(self.points, i)
                i = i + 0.05

        for i in range(len(self.points) - 1):
            self.canvas.create_line(self.points[i].X, self.points[i].Y, self.points[i + 1].X, self.points[i + 1].Y,
                                    tag='line')

        for i in range(len(self.pointsBez) - 1):
            self.canvas.create_line(self.pointsBez[i].X, self.pointsBez[i].Y, self.pointsBez[i + 1].X,
                                    self.pointsBez[i + 1].Y, tag='line')

        return

    #Поиск точки, делящей отрезок AB в отношении arg
    def lerp(self, pointA, pointB, arg):
        temp = tkPoint(pointA.X + arg * (pointB.X - pointA.X), pointA.Y + arg * (pointB.Y - pointA.Y))
        return temp


    # Алгоритм де Кастельжо
    def bezline(self, arr, arg):
        temp = []
        for i in range(len(arr) - 1):
            temp.append(self.lerp(arr[i], arr[i + 1], arg))
        if len(arr) == 2:
            self.pointsBez.append(temp[0])
        else:
            self.bezline(temp, arg)

    def DestWin(self):
        self.top.destroy()

    def ClearWin(self):
        self.canvas.delete("all")
        self.points = []
        self.pointsBez = []

    def centreWindow(self):
        w = 900
        h = 900

        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2 - 50
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Диалог создания фигуры

class objDialog():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.SubmitButton = Button(top, text='Создать', command=self.DestWin, width=20)
        self.centreWindow()
        self.top.wm_title("Создание нового объекта")

        self.comboExample = Combobox(top,
                                     values=[
                                         "Куб",
                                         "Тетраэдр",
                                         "Пирамида"], width=30)
        self.comboExample.current(0)

        self.comboExample.grid(row=0, column=0, columnspan=2)

        self.labelX = Label(top, text="X:")
        self.labelY = Label(top, text="Y:")
        self.labelZ = Label(top, text="Z:")

        self.labelSize = Label(top, text="Сторона:")

        self.labelX.grid(row=1, column=0)
        self.labelY.grid(row=2, column=0)
        self.labelZ.grid(row=3, column=0)
        self.labelSize.grid(row=4, column=0)

        self.pointFieldX = Entry(top)
        self.pointFieldY = Entry(top)
        self.pointFieldZ = Entry(top)
        self.width = Entry(top)

        self.pointFieldX.insert(0, "0")
        self.pointFieldY.insert(0, "0")
        self.pointFieldZ.insert(0, "0")
        self.width.insert(0, "99")

        self.pointFieldX.grid(row=1, column=1)
        self.pointFieldY.grid(row=2, column=1)
        self.pointFieldZ.grid(row=3, column=1)
        self.width.grid(row=4, column=1)

        self.SubmitButton.grid(row=5, column=0, columnspan=2)

    # Закрытие окна
    def DestWin(self):
        mbox.showinfo(title="Успех", message="Создана фигура")
        self.callback([self.pointFieldX.get(), self.pointFieldY.get(), self.pointFieldZ.get(), self.width.get(),
                       self.comboExample.get()])
        self.top.destroy()

    # Обратный вызов
    def set_callback(self, a_func):
        self.callback = a_func

    def centreWindow(self):
        w = 260
        h = 240

        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2 - 50
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Основное окно
class Win(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.data = None
        self.Dcanvas = Canvas()
        self.Icanvas = Canvas()
        self.Points = []
        self.obj = None
        self.obj2 = None
        self.centreWindow()
        self.initUI()
        self.parent.config(bg="white")

    def initUI(self):
        self.parent.title("Graphic demo")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.config(bg="white")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        menubar.add_command(label="Новый объект", command=self.onNewObject)
        menubar.add_command(label="Диметрия", command=self.onDimetry)
        menubar.add_command(label="Изометрия", command=self.onIsometry)
        menubar.add_command(label="Кривая Безье", command=self.onBezline)
        menubar.add_command(label="Отсечение отрезков", command=self.onSection)

    def onSection(self):
        newSect = SectWin(self)
        return

    def onBezline(self):
        newBez = BezField(self)
        return

    def onNewObject(self):
        newobj = objDialog(self)
        newobj.set_callback(self.addObj)
        return

    # Добавление объекта в память программы
    def addObj(self, astr=''):
        # print(astr)
        self.data = astr
        self.Points = []
        A = int(self.data[0])
        B = int(self.data[1])
        C = int(self.data[2])
        size = int(self.data[3])

        # Формирование фигуры по точке и размеру
        if self.data[4] == "Куб":
            self.Points.append([A, B, C, 1])
            self.Points.append([A + size, B, C, 1])
            self.Points.append([A, B + size, C, 1])
            self.Points.append([A + size, B + size, C, 1])
            self.Points.append([A, B, C + size, 1])
            self.Points.append([A + size, B, C + size, 1])
            self.Points.append([A, B + size, C + size, 1])
            self.Points.append([A + size, B + size, C + size, 1])
        elif self.data[4] == "Пирамида":
            self.Points.append([A, B, C, 1])
            self.Points.append([A + size, B, C, 1])
            self.Points.append([A, B, C + size, 1])
            self.Points.append([A + size, B, C + size, 1])
            self.Points.append([A + size / 2, B + size, C + size / 2, 1])
        elif self.data[4] == "Тетраэдр":
            self.Points.append([A, B, C, 1])
            self.Points.append([A + size, B, C, 1])
            self.Points.append([A + size / 2, B, C + 0.866025403 * size, 1])
            self.Points.append([A + size / 2, B + 0.816496580 * size, C + size * 0.288675134, 1])
        # Точки для построения координат
        self.Points.append([-300 + A, 0 + B, 0 + C, 1])
        self.Points.append([0 + A, 300 + B, 0 + C, 1])
        self.Points.append([0 + A, 0 + B, 300 + C, 1])

        self.obj = np.array(self.Points)

        print(self.obj)

    # Преобразование к диметрии
    def onDimetry(self):
        if self.Icanvas:
            self.Icanvas.destroy()
        if self.Dcanvas:
            self.Dcanvas.destroy()
        self.Dcanvas = Canvas(self, width=1280, height=710, bg="white")
        # Матрица поворота
        turnMatrix = np.array([[0.925820, 0.133631, - 0.353553, 0],
                               [0, 0.935414, 0.353553, 0],
                               [0.377964, - 0.327329, 0.866025, 0],
                               [0, 0, 0, 1]])
        # Перемножение матриц
        self.obj2 = self.obj.dot(turnMatrix)
        projectionMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 1]])
        # Умножение на матрицу проекции
        self.obj2 = self.obj2.dot(projectionMatrix)

        A = []
        if self.data[4] == "Куб":
            for i in range(11):
                # Преобразование к координатам tkinter
                A.append([round(self.obj2[i, 0] + 640), round(360 - self.obj2[i, 1])])
            # Рисование фигуры
            self.Dcanvas.create_line(A[0][0], A[0][1], A[1][0], A[1][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[2][0], A[2][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[4][0], A[4][1])
            self.Dcanvas.create_line(A[1][0], A[1][1], A[3][0], A[3][1])
            self.Dcanvas.create_line(A[1][0], A[1][1], A[5][0], A[5][1])
            self.Dcanvas.create_line(A[6][0], A[6][1], A[2][0], A[2][1])
            self.Dcanvas.create_line(A[6][0], A[6][1], A[7][0], A[7][1])
            self.Dcanvas.create_line(A[6][0], A[6][1], A[4][0], A[4][1])
            self.Dcanvas.create_line(A[7][0], A[7][1], A[5][0], A[5][1])
            self.Dcanvas.create_line(A[7][0], A[7][1], A[3][0], A[3][1])
            self.Dcanvas.create_line(A[2][0], A[2][1], A[3][0], A[3][1])
            self.Dcanvas.create_line(A[4][0], A[4][1], A[5][0], A[5][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[8][0], A[8][1], fill="#FB00FF", arrow=LAST)
            self.Dcanvas.create_line(A[0][0], A[0][1], A[9][0], A[9][1], fill="#FB00FF", arrow=LAST)
            self.Dcanvas.create_line(A[0][0], A[0][1], A[10][0], A[10][1], fill="#FB00FF", arrow=LAST)

        elif self.data[4] == "Пирамида":
            for i in range(8):
                A.append([round(self.obj2[i, 0] + 640), round(360 - self.obj2[i, 1])])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[1][0], A[1][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[2][0], A[2][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[4][0], A[4][1])
            self.Dcanvas.create_line(A[3][0], A[3][1], A[1][0], A[1][1])
            self.Dcanvas.create_line(A[3][0], A[3][1], A[2][0], A[2][1])
            self.Dcanvas.create_line(A[3][0], A[3][1], A[4][0], A[4][1])
            self.Dcanvas.create_line(A[2][0], A[2][1], A[4][0], A[4][1])
            self.Dcanvas.create_line(A[4][0], A[4][1], A[1][0], A[1][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[5][0], A[5][1], fill="#FB00FF", arrow=LAST)
            self.Dcanvas.create_line(A[0][0], A[0][1], A[6][0], A[6][1], fill="#FB00FF", arrow=LAST)
            self.Dcanvas.create_line(A[0][0], A[0][1], A[7][0], A[7][1], fill="#FB00FF", arrow=LAST)
        elif self.data[4] == "Тетраэдр":
            for i in range(7):
                A.append([round(self.obj2[i, 0] + 640), round(360 - self.obj2[i, 1])])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[1][0], A[1][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[2][0], A[2][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[3][0], A[3][1])
            self.Dcanvas.create_line(A[1][0], A[1][1], A[2][0], A[2][1])
            self.Dcanvas.create_line(A[1][0], A[1][1], A[3][0], A[3][1])
            self.Dcanvas.create_line(A[2][0], A[2][1], A[3][0], A[3][1])
            self.Dcanvas.create_line(A[0][0], A[0][1], A[4][0], A[4][1], fill="#FB00FF", arrow=LAST)
            self.Dcanvas.create_line(A[0][0], A[0][1], A[5][0], A[5][1], fill="#FB00FF", arrow=LAST)
            self.Dcanvas.create_line(A[0][0], A[0][1], A[6][0], A[6][1], fill="#FB00FF", arrow=LAST)

        self.Dcanvas.pack()

        return

    # Преобразование к изометрии
    def onIsometry(self):
        if self.Dcanvas:
            self.Dcanvas.destroy()
        if self.Icanvas:
            self.Icanvas.destroy()
        self.Icanvas = Canvas(self, width=1280, height=710, bg="white")

        turnMatrix = np.array([[0.707107, 0.408248, -0.577353, 0],
                               [0, 0.816497, 0.577345, 0],
                               [0.707107, -0.408248, 0.577353, 0],
                               [0, 0, 0, 1]])

        self.obj2 = self.obj.dot(turnMatrix)
        projectionMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 1]])

        self.obj2 = self.obj2.dot(projectionMatrix)

        A = []
        if self.data[4] == "Куб":
            for i in range(11):
                A.append([round(self.obj2[i, 0] + 640), round(360 - self.obj2[i, 1])])
            self.Icanvas.create_line(A[0][0], A[0][1], A[1][0], A[1][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[2][0], A[2][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[4][0], A[4][1])
            self.Icanvas.create_line(A[1][0], A[1][1], A[3][0], A[3][1])
            self.Icanvas.create_line(A[1][0], A[1][1], A[5][0], A[5][1])
            self.Icanvas.create_line(A[6][0], A[6][1], A[2][0], A[2][1])
            self.Icanvas.create_line(A[6][0], A[6][1], A[7][0], A[7][1])
            self.Icanvas.create_line(A[6][0], A[6][1], A[4][0], A[4][1])
            self.Icanvas.create_line(A[7][0], A[7][1], A[5][0], A[5][1])
            self.Icanvas.create_line(A[7][0], A[7][1], A[3][0], A[3][1])
            self.Icanvas.create_line(A[2][0], A[2][1], A[3][0], A[3][1])
            self.Icanvas.create_line(A[4][0], A[4][1], A[5][0], A[5][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[8][0], A[8][1], fill="#FB00FF", arrow=LAST)
            self.Icanvas.create_line(A[0][0], A[0][1], A[9][0], A[9][1], fill="#FB00FF", arrow=LAST)
            self.Icanvas.create_line(A[0][0], A[0][1], A[10][0], A[10][1], fill="#FB00FF", arrow=LAST)

        elif self.data[4] == "Пирамида":
            for i in range(8):
                A.append([round(self.obj2[i, 0] + 640), round(360 - self.obj2[i, 1])])
            self.Icanvas.create_line(A[0][0], A[0][1], A[1][0], A[1][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[2][0], A[2][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[4][0], A[4][1])
            self.Icanvas.create_line(A[3][0], A[3][1], A[1][0], A[1][1])
            self.Icanvas.create_line(A[3][0], A[3][1], A[2][0], A[2][1])
            self.Icanvas.create_line(A[3][0], A[3][1], A[4][0], A[4][1])
            self.Icanvas.create_line(A[2][0], A[2][1], A[4][0], A[4][1])
            self.Icanvas.create_line(A[4][0], A[4][1], A[1][0], A[1][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[5][0], A[5][1], fill="#FB00FF", arrow=LAST)
            self.Icanvas.create_line(A[0][0], A[0][1], A[6][0], A[6][1], fill="#FB00FF", arrow=LAST)
            self.Icanvas.create_line(A[0][0], A[0][1], A[7][0], A[7][1], fill="#FB00FF", arrow=LAST)
        elif self.data[4] == "Тетраэдр":
            for i in range(7):
                A.append([round(self.obj2[i, 0] + 640), round(360 - self.obj2[i, 1])])
            self.Icanvas.create_line(A[0][0], A[0][1], A[1][0], A[1][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[2][0], A[2][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[3][0], A[3][1])
            self.Icanvas.create_line(A[1][0], A[1][1], A[2][0], A[2][1])
            self.Icanvas.create_line(A[1][0], A[1][1], A[3][0], A[3][1])
            self.Icanvas.create_line(A[2][0], A[2][1], A[3][0], A[3][1])
            self.Icanvas.create_line(A[0][0], A[0][1], A[4][0], A[4][1], fill="#FB00FF", arrow=LAST)
            self.Icanvas.create_line(A[0][0], A[0][1], A[5][0], A[5][1], fill="#FB00FF", arrow=LAST)
            self.Icanvas.create_line(A[0][0], A[0][1], A[6][0], A[6][1], fill="#FB00FF", arrow=LAST)

        self.Icanvas.pack()
        return

    def onExit(self):
        self.quit()

    def centreWindow(self):
        w = 1280
        h = 720

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2 - 50
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    app = Win(root)
    root.mainloop()


if __name__ == '__main__':
    main()
