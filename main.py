import tkinter
from PIL import ImageDraw, Image, ImageTk
import os
import math

class App:
    def __init__(self, master):

        image = Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"polschuh_p2_2.png"))
        basewidth = 1000
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)

        frame = tkinter.Frame(master)
        frame.pack()

        self.canvas = tkinter.Canvas(frame, width=image.size[0], height=image.size[1])
        self.canvas.pack(side=tkinter.RIGHT)
        self.image_tk = ImageTk.PhotoImage(image)

        self.x_tuple_1 = tkinter.Button(frame, text="x - axis point 1", command=self.set_x_axis_1)
        self.x_tuple_1.pack(side=tkinter.TOP)

        self.x_entry_1 = tkinter.Entry(frame, width=5)
        self.x_entry_1.pack(side=tkinter.TOP)
        self.x_entry_1.insert(0, "1")

        self.x_tuple_2 = tkinter.Button(frame, text="x - axis point 2", command=self.set_x_axis_2)
        self.x_tuple_2.pack(side=tkinter.TOP)

        self.x_entry_2 = tkinter.Entry(frame, width=5)
        self.x_entry_2.pack(side=tkinter.TOP)
        self.x_entry_2.insert(0, "1")

        self.x_axis_log = tkinter.IntVar()
        self.x_log_button = tkinter.Checkbutton(frame, text="x-axis logarithmic", variable = self.x_axis_log,command=self.set_x_axis_log)
        self.x_log_button.pack(side=tkinter.TOP)



        self.y_tuple = tkinter.Button(frame, text="y - axis", command=self.set_y_axis)
        self.y_tuple.pack(side=tkinter.TOP)

        self.y_entry = tkinter.Entry(frame, width=5)
        self.y_entry.pack(side=tkinter.TOP)
        self.y_entry.insert(0, "1")


        self.cla = tkinter.Button(frame, text="Clear ALL values", command=self.clear_values)
        self.cla.pack(side=tkinter.TOP)

        self.clv = tkinter.Button(frame, text="Clear last value", command=self.clear_one)
        self.clv.pack(side=tkinter.TOP)

        self.textfield = tkinter.Text(frame,width = 25,height = 25)
        self.textfield.pack(side=tkinter.TOP)


        # Prevents garbage collection
        # root.image_tk = image_tk
        self.canvas.create_image(image.size[0] // 2, image.size[1] // 2, image=self.image_tk)
        self.canvas.bind("<Button-1>", self.xy_callback)

        self.listen_origin = False

        self.listen_xaxis_1 = False
        self.listen_xaxis_2 = False

        self.listen_yaxis = False

        self.origin = (0, 0)
        # xval,yval,val
        self.x_tuple_1 = (0, 0, 1)
        self.x_tuple_2 = (0, 0, 1)
        self.x_axis_y_component = 0
        self.x_axis_log_val = False

        self.a_x = 1
        self.b_x = 0

        self.y_tuple = (1, 1)

        self.values = []

        self.update_view = tkinter.Button(frame, text="Update Values", command=self.update_textfield())
        self.update_view.pack(side=tkinter.TOP)


    def x_from_pixel(self,x_pixel):
        if self.x_axis_log_val == 0:
            return self.a_x*x_pixel+self.b_x
        else:
            return math.exp(self.a_x*x_pixel+self.b_x)

    def xy_callback(self, event):
        self.check_listeners(event.x, event.y)
        print("clicked at: x -> {}; y -> {}".format(self.x_from_pixel(event.x), event.y))
        self.update_textfield()

    def check_listeners(self, input_x, input_y):
        if self.listen_origin == True:
            self.origin = (input_x, input_y)
            print("Origin set to x -> {}; y -> {}".format(input_x, input_y))
            self.listen_origin = False


        elif self.listen_xaxis_1 == True:
            s = float(self.x_entry_1.get())
            self.x_tuple_1 = (input_x, input_y, s)
            print("XPoint 1:{},{} with value {}".format(self.x_tuple_1[0], self.x_tuple_1[1], self.x_tuple_1[2]))
            self.listen_xaxis_1 = False

        elif self.listen_xaxis_2 == True:
            s = float(self.x_entry_2.get())
            self.x_tuple_2 = (input_x, input_y, s)
            print("XPoint 2:{},{} with value {}".format(self.x_tuple_2[0], self.x_tuple_2[1], self.x_tuple_2[2]))
            self.listen_xaxis_2 = False

        else:
            self.values.append((input_x,input_y))
            self.update_textfield()



    def calculate_x_scaling(self):
        x1 = self.x_tuple_1[0]
        x2 = self.x_tuple_2[0]

        if self.x_axis_log_val == 1:
            try:
                x_1_val = math.log(self.x_tuple_1[2])
                x_2_val = math.log(self.x_tuple_2[2])
            except ValueError:
                print("Log scaling with invalid points")
        else:
            x_1_val = self.x_tuple_1[2]
            x_2_val = self.x_tuple_2[2]

        self.x_axis_y_component = (self.x_tuple_1[1]+self.x_tuple_2[1])/2

        try:
            self.a_x = (x_2_val-x_1_val)/(x2-x1)
            self.b_x = x_1_val-self.a_x*x1
        except ZeroDivisionError:
            print("X axis points are at the same coordinate")
        except UnboundLocalError:
            print("There is a problem with the x-coordinate points, please reset")



    def update_textfield(self):
        self.calculate_x_scaling()
        self.textfield.delete('1.0', tkinter.END)
        for i in range(len(self.values)):
            self.textfield.insert("{}.0".format(i + 1),
                                  "{0: >#010.4f};{1: >#010.4f}\n".format(self.x_from_pixel(self.values[i][0]),
                                                                         self.values[i][1]))
            #self.textfield.insert("{}.0".format(i + 1),
            #                      "{};{}\n".format(round(self.x_from_pixel(self.values[i][0]),10),
            #                                                             round(self.values[i][1],10)))

    def set_origin(self):
        self.listen_origin = True
        print("Set Origin")

    def set_x_axis_1(self):
        self.listen_xaxis_1 = True
        print("Set xax1")

    def set_x_axis_2(self):
        self.listen_xaxis_2 = True
        print("Set xax2")


    def set_y_axis(self):
        self.listen_yaxis = True
        print("Set yax")

    def set_x_axis_log(self):
        self.x_axis_log_val = self.x_axis_log.get()
        print("X-axis log:{}".format(self.x_axis_log_val))

    def clear_values(self):
        self.values = []
        self.update_textfield()

    def clear_one(self):
        self.values = self.values[:-1]
        self.update_textfield()


root = tkinter.Tk()
app = App(root)
root.mainloop()
root.destroy()
