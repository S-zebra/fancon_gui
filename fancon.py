#!/usr/bin/env python3.10

from tkinter import *
import os
import subprocess

SMC_PATH = "/usr/local/bin/smc"

class FanController(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.smc_util = SmcUtil(SMC_PATH)


        self.chkbox_val = IntVar(self)
        self.chkbox_val.set(1 if self.smc_util.is_manual() else 0)
        self.checkbox = Checkbutton(self, text="Manual", variable=self.chkbox_val, onvalue=1, offvalue=0, command=self.toggle_manual)
        self.checkbox.pack()

        self.scale = Scale(self, from_=1200, to=6500, orient=HORIZONTAL, command=self.on_scroll)
        self.scale.pack()

        if self.chkbox_val.get() == 0: # if auto
            self.scale.config(state=DISABLED)


    def on_scroll(self, event=None):
        self.smc_util.set_speed(self.scale.get())

    def toggle_manual(self, event=None):
        if self.chkbox_val.get() == 0:
            self.smc_util.set_auto()
            self.scale.config(state=DISABLED)
        else:
            self.smc_util.set_manual()
            self.smc_util.set_speed(self.scale.get())
            self.scale.config(state=NORMAL)

class SmcUtil:
    def __init__(self, smc_path):
        self.smc_path = smc_path

    def is_manual(self):
        p = subprocess.run([self.smc_path, "-r", "-k", "FS! "], capture_output=True)
        return p.stdout.decode()[16] == '1'

    def set_auto(self):
        os.system(self.smc_path + " -k 'FS! ' -w 0000")

    def set_manual(self):
        os.system(self.smc_path + " -k 'FS! ' -w 0001")

    def get_speed(self):
        p = subprocess.run([self.smc_path, "-r", "-k", "F0Tg"], capture_output=True)
        return int(p.stdout.decode()[16:19])

    def set_speed(self, speed):
        # speed = 1200 .. 6500
        speed_hex = hex(speed<<2)[2:]
        os.system(self.smc_path + " -k 'F0Tg' -w " + speed_hex)

if __name__ == "__main__":
    app = FanController()
    app.mainloop()

