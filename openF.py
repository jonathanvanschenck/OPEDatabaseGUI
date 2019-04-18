import tkinter as tk
import os
from tkinter import filedialog


class widget:
    def __init__(self,master,**kwargs):
        self.frame = tk.LabelFrame(master,text="Select File(s)")
        self.frame.grid(**kwargs)
        self.createWidgets()
        
    def createWidgets(self):
        
        self.files = []
        self.selectButton = tk.Button(self.frame,
                                      text="Open:",
                                      justify=tk.RIGHT,
                                      command=self.select)
        self.selectButton.grid(row=0,column=0)
        self.filenameText = tk.Text(self.frame,
                                    width=40,height=4)
        self.filenameText.config(state="disabled")
        self.filenameText.grid(row=0,column=1)
        
        self.dir = tk.StringVar()
        self.dir.set("")
        self.dirButton = tk.Button(self.frame,
                                   text="Directory:",
                                   justify=tk.RIGHT,
                                   command=self.dirSelect)
        self.dirButton.grid(row=1,column=0)
        self.dirLabel = tk.Label(self.frame,
                                 textvariable=self.dir,
                                 justify=tk.LEFT)
        self.dirLabel.grid(row=1,column=1)
        
        
    def select(self):
        self.filenameText.config(state="normal")
        self.filenameText.delete(1.0,tk.END)
        self.files = []
        t = filedialog.askopenfilenames(title="Select File(s)")
        if len(t) == 0:
            return None
        self.files = list(t)
        for f in self.files:
            self.filenameText.insert(tk.END,"..."+f[-36:]+"\n")
        self.filenameText.config(state="disabled")
        directory = set([os.path.dirname(f) for f in self.files])
        assert len(directory)==1, "Inconsistent file home directory"
        self.dir.set(directory.pop())
        return None
        
    def dirSelect(self):
        directory = filedialog.askdirectory(title="Select Directory to Save File(s)")
        if type(directory) != type(()):
            self.dir.set(directory)
        