# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import os
from shutil import copy
import json
import datetime as dt
import glob

class dtEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return {
                "_type": "datetime",
                "value": "{},{},{},{},{},{},{}".format(obj.year,
                                                       obj.month,
                                                       obj.day,
                                                       obj.hour,
                                                       obj.minute,
                                                       obj.second,
                                                       obj.microsecond)
            }
        return super(dtEncoder, self).default(obj)

class dtDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'datetime':
            return dt.datetime(*[int(i) for i in obj["value"].split(",")])
        return obj


class widget:
    def __init__(self,master,openF,meta,db,**kwargs):
        self.db = db
        self.frame = tk.LabelFrame(master,text="Save Header")
        self.frame.grid(**kwargs)
        self.openF = openF
        self.meta = meta
        self.createWidgets()

    def createWidgets(self):
        # a
        self.saveButton = tk.Button(self.frame,text="Save Header Only",
                                    command=lambda : self.save(move=False))
        self.saveButton.grid(row=0)
        self.saveButton = tk.Button(self.frame,text="Save Header & Copy Files",
                                    command=lambda : self.save(move=True))
        self.saveButton.grid(row=1)
        
    def save(self,move=False):
        dic = self.meta()
        assert self.openF.files != [], "Must pick file(s) to associate!"
        dic['files'] = self.openF.files
        dic['i'] = dt.datetime.now()
        dic['broken_link'] = '0'
        dic['faulty'] = '0'
        directory = self.openF.dir.get()
        dic['directory'] = directory
        fp = os.path.join(directory,"header.json")
        if os.path.isfile(fp):
            r = messagebox.askyesnocancel("Header File Exists!", "Overwrite existing json file?\nThis will destroy previous header file and overwrite previous database entry.")
            print(r)
            if r==None:
                return None
            elif r:
                f = open(fp)
                dicOld = json.load(f,cls=dtDecoder)
                f.close()
                self.db.removeIndex(dicOld['i'])
            else:
                fp = fp[:-5]+"{}.json".format(len(glob.glob(os.path.join(directory,"header*.json"))))
        f = open(fp,"w")
        json.dump(dic,f,indent=4,cls=dtEncoder)
        f.close()
        self.db.push(dic)
        if move:
            for f in self.openF.files:
                copy(f,directory)
            dic['files'] = [os.path.join(directory,os.path.basename(f))\
                            for f in self.openF.files]
        return None
    
    def commit(self):
        self.db.commit()
        
