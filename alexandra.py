"""
A Python tool for grabbing history screenshots from FL Studio and converting them into a flexible history tool.

Built by Tayo Castro for Zakk Myer.
Copyright 2023 new underground media brigade.
See license for complete copyright details.
"""

import datetime
import os
import io
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog

import numpy as np
import pandas as pd
import pyautogui
import pytesseract
import PIL


"""
CONFIG
"""
"""
CONFIGURATION
"""
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
FUNCTIONS
"""
def text_capture(x1, y1, x2, y2):
    """
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = datetime.datetime.now().strftime("%f")
    image.save("temp/" + file_name + ".png")
    imgarray = np.array(PIL.Image.open("temp/" + file_name + ".png"))
    os.remove("temp/" + file_name + ".png") # This removes the temporary file that was created for processing
    text = pytesseract.image_to_string(imgarray)
    return text

def text_formatter(input_text):
    # This one is fully my function; NOT a class method. Formats a string buffer into a dataframe.
    print(input_text)
    return(input_text.strip())
"""
CLASSES
"""

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
        self.history_buffer = None


        root.geometry('300x500+1200+200')  # set new geometry
        root.title('Alexandra') # Window title
        root.iconbitmap(r'Alexandra.ico') # Window icon

        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(expand=tk.TRUE, fill=tk.BOTH)

        self.buttonBar = tk.Frame(self.menu_frame, bg="")
        self.buttonBar.pack(side=tk.TOP)

        self.table_frame = tk.Frame(self.menu_frame)
        self.table_frame.pack()

        self.snipButton = tk.Button(self.buttonBar, width=7, height=2, command=self.create_screen_canvas, # pretty sure this command needs editing
                                    text="Capture", background="gray")
        self.snipButton.grid(row=0, column=0, sticky="w")

        self.findButton = tk.Button(self.buttonBar, width=16, height=2, text="Find and Replace...")
        self.findButton.grid(row=0, column=1, sticky="w")

        self.saveButton = tk.Button(self.buttonBar, width=7, height=2, command=self.save_history, text="Save As...")
        self.saveButton.grid(row=0,column=3, sticky="w")

        self.history_text = st.ScrolledText(self.table_frame, height=20, width=25) # This turns the instantiated class attribute into a pandastable
        self.history_text.pack()

        self.master_screen = tk.Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = tk.Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=tk.BOTH, expand=tk.YES)


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

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        """
        :param event: mouse drag
        :return:
        """
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def on_button_release(self, event):
        # activated on release - should do exception checking here
        try:
            if self.start_x <= self.current_x and self.start_y <= self.current_y:
                self.history_buffer = text_capture(self.start_x, self.start_y, self.current_x - self.start_x,
                                            self.current_y - self.start_y)

            elif self.start_x >= self.current_x and self.start_y <= self.current_y:
                self.history_buffer = text_capture(self.current_x, self.start_y, self.start_x - self.current_x,
                                            self.current_y - self.start_y)

            elif self.start_x <= self.current_x and self.start_y >= self.current_y:
                self.history_buffer = text_capture(self.start_x, self.current_y, self.current_x - self.start_x,
                                            self.start_y - self.current_y)

            elif self.start_x >= self.current_x and self.start_y >= self.current_y:
                self.history_buffer = text_capture(self.current_x, self.current_y, self.start_x - self.current_x,
                                            self.start_y - self.current_y)

            self.exit_screenshot_mode()

        except FloatingPointError: # This isn't the error I want to be capturing, but we're getting closer
            print(FloatingPointError)
            print("Error capturing history, please try again")
            self.exit_screenshot_mode()
            self.create_screen_canvas()

        return event

    def exit_screenshot_mode(self):
        """
        Destroys the screencap mode, and shows the table
        :return:
        """
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify() # Pulls the root window out.
        self.history_text.insert(tk.END, self.history_buffer)

    def find_and_replace(self):
        """
        For finding and replacing specific instances of words with user generated substitutes.
        :return:
        """

    def save_history(self):
        """
        Should save all the text. This still needs to be built out.
        :return:
        """
        filename = tkinter.filedialog.asksaveasfilename(filetypes=[('Text Document', '*.txt')],
                                                        defaultextension=[('Text Document', '*.txt')])
        text_file = open(filename, "w")
        text_file.write(self.history_text.get('1.0', 'end-1c'))
        text_file.close()



if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()