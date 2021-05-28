import copy
import operator
import matplotlib.colors as colors
import tkinter
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


class tkPoint3D:
    X = 0
    Y = 0
    Z = 0
    W = 1

    def __init__(self, gx, gy, gz):
        self.X = gx
        self.Y = gy
        self.Z = gz
        return

class tkSurface:
    S = []
    ST = []
    N = 0
    M = 0
    SurfaceList = []
    SurfaceListT = []
    SurfaceListR = []

    def __init__(self,n=0,m=0):
        self.N = n
        self.M = m
        self.S  = []
        self.ST = []
        self.SurfaceList = []
        self.SurfaceListT = []
        self.SurfaceListR = []

        for i in range(0, m):
            Tlist = []
            for j in range(0, n):
                Tlist.append(tkPoint3D(-100*(m%2)*(m//2) -50*((m+1)%2)*(m//2+1) + 100*i,-100*(n%2)*(n//2) -50*((n+1)%2)*(n//2+1) + 100 * j, 0))
            self.S.append(Tlist)
            self.ST.append(Tlist)




class surfaceDialog():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.SubmitButton = Button(top, text='Создать', command=self.DestWin, width=20)
        self.centreWindow()
        self.top.wm_title("Создание поверхности")

        self.labelMain = Label(top, text = "Surface size:")
        self.labelX = Label(top,text = "x")
        self.pointFieldM = Entry(top)
        self.pointFieldN = Entry(top)

        self.labelMain.grid(row=1, column=1)

        self.pointFieldM = Entry(top)
        self.pointFieldN = Entry(top)

        self.pointFieldN.insert(0, 3)
        self.pointFieldM.insert(0, 3)

        self.pointFieldN.grid(row=2, column=1)
        self.labelX.grid(row=2, column=2)
        self.pointFieldM.grid(row=2, column=3)
        self.SubmitButton.grid(row=3, column=0, columnspan=3)

    # Закрытие окна
    def DestWin(self):
        self.callback([self.pointFieldM.get(), self.pointFieldN.get()])
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



class pointDialog():
    def __init__(self, parent,data):
        top = self.top = Toplevel(parent)
        self.SubmitButton = Button(top, text='Изменить', command=self.DestWin, width=20)
        self.centreWindow()
        self.top.wm_title("Изменение координат точки")


        self.labelX = Label(top, text="X:")
        self.labelY = Label(top, text="Y:")
        self.labelZ = Label(top, text="Z:")

        self.labelX.grid(row=1, column=0)
        self.labelY.grid(row=2, column=0)
        self.labelZ.grid(row=3, column=0)

        self.pointFieldX = Entry(top)
        self.pointFieldY = Entry(top)
        self.pointFieldZ = Entry(top)

        self.pointFieldX.insert(0, data.X)
        self.pointFieldY.insert(0, data.Y)
        self.pointFieldZ.insert(0, data.Z)

        self.pointFieldX.grid(row=1, column=1)
        self.pointFieldY.grid(row=2, column=1)
        self.pointFieldZ.grid(row=3, column=1)

        self.SubmitButton.grid(row=4, column=0, columnspan=2)

    # Закрытие окна
    def DestWin(self):
        self.callback([self.pointFieldX.get(), self.pointFieldY.get(), self.pointFieldZ.get()])
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



    # Закрытие окна
    def DestWin(self):
        self.callback([self.pointFieldX.get(), self.pointFieldY.get(), self.pointFieldZ.get()])
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




# Окно для построения поверхности Безье

class BezSect:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.centreWindow()
        self.top.wm_title("Рисование поверхности Безье")
        menubar = Menu(self.top)

        self.useLighting = False
        self.varL = tkinter.IntVar()

        self.slider = Scale(self.top, from_=0, to=1000,
                               orient="horizontal",
                               command=self.updateValue)
        self.checkbox = Checkbutton(self.top,text = "Lighting",variable = self.varL, onvalue = 1, offvalue = 0,command=self.updateLight)

        menubar.add_command(label = "Создать поле",command = self.onNew)
        self.checkbox.grid(row = 0,column = 0)
        self.slider.grid(row = 0, column = 1)
        self.top.config(menu=menubar)

        #self.surface = tkSurface(2,2)
        self.global_temp = []
        #self.generate_bezfield()
        self.LightSource = tkPoint3D(300,300,500)
        self.LightIntensity = 0

        self.alpha = 0
        self.beta = 0
        self.gamma = 0










        self.canvas = Canvas(self.top, bg="white", width=900, height=900)

        self.canvas.bind("<Up>",self.turnXright)
        self.canvas.bind("<Down>",self.turnXleft)
        self.canvas.bind("<Left>",self.turnYdown)
        self.canvas.bind("<Right>",self.turnYup)
        self.canvas.bind("<Button-3>",self.onMove)
        self.canvas.bind("<Button-2>",self.getInfo)
        self.canvas.grid(row = 1,columnspan = 2)
        self.canvas.configure(scrollregion=(-300, -300, 300, 300))
        self.canvas.xview_moveto(.5)
        self.canvas.yview_moveto(.5)

        self.canvas.focus_set()
        #self.redraw()

    def updateValue(self,A):
        self.LightIntensity = int(A)
        self.redraw()

    def updateLight(self):
        self.useLighting = self.varL.get() == 1
        self.redraw()

    def onMove(self,event):
        t = self.canvas.gettags(self.canvas.find_withtag("current"))

        if (len(t)>0) and (t[0] != "current"):
            if t[0] == "Light":
                editPoint = pointDialog(self.top,self.LightSource)
                editPoint.set_callback(self.editLight)
            else:
                i = int(t[0])
                j = int(t[1])
                self.global_temp = [i,j]
                editPoint = pointDialog(self.top, self.surface.S[i][j])
                editPoint.set_callback(self.editPoint)
        return

    def onNew(self):
        nsurf = surfaceDialog(self.top)
        nsurf.set_callback(self.newSurface)

    def editLight(self,astr=''):
        self.LightSource.X = float(astr[0])
        self.LightSource.Y = float(astr[1])
        self.LightSource.Z = float(astr[2])
        self.redraw()

    # Добавление объекта в память программы
    def editPoint(self, astr=''):
        i = self.global_temp[0]
        j = self.global_temp[1]

        self.surface.S[i][j].X = float(astr[0])
        self.surface.S[i][j].Y = float(astr[1])
        self.surface.S[i][j].Z = float(astr[2])

        self.global_temp = []

        self.generate_bezfield()
        self.redraw()

    def newSurface(self, astr = ''):

        self.surface = tkSurface(int(astr[0]),int(astr[1]))
        self.generate_bezfield()
        self.slider.set(500)
        self.redraw()


    def turnXright(self,event):
        self.alpha = self.alpha + 10
        self.redraw()

    def turnYdown(self,event):
        self.beta = self.beta + 10
        self.redraw()

    def turnXleft(self,event):
        self.alpha = self.alpha - 10
        self.redraw()

    def turnYup(self,event):
        self.beta = self.beta - 10
        self.redraw()

    def getInfo(self, event):
        print(self.canvas.gettags(self.canvas.find_withtag("current")))
        print(self.canvas.gettags(self.canvas.find_below(self.canvas.find_withtag("current"))))
        print(self.canvas.gettags(self.canvas.find_above(self.canvas.find_withtag("current"))))
        A = self.canvas.coords(self.canvas.find_withtag("current"))
        x1=(A[0]+A[2])/2-0.05
        y1=(A[1]+A[5])/2-0.05
        x2=(A[0]+A[2])/2+0.05
        y2=(A[1]+A[5])/2+0.05
        # x2=self.canvas.coords(self.canvas.find_withtag("current"))[4]
        # y2=self.canvas.coords(self.canvas.find_withtag("current"))[5]
        print(x1,y1,x2,y2)
        print(self.canvas.coords(self.canvas.find_withtag("current")))
        print(self.canvas.gettags(self.canvas.find_overlapping(x1,y1,x2,y2)))



    def proj(self,A):
        B = self.rot(A)
        obj = np.array([B.X,B.Y,B.Z,B.W])
        projectionMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 1]])
        obj = obj.dot(projectionMatrix)
        res = tkPoint3D(obj[0],obj[1],obj[2])
        return res

    def projNOROT(self,A):
        B = A
        obj = np.array([B.X, B.Y, B.Z, B.W])
        projectionMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 1]])
        obj = obj.dot(projectionMatrix)
        res = tkPoint3D(obj[0], obj[1], obj[2])
        return res

    def rot(self,A):
        obj = np.array([A.X,A.Y,A.Z,A.W])

        alphaDeg = np.deg2rad(self.alpha)
        betaDeg = np.deg2rad(self.beta)
        gammaDeg = np.deg2rad(self.gamma)
        rotX = np.array([[1,0,0,0],
                         [0,np.cos(alphaDeg),np.sin(alphaDeg),0],
                         [0,-1*np.sin(alphaDeg),np.cos(alphaDeg),0],
                         [0,0,0,1]])
        rotY = np.array([[np.cos(betaDeg), 0, -1*np.sin(betaDeg), 0],
                         [0, 1, 0, 0],
                         [np.sin(betaDeg), 0, np.cos(betaDeg), 0],
                         [0, 0, 0, 1]])
        rotZ = np.array([[np.cos(gammaDeg), np.sin(gammaDeg), 0, 0],
                         [-1*np.sin(gammaDeg), np.cos(gammaDeg),0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

        turnMatrix = rotZ.dot(rotY)
        turnMatrix = turnMatrix.dot(rotX)
        obj = obj.dot(turnMatrix)
        res = tkPoint3D(obj[0],obj[1],obj[2])
        return res









    def turn(self):
        self.surface.ST = []
        self.surface.SurfaceListT = []
        self.surface.SurfaceListR = []
        index_i = 0
        for i in self.surface.S:
            Tlist = []
            index_j =0
            for j in i:
                Tlist.append(self.proj(j))
                index_j = index_j + 1
            index_i = index_i + 1
            self.surface.ST.append(Tlist)
        index_i = 0
        for i in self.surface.SurfaceList:
            Tlist = []
            Rlist = []
            index_j = 0
            for j in i:
                Rlist.append(self.rot(j))
                Tlist.append(self.proj(j))
                index_j = index_j + 1
            index_i = index_i + 1
            self.surface.SurfaceListR.append(Rlist)
            self.surface.SurfaceListT.append(Tlist)


    def overlap_polygons(self):
        tags = self.canvas.find_withtag("polygon")
        X = []
        for tag in tags:
            A = self.canvas.coords(tag)
            x1 = (A[0] + A[2]) / 2 - 0.05
            y1 = (A[1] + A[5]) / 2 - 0.05
            x2 = (A[0] + A[2]) / 2 + 0.05
            y2 = (A[1] + A[5]) / 2 + 0.05
            #if len(self.canvas.find_overlapping(x1,y1,x2,y2)) == 0:
                #self.canvas.itemconfig(tag,fill = "")
            #print("Overlap for ",self.canvas.gettags(tag), " => ", self.canvas.gettags(self.canvas.find_overlapping(x1,y1,x2,y2)))




    def redraw(self):
        self.canvas.delete("all")
        self.turn()
        self.generate_bezfield()


        self.canvas.create_text(400,-150,text = str([self.alpha % 360,self.beta % 360]))

        R = []

        k = 0
        for i in range (0,len(self.surface.SurfaceListT)):
            for j in range (0,len(self.surface.SurfaceListT[0])):
                if (j != len(self.surface.SurfaceListT[0]) - 1) and (i != len(self.surface.SurfaceListT)-1):




                    sR = self.rot(tkPoint3D(self.surface.SurfaceList[i][j].X,self.surface.SurfaceList[i][j].Y,self.surface.SurfaceList[i][j].Z)).Z < \
                         self.rot(tkPoint3D(self.surface.SurfaceList[i][j].X,self.surface.SurfaceList[i][j].Y,self.surface.SurfaceList[i][j].Z+5)).Z
                    sR = sR == (self.rot(tkPoint3D(0,0,0)).Z < self.rot(tkPoint3D(0,0,1)).Z)



                    sX = self.surface.SurfaceListR[i][j].X < self.surface.SurfaceListR[i][j + 1].X and \
                         self.surface.SurfaceListR[i + 1][j].X < self.surface.SurfaceListR[i + 1][j + 1].X
                    sY = self.surface.SurfaceListR[i][j].Y < self.surface.SurfaceListR[i+1][j].Y and \
                         self.surface.SurfaceListR[i][j+1].Y < self.surface.SurfaceListR[i + 1][j + 1].Y

                    s = (sX and sY and sR) or (not sX and not sY and sR)



                    colorStr = "#fc5203"
                    if s:
                        colorStr = "#2c03fc"

                    z = int(self.surface.SurfaceListR[i][j].Z)

                    if self.useLighting:
                        L = self.LightSource
                        P = self.surface.SurfaceListR[i][j]
                        N = self.rot(tkPoint3D(self.surface.SurfaceList[i][j].X, self.surface.SurfaceList[i][j].Y,
                                               self.surface.SurfaceList[i][j].Z + 10))
                        V = tkPoint3D(0, 0, 1000)
                        vecL = (-P.X + L.X, -P.Y + L.Y, -P.Z + L.Z)
                        vecN = (N.X - P.X, N.Y - P.Y, N.Z - P.Z)
                        vecV = (V.X - P.X, V.Y - P.Y, V.Z - P.Z)
                        # vecH = [vecL[0] + vecV[0], vecL[1] + vecV[1], vecL[2] + vecV[2]]
                        # norm = np.sqrt(vecH[0] ** 2 + vecH[1] ** 2 + vecH[2] ** 2)
                        # for ii in range(0, len(vecH)):
                        #     vecH[ii] = vecH[ii] / norm
                        # vecH = tuple(vecH)
                        # cosNH = abs((vecH[0] * vecN[0] + vecH[1] * vecN[1] + vecH[2] * vecN[2]) / np.sqrt(
                        #     vecH[0] ** 2 + vecH[1] ** 2 + vecH[2] ** 2) / np.sqrt(
                        #     vecN[0] ** 2 + vecN[1] ** 2 + vecN[2] ** 2))
                        cosLN = abs((vecL[0] * vecN[0] + vecL[1] * vecN[1] + vecL[2] * vecN[2]) / np.sqrt(
                            vecL[0] ** 2 + vecL[1] ** 2 + vecL[2] ** 2) / np.sqrt(
                            vecN[0] ** 2 + vecN[1] ** 2 + vecN[2] ** 2))
                        # light
                        dist = np.sqrt((P.X - L.X) ** 2 + (P.Y - L.Y) ** 2 + (P.Z - L.Z) ** 2)
                        iA = 0.3 * self.LightIntensity * (1000 - dist % 1000) / 1000
                        iD = 1.9 * self.LightIntensity * (1000 - dist % 1000) / 1000 * cosLN
                        iS = 0# + 1.3 * self.LightIntensity * (1000 - dist % 1000) / 1000 * (cosNH ** 5)
                        light = int((iA + iD+iS))
                        if light > 1000:
                            light = 1000
                    else:
                        light = 1000

                    #print(iA,iD,iS)



                    R.append([i,j,k,colorStr,z,str(sX)+str(sY)+str(sR),light])

                    k = k + 1

        R = sorted(R,key=operator.itemgetter(4))

        for q in range (0,len(R)):
            i = R[q][0]
            j = R[q][1]
            k = R[q][2]
            colorStr = R[q][3]
            z = R[q][4]
            place = R[q][5]
            l = R[q][6]/1000

            A = list(colors.hex2color(colorStr))
            for ii in range(0,len(A)):
                A[ii] = A[ii]*l
            true_color = colors.rgb2hex(tuple(A))

            self.canvas.create_polygon(self.surface.SurfaceListT[i][j].X, self.surface.SurfaceListT[i][j].Y,
                                       self.surface.SurfaceListT[i][j + 1].X, self.surface.SurfaceListT[i][j + 1].Y,
                                       self.surface.SurfaceListT[i + 1][j + 1].X,
                                       self.surface.SurfaceListT[i + 1][j + 1].Y,
                                       self.surface.SurfaceListT[i + 1][j].X, self.surface.SurfaceListT[i + 1][j].Y,
                                       fill=true_color, outline="#000000",
                                       tags="polygon" + " " + str(k) + " "+place+ " " + str(z)+" "+str(l))



        i = 0
        for A in self.surface.ST:
            j = 0
            for B in A:
                self.canvas.create_oval(B.X - 4, B.Y + 4, B.X + 4, B.Y - 4, tags=str(i) + " " + str(j),
                                        activefill="#ffffff", fill="#000000")
                j = j + 1
            i = i + 1
        if self.useLighting:
            src = self.projNOROT(self.LightSource)
            self.canvas.create_rectangle(src.X - 5, src.Y + 5, src.X + 5, src.Y - 5,
                                         tags="Light" + " " + str(self.LightIntensity), activefill="#b2ff36",
                                         fill="#000000")




    #Поиск точки, делящей отрезок AB в отношении arg
    def lerp3D(self, pointA, pointB, arg):
        temp = tkPoint3D(pointA.X + arg * (pointB.X - pointA.X), pointA.Y + arg * (pointB.Y - pointA.Y),pointA.Z + arg * (pointB.Z - pointA.Z))
        return temp


    # Алгоритм де Кастельжо
    def bezline(self, arr, arg):
        temp = []
        for i in range(len(arr) - 1):
            temp.append(self.lerp3D(arr[i], arr[i + 1], arg))
        if len(arr) == 2:
            self.global_temp.append(temp[0])
        else:
            self.bezline(temp, arg)


    def generate_bezfield(self):
        self.surface.SurfaceList = []
        Bezlist = []
        for i in range(0,self.surface.M):


            t = 0
            while t<1:
                self.bezline(self.surface.S[i],t)
                t = t + 0.05
            Bezlist.append(self.global_temp)
            self.global_temp = []

        for j in range (0,len(Bezlist[0])):
            temp = []
            for i in range (0,self.surface.M):
                temp.append(Bezlist[i][j])
            t = 0
            while t<1:
                self.bezline(temp,t)
                t = t + 0.05
            self.surface.SurfaceList.append(self.global_temp)
            self.global_temp = []



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

        self.canvas = Canvas(self.top, bg="white", width=2560, height=1020)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.mouseGrabLine)  # Создание новой точки

        self.canvas.focus_set()
# Режим создания отрезков
    def modeLine(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<ButtonPress-1>", self.mouseGrabLine)  # Создание новой точки
# Режим создания сечения
    def modeSect(self):

        if self.fin:
            self.ClearSec()

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
        w = 2560
        h = 1020

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
        self.style.theme_use("clam")
        self.config(bg="white")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        menubar.add_command(label="Новый объект", command=self.onNewObject)
        menubar.add_command(label="Диметрия", command=self.onDimetry)
        menubar.add_command(label="Изометрия", command=self.onIsometry)
        menubar.add_command(label="Кривая Безье", command=self.onBezline)
        menubar.add_command(label="Поверхность Безье", command=self.onBezsect)
        menubar.add_command(label="Отсечение отрезков", command=self.onSection)

    def onSection(self):
        newSect = SectWin(self)
        return

    def onBezline(self):
        newBez = BezField(self)
        return


    def onBezsect(self):
        newBez = BezSect(self)
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
