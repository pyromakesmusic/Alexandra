"""
A Python tool for grabbing history screenshots from FL Studio and converting them into a flexible history tool.
Copyright 2023 new underground media brigade
See license for complete copyright details.
"""

import datetime
import os
import io
import tkinter as tk
import numpy as np
import pandas as pd
import pandastable as pt
import pyautogui
import pytesseract
import PIL

def text_capture(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = datetime.datetime.now().strftime("%f")
    image.save("temp/" + file_name + ".png") # want to remove this line and instead feed into pytesseract.
    imgarray = np.array(PIL.Image.open("temp/" + file_name + ".png"))
    os.remove("temp/" + file_name + ".png")
    text = pytesseract.image_to_string(imgarray)
    text_df = pd.read_csv(io.StringIO(text))
    text_df_revised = text_df.fillna("")
    text_table = text_df_revised.squeeze()
    print(text_table)
    return(text_table)


class Application():
    """
    Tkinter main loop.
    """
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.history = None # I added this. This is a history dataframe - not the table object based on it.

        root.geometry('300x50+200+200')  # set new geometry
        root.title('Alexandra') # Window title
        root.iconbitmap(r'Alexandra.ico') # Window icon

        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.buttonBar = tk.Frame(self.menu_frame, bg="")
        self.buttonBar.grid(row=0, column=0, sticky="n")

        self.snipButton = tk.Button(self.buttonBar, width=6, height=8, command=self.create_screen_canvas, background="red")
        self.snipButton.grid(row=0, column=1, sticky="n")

        self.master_screen = tk.Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = tk.Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=tk.BOTH, expand=tk.YES)


        self.history_table = pt.Table(self.menu_frame, dataframe=self.history, showtoolbar=False, showstatusbar=False)
        self.history_table.grid(row=0, column=1)

    def create_screen_canvas(self):
        """
        Initializes the snipping surface.
        :return:
        """
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = tk.Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=tk.BOTH, expand=tk.YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            self.history = text_capture(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            self.history = text_capture(self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            self.history = text_capture(self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            self.history = text_capture(self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)

        self.exit_screenshot_mode()

        return event

    def exit_screenshot_mode(self):
        """
        Destroys the screencap mode.
        :return:
        """
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

        self.history_table.show()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        """
        This can stay unchanged for now.
        :param event:
        :return:
        """
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)



if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()