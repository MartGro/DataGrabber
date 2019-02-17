import tkinter
from PIL import ImageDraw, Image, ImageTk


class App:
    def __init__(self, master):

        image = Image.open("polschuh_p2_2.png")
        basewidth = 1000
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)

        frame = tkinter.Frame(master)
        frame.pack()

        self.canvas = tkinter.Canvas(frame, width=image.size[0], height=image.size[1])
        self.canvas.pack(side=tkinter.RIGHT)
        self.image_tk = ImageTk.PhotoImage(image)

        self.origin = tkinter.Button(frame, text="Origin", fg="red", command=self.set_origin)
        self.origin.pack(side=tkinter.TOP)

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



        self.y_tuple = tkinter.Button(frame, text="y - axis", command=self.set_y_axis)
        self.y_tuple.pack(side=tkinter.TOP)

        self.y_entry = tkinter.Entry(frame, width=5)
        self.y_entry.pack(side=tkinter.TOP)
        self.y_entry.insert(0, "1")


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

        self.y_tuple = (1, 1)

    def xy_callback(self, event):
        self.check_listeners(event.x, event.y)
        print("clicked at: x -> {}; y -> {}".format(event.x, event.y))

    def check_listeners(self, input_x, input_y):
        if self.listen_origin == True:
            self.origin = (input_x, input_y)
            print("Origin set to x -> {}; y -> {}".format(input_x, input_y))
            self.listen_origin = False

        elif self.listen_xaxis_1 == True:
            s = self.x_entry_1.get()
            self.x_tuple_1 = (input_x, input_y, s)
            print("XPoint 1:{},{} with value {}".format(self.x_tuple_1[0], self.x_tuple_1[1], self.x_tuple_1[2]))
            self.listen_xaxis_1 = False

        elif self.listen_xaxis_2 == True:
            s = self.x_entry_2.get()
            self.x_tuple_2 = (input_x, input_y, s)
            print("XPoint 2:{},{} with value {}".format(self.x_tuple_2[0], self.x_tuple_2[1], self.x_tuple_2[2]))
            self.listen_xaxis_2 = False

        self.calculate_x_scaling()


    def calculate_x_scaling(self):
        x1 = self.x_tuple_1[0]
        x2 = self.x_tuple_2[0]

        self.x_axis_y_component = (self.x_tuple_1[1]+self.x_tuple_2[1])/2


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


root = tkinter.Tk()
app = App(root)
root.mainloop()
root.destroy()
