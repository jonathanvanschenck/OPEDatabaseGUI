import tkinter as tk
rows = ["creator","material","submaterial","phase","device_host",
        "measurement_type","measurement_subtype","experimental_notes",
        "data_notes"]
rows2 = ["broken_link","faulty"]

class widget(tk.Frame):
    def __init__(self,master,db,**kwargs):
        self.db = db
        self.frame = tk.LabelFrame(master,text="Search Box")
        self.frame.grid(**kwargs)
        self.createWidgets()
        
    def createWidgets(self):
        #-----Search Boxes---------
        self.searchFrame = tk.LabelFrame(self.frame,
                                         text="Search Criteria")
        self.searchFrame.grid(row=0,column=0)
        # Date Range
        self.dateRangeFrame = tk.LabelFrame(self.searchFrame,
                                            text="Date Ranges")
        self.dateRangeFrame.grid(row=0,column=0,rowspan=2)
        self.dateRangeLabel = tk.Label(self.dateRangeFrame,
                                       text="Select dates with form: YYMMDD",
                                       justify=tk.LEFT)
        self.dateRangeLabel.grid(row=0,column=0,columnspan=2,sticky=tk.W)
        self.dateLow = KeywordEntry(self.dateRangeFrame,"Low",
                                    rowi=1,columni=0)
        self.dateLow.Entry.config(width=6)
        self.dateLow.set("000000")
        self.dateHigh = KeywordEntry(self.dateRangeFrame,"High",
                                    rowi=2,columni=0)
        self.dateHigh.Entry.config(width=6)
        self.dateHigh.set("999999")
        # Keyword criterea
        self.kwCritFrame = tk.LabelFrame(self.searchFrame,
                                         text="Keywords")
        self.kwCritFrame.grid(row=2,column=0,columnspan=2)
        self.kwCritLabel = tk.Label(self.kwCritFrame,
                                       text="Indicate keywords to include in search (comma delimited)",
                                       justify=tk.LEFT)
        self.kwCritLabel.grid(row=0,column=0,columnspan=2,sticky=tk.W)
        self.kwCrit = [KeywordEntry(self.kwCritFrame,rows[i],
                                    rowi=i+1,columni=0)\
                       for i in range(len(rows))]
        # Expanded Search Options
        self.expandOptFrame = tk.LabelFrame(self.searchFrame,
                                            text="Include:")
        self.expandOptFrame.grid(row=1,column=1)
        self.expandOpt = [KeywordCheckbutton(self.expandOptFrame,
                                             rows2[i],row=i,column=0)\
                          for i in range(len(rows2))]
        # Search Button
        self.searchButton = tk.Button(self.searchFrame,text="Search",
                                      command=self.search)
        self.searchButton.grid(row=0,column=1)
        #-------Search Results------------
        self.resultFrame = tk.LabelFrame(self.frame,
                                         text="Search Results")
        self.resultFrame.grid(row=1,column=0)
        self.resultSBy = tk.Scrollbar(self.resultFrame,orient=tk.VERTICAL)
        self.resultSBx = tk.Scrollbar(self.resultFrame,orient=tk.HORIZONTAL)
        self.resultText = listText(self.resultFrame,
                                   width=40,height=10,
                                   yscrollcommand=self.resultSBy.set,
                                   xscrollcommand=self.resultSBx.set,
                                   wrap="none")
        self.resultText.grid(row=0,column=0)
        self.resultSBy.config(command=self.resultText.yview)
        self.resultSBy.grid(row=0,column=1,sticky=tk.NS)
        self.resultSBx.config(command=self.resultText.xview)
        self.resultSBx.grid(row=1,column=0,sticky=tk.EW)
        
    def search(self):
        searchDic = {kwC.kw:kwC.get().strip(" ").strip(",").strip(" ")\
                     for kwC in self.kwCrit\
                     if kwC.get().strip(" ").strip(",").strip(" ")!=""}
        for exO in self.expandOpt:
            if exO.get()=="0":
                searchDic[exO.kw]="0"
        res = self.db.pullLike(searchDic,dateRange=[int(self.dateLow.get()),
                                                    int(self.dateHigh.get())])
        self.resultText.loadList(res)

class KeywordEntry(tk.StringVar):
    def __init__(self,master,kw,rowi=0,columni=0):
        tk.StringVar.__init__(self)
        self.kw = kw
        self.Label = tk.Label(master,text=kw+":",justify=tk.RIGHT)
        self.Label.grid(row=rowi,column=columni,sticky=tk.E)
        self.Entry = tk.Entry(master,textvariable=self)
        self.Entry.grid(row=rowi,column=columni+1,sticky=tk.W)
        
class KeywordCheckbutton(tk.StringVar):
    def __init__(self,master,kw,**kwargs):
        tk.StringVar.__init__(self)
        self.set("0")
        self.kw = kw
        self.Checkbutton = tk.Checkbutton(master,variable=self,text=kw+"?",
                                          offvalue="0",onvalue="")
        self.Checkbutton.grid(sticky=tk.W,**kwargs)
        
class listText(tk.Text):
    def __init__(self,*args,**kwargs):
        tk.Text.__init__(self,*args,**kwargs)
        self.data = []
        self.d()
        
    def loadList(self,l):
        self.e()
#        self.tag_remove("highlight", 1.0, "end")
        self.delete(1.0,tk.END)
        for dic in self.data:
            self.tag_unbind(dic['i'].isoformat(" "),"<Button-1>")
        self.data = l
        for dic in self.data:
            self.insert(tk.END,"{date}-{creator}-{material}/{submaterial}-{measurement_type}-{phase}-{device_host}\n".format(**dic))
            self.tag_bind(dic['i'].isoformat(" "),"<Button-1>",self.click_callback)
        self.see(1.0)
        self.d()
    
    def click_callback(self,event):
        print("click")
        line_no = event.widget.index("@%s,%s linestart" % (event.x, event.y))
        line_end = event.widget.index("%s lineend" % line_no)
        self.tag_remove("highlight", 1.0, "end")
        self.tag_add("highlight", line_no, line_end)
        self.tag_configure("highlight", background="blue")
    
    def d(self):
        self.config(state='disabled')
    def e(self):
        self.config(state='normal')