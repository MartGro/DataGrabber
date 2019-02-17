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

        self.origin = tkinter.Button(frame, text="Origin", fg="red", command=self.set_origin)
        self.origin.pack(side=tkinter.LEFT)

        self.xaxis = tkinter.Button(frame, text="x - axis", command=self.set_x_axis)
        self.xaxis.pack(side=tkinter.LEFT)

        self.x_entry = tkinter.Entry(frame, width=5)
        self.x_entry.pack(side=tkinter.LEFT)
        self.x_entry.insert(0, "1")

        self.yaxis = tkinter.Button(frame, text="y - axis", command=self.set_y_axis)
        self.yaxis.pack(side=tkinter.LEFT)

        self.y_entry = tkinter.Entry(frame, width=5)
        self.y_entry.pack(side=tkinter.LEFT)
        self.y_entry.insert(0, "1")

        self.canvas = tkinter.Canvas(frame, width=image.size[0], height=image.size[1])
        self.canvas.pack()
        self.image_tk = ImageTk.PhotoImage(image)

        # Prevents garbage collection
        # root.image_tk = image_tk
        self.canvas.create_image(image.size[0] // 2, image.size[1] // 2, image=self.image_tk)
        self.canvas.bind("<Button-1>", self.xy_callback)

        self.listen_origin = False
        self.listen_xaxis = False
        self.listen_yaxis = False

        self.origin = (0, 0)
        # 1 Pixel, 1 Unit
        self.xaxis = (1, 1)
        self.yaxis = (1, 1)

    def xy_callback(self, event):
        self.check_listeners(event.x, event.y)
        print("clicked at: x -> {}; y -> {}".format(event.x, event.y))

    def check_listeners(self, input_x, input_y):
        if self.listen_origin == True:
            self.origin = (input_x, input_y)
            print("Origin set to x -> {}; y -> {}".format(input_x, input_y))
            self.listen_origin = False

        elif self.listen_xaxis == True:
            diff_x = input_x - self.origin[0]
            self.xaxis = (diff_x, self.xaxis[1])
            print("Set xdiff to {} with scaling {}".format(diff_x, self.xaxis[1]))
            self.listen_xaxis = False

    def set_origin(self):
        self.listen_origin = True
        print("Set Origin")

    def set_x_axis(self):
        self.listen_xaxis = True
        print("Set xax")

    def set_y_axis(self):
        self.listen_yaxis = True
        print("Set yax")


root = tkinter.Tk()
app = App(root)
root.mainloop()
root.destroy()
