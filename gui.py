from tkinter import *
import apihandle


class Application(Frame):
    """Applications main window"""

    def __init__(self, master):
        super().__init__()

        # Setting main window widgets
        self.master = master
        self.master.title('CBR Rates')
        self.master.geometry('300x300')
        self.master.resizable(0, 0)
        self.main_frame = Frame(self.master, bg='GREY')
        self.main_frame.pack(fill=BOTH, expand=True)
        self.widgets()

    def widgets(self):
        """Applications main widgets"""

        ent_day = Entry(self.main_frame)
        ent_day.pack(side=LEFT, padx=(0, 1))

        ent_mon = Entry(self.main_frame)
        ent_mon.pack(side=LEFT, padx=(0, 1))

        ent_year = Entry(self.main_frame)
        ent_year.pack(side=LEFT, padx=(0, 1))

        # lst_curr = OptionMenu(self.main_frame, DEFAULT)
        # lst_curr.pack()
        #
        # btn_fetch = Button(self.main_frame, text='Update')
        # btn_fetch.pack()


def start_app():

    root = Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    start_app()
