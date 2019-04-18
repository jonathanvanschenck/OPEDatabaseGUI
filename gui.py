# -*- coding: utf-8 -*-
"""
GUI to save and search database
"""


import tkinter as tk
from tkinter import messagebox
import openF as GopenF
import metadata as Gmeta
import saveF as GsaveF
import databaseBackend as DB


class App(tk.Frame):
    def __init__(self,root=None):
        tk.Frame.__init__(self,root)
        self.root = root
        self.grid(row=0,column=0)
        self.db = DB.Database()
        self.createWidgets()
        
    def createWidgets(self):
        self.openF = GopenF.widget(self,row=0,column=0)
        self.meta = Gmeta.widget(self,row=1,column=0)
        self.saveF = GsaveF.widget(self,self.openF,self.meta,self.db,
                                   row=2,column=0)
        self.print = tk.Button(self,text="print",command=lambda :print(self.meta()))
        self.print.grid(row=3)


    def commitChanges(self):
        if messagebox.askyesno("Close", "Commit Changes to database?"):
            self.db.commit()
        self.root.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.root.title("OPE Database")
    app.root.protocol('WM_DELETE_WINDOW', app.commitChanges)
    app.mainloop()