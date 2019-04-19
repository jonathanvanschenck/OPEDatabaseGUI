import tkinter as tk
from time import localtime

defaultUser = "JVS"
materialOpts = {"JVS":["ADT","Xyl","Red Pig","Pc"],
                "GG":["Xyl","ADT","Red Pig","Pc"],
                "NQ":["Pc","Xyl","ADT","Red Pig"]}[defaultUser]
submaterialOpts = {"ADT":["TES","TSBS","TBDMS"],
                   "Pc":["TIPS-F8","TCHS-F8","TIPS"],
                   "Xyl":["Xyl","Lab Grade","Wild Type"]}
phaseOpts = ["Solution","Film (Isolated)","Film (Agg. Amorphus)","Film (PolyCrys)","Crystal"]
deviceOpts = {"Solution":["CB","Tol","DMSO","Ace","IPA","DIWater"],
              "Film (Isolated)":["PMMA","PS","CNC","Cavity"],
              "Film (Agg. Amorphus)":["PMMA","PS","CNC"],
              "Film (PolyCrys)":["PMMA","Cavity","Dropcast"],
              "Crystal":["Dropcast"]}
mtypeOpts = ["Absorption","PL","IV"]
msubtypeOpts = {"Absorption":["Pol-Dep","Temp-Dep"],
                "PL":["Pol-Dep","Angle-Dep","Temp-Dep","Time-Dep"],
                "Reflectance":["Angle-Dep"],
                "IV":[]}
noteOpts = {\
"Absorption":\
"""Wavelength Range: 400-1000nm
Light Source:
IT: 
Aves:
""",
"PL":\
"""Wavelength Range: ???-1000 nm
Laser Used:
Laser Power: 
Spot Size: 
IT: 
Aves:
"""}
noteOptssub = {\
"Temp-Dep":"Temp Range (steps): \n",
"Pol-Dep":"Pol Range (steps): \n",
"Angle-Dep":"AOI range (steps): \n"}


class widget:
    def __init__(self,master,**kwargs):
        self.frame = tk.LabelFrame(master,text="Metadata")
        self.frame.grid(**kwargs)
        self.createWidgets()
        
    def __call__(self):
        dic = {"creator":self.creator_md.get(),
               "date":int(self.date_md.get()),
               "material":self.material_md.get(),
               "submaterial":self.submaterial_md.get(),
               "phase":self.phase_md.get(),
               "device_host":self.device_md.get(),
               "measurement_type":self.mtype_md.get(),
               "measurement_subtype":self.msubtype_md.get(),
               "experimental_notes":self.noteText.get(1.0,tk.END),
               "data_notes":self.dnoteText.get(1.0,tk.END)}
        return dic

        
    def createWidgets(self):
        # Creator
        self.creator_md = tk.StringVar()
        self.creator_md.set(defaultUser)
        self.creatorFrame = tk.LabelFrame(self.frame,
                                          text="Creator:")
        self.creatorFrame.grid(row=0,column=0)
        self.creatorEntry = tk.Entry(self.creatorFrame,
                                     textvariable=self.creator_md,
                                     width=10)
        self.creatorEntry.grid(row=0,column=0)
        # Date
        self.date_md = tk.StringVar()
        t = localtime()
        self.date_md.set("{0}{1:0>2}{2:0>2}".format(str(t.tm_year)[-2:],
                                                      t.tm_mon,
                                                      t.tm_mday))
        self.dateFrame = tk.LabelFrame(self.frame,
                                          text="Date:")
        self.dateFrame.grid(row=1,column=0)
        self.dateEntry = tk.Entry(self.dateFrame,
                                  textvariable=self.date_md,
                                  width=10)
        self.dateEntry.grid(row=0,column=0)
        # Material
        self.material_md = tk.StringVar()
        self.materialFrame = tk.LabelFrame(self.frame,
                                           text="Material:")
        self.materialFrame.grid(row=3,column=0)
        self.materialClass = optionOther(self.materialFrame,
                                         self.material_md,
                                         materialOpts)
        # subMaterial
        self.submaterial_md = tk.StringVar()
        self.submaterialFrame = tk.LabelFrame(self.frame,
                                              text="Submaterial:")
        self.submaterialFrame.grid(row=3,column=1)
        self.constructSubmaterial()
        self.material_md.trace_variable("w",lambda *args: self.constructSubmaterial())
        # Phase
        self.phase_md = tk.StringVar()
        self.phaseFrame = tk.LabelFrame(self.frame,
                                           text="Phase:")
        self.phaseFrame.grid(row=4,column=0)
        self.phaseClass = optionOther(self.phaseFrame,
                                         self.phase_md,
                                         phaseOpts)        
        # Device
        self.device_md = tk.StringVar()
        self.deviceFrame = tk.LabelFrame(self.frame,
                                              text="Device/Host:")
        self.deviceFrame.grid(row=4,column=1)
        self.constructDevice()
        self.phase_md.trace_variable("w",lambda *args: self.constructDevice())
        # measurement_type
        self.mtype_md = tk.StringVar()
        self.mtypeFrame = tk.LabelFrame(self.frame,
                                           text="Measurement Type:")
        self.mtypeFrame.grid(row=5,column=0)
        self.mtypeClass = optionOther(self.mtypeFrame,
                                      self.mtype_md,
                                      mtypeOpts)        
        # measurement_subtype
        self.msubtype_md = tk.StringVar()
        self.musubtypeFrame = tk.LabelFrame(self.frame,
                                              text="Measurement Keywords:")
        self.musubtypeFrame.grid(row=5,column=1)
        self.constructmsubtype()
        self.mtype_md.trace_variable("w",lambda *args: self.constructmsubtype())
        # Notes
        self.noteFrame = tk.LabelFrame(self.frame,
                                       text="Experimental Notes")
        self.noteFrame.grid(row=3,column=2)
        self.noteButton = tk.Button(self.noteFrame,text="Generate Template",
                                    command=self.genNoteTemplate)
        self.noteButton.grid(row=0,column=0,sticky=tk.W)
        self.noteText = tk.Text(self.noteFrame,
                                width=30,height=6)
        self.noteText.grid(row=1,column=0)
        # DNotes
        self.dnoteFrame = tk.LabelFrame(self.frame,
                                       text="Data Structure Notes")
        self.dnoteFrame.grid(row=4,column=2)
        self.dnoteText = tk.Text(self.dnoteFrame,
                                width=30,height=6)
        self.dnoteText.grid(row=0,column=0)
        
    def genNoteTemplate(self):
        try:
            t = noteOpts[self.mtype_md.get()]
        except KeyError:
            t = "\n"
        for key in self.msubtype_md.get().split(","):
            try:
                t += noteOptssub[key]
            except KeyError:
                pass
        self.noteText.delete(1.0,tk.END)
        self.noteText.insert(1.0,t)
    
    def constructSubmaterial(self):
        try:
            self.submaterialClass.forget()
        except AttributeError:
            pass
        try:
            mat = submaterialOpts[self.material_md.get()]
        except KeyError:
            mat = []
        self.submaterialClass = optionOther(self.submaterialFrame,
                                             self.submaterial_md,
                                             mat)
    def constructDevice(self):
        try:
            self.deviceClass.forget()
        except AttributeError:
            pass
        try:
            mat = deviceOpts[self.phase_md.get()]
        except KeyError:
            mat = []
        self.deviceClass = optionOther(self.deviceFrame,
                                         self.device_md,
                                         mat)

    def constructmsubtype(self):
        try:
            self.msubtypeClass.forget()
        except AttributeError:
            pass
        try:
            mat = msubtypeOpts[self.mtype_md.get()]
        except KeyError:
            mat = []
        self.msubtypeClass = listOther(self.musubtypeFrame,
                                         self.msubtype_md,
                                         mat)
        
class optionOther:
    def __init__(self,master,var,opts=[]):
        self.var = var
        self.opts = opts
        try:
            self.var.set(self.opts[0])
        except IndexError:
            self.var.set("")
        self.buttons = len(opts)*[""]
        for i in range(len(opts)):
            self.buttons[i] = tk.Radiobutton(master,text=opts[i],
                                             variable=var,value=opts[i])
            self.buttons[i].grid(row=i,column=0,sticky=tk.W)
        self.cbVal = tk.IntVar()
        self.cbVal.set(int(len(opts)==0))
        self.cb = tk.Checkbutton(master,text="Other:",
                                 variable=self.cbVal,
                                 command=self.toggle,
                                 onvalue=1,offvalue=0)
        self.cb.grid(row=len(opts),column=0,sticky=tk.W)
        self.otherEntry = tk.Entry(master,textvariable=var)
        self.otherEntry.grid(row=len(opts)+1,column=0,sticky=tk.W)
        self.otherEntry.config(state=["disabled","normal"][self.cbVal.get()])
    
    def toggle(self):
        for b in self.buttons:
            b.config(state=["normal","disabled"][self.cbVal.get()])
        self.otherEntry.config(state=["disabled","normal"][self.cbVal.get()])
        if not self.cbVal.get():
            self.var.set(self.opts[0])
        
    def forget(self):
        for b in self.buttons:
            b.grid_forget()
        self.cb.grid_forget()
        self.otherEntry.grid_forget()
        self.var.set("")


class listOther:
    def __init__(self,master,var,opts=[]):
        self.var = var
        self.opts = opts
        self.var.set("")
        self.buttonState = [tk.IntVar() for _ in range(len(opts))]
        for bs in self.buttonState:
            bs.set(0)
            bs.trace_variable("w",lambda *args: self.update())
        self.buttons = [tk.Checkbutton(master,variable=bs) for bs in self.buttonState]
        for i in range(len(opts)):
            self.buttons[i].grid(row=i,column=0,sticky=tk.W)
            self.buttons[i].config(text=opts[i])
        self.otherLabel = tk.Label(master,text="Other (comma seperated):")
        self.otherLabel.grid(row=len(opts),column=0,sticky=tk.W)
        self.eVal = tk.StringVar()
        self.eVal.set("")
        self.eVal.trace_variable("w",lambda *args: self.update())
        self.otherEntry = tk.Entry(master,textvariable=self.eVal)
        self.otherEntry.grid(row=len(opts)+1,column=0,sticky=tk.W)
        self.listText = tk.Text(master,width=20,height=3)
        self.listText.grid(row=len(opts)+2,column=0,sticky=tk.W)
        self.listText.config(state="disabled")
        self.update()

    def update(self):
        t = ",".join([self.opts[i] for i in range(len(self.opts)) if self.buttonState[i].get()])
        if (self.eVal.get()) != "":
            if len(t)!=0:
                t += ","
            t+=self.eVal.get()
        self.var.set(t)
        self.listText.config(state="normal")
        self.listText.delete(1.0,tk.END)
        self.listText.insert(tk.END,t)
        self.listText.config(state="disabled")
        
    def forget(self):
        for b in self.buttons:
            b.grid_forget()
        self.otherLabel.grid_forget()
        self.otherEntry.grid_forget()
        self.listText.grid_forget()
        self.eVal.set("")
        self.var.set("")