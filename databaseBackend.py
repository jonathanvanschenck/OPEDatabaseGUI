import os
import sqlite3
import datetime as dt

class strList(list):
    def __init__(self,List):
        assert type(List)==type([]), "Input must be a list"
        l = [str(e) for e in List]
        for s in l:
            assert not ";;" in s, "Invalid string value: cannot contain ';;'"
        list.__init__(self,l)
    
    def __repr__(self):
        return "("+";;".join(self)+")"
        
def adapt_strList(strlist):
    return ("%s" % (";;".join(strlist))).encode('ascii')

def convert_strList(s):
    return strList([e.decode() for e in s.split(b";;")])

sqlite3.register_adapter(strList,adapt_strList)
sqlite3.register_converter("strlist",convert_strList)

rows = ["i","date","creator","material","submaterial","phase","device_host",
        "measurement_type","measurement_subtype","experimental_notes",
        "data_notes","broken_link","files"]

if not os.path.isfile("all.db"):
    conn = sqlite3.connect("all.db")
    cur = conn.cursor()
    t = "CREATE TABLE md("
    t += rows[0]+" timestamp, "
    t += rows[1]+" INTEGER, "
    for r in rows[2:-1]:
        t += r+" TEXT, "
    t += rows[-1]+" strlist)"
    cur.execute(t)
    conn.commit()
    conn.close()

test = {'creator': 'JVS',
  'data_notes': '\n',
  'date': 190417,
  'device_host': 'CB',
  'experimental_notes': '\n',
  'files': strList(['/home2/gaussian/OPEDatabase/all.db-journal',
                    '/home2/gaussian/OPEDatabase/metadata.py',
                    '/home2/gaussian/OPEDatabase/saveF.py']),
  'material': 'ADT',
  'measurement_subtype': '',
  'measurement_type': 'Absorption',
  'phase': 'Solution',
  'submaterial': 'TES',
  'broken_link': '0',
  'i':dt.datetime.now()}

class Database:
    def __init__(self):
        self.__conn = sqlite3.connect("all.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.__cur = self.__conn.cursor()
        self.limit = 10
        
    def shutdown(self):
        self.__conn.close()
    
    def commit(self):
        self.__conn.commit()
        
    def pull(self,dateRange=[0,999999],limit=True):
        t = "SELECT *"
        t += " FROM md WHERE date BETWEEN "
        t += " AND ".join([str(i) for i in dateRange])
        if limit:
            t += (" LIMIT %s" % str(self.limit))
        self.__cur.execute(t)
        return [{kw:val for kw,val in zip(rows,tup)} for tup in self.__cur.fetchall()]
    
    def push(self,dic):
        assert len(dic)==len(rows), "Invalid dictionary structure"
        for k in dic.keys():
            assert k in rows, "Provided key: {} is invalid".format(k)
        dic2 = dic.copy()
        dic2["files"] = strList(dic['files'])
        return self.__cur.execute("INSERT INTO md VALUES ("+",".join(len(rows)*["?"])+")",
                                  tuple([dic2[k] for k in rows]))
        
    def pullIndex(self,dtIndex):
        self.__cur.execute("SELECT * FROM md WHERE i=?",
                           (dtIndex.isoformat(" "),))
        return [{kw:val for kw,val in zip(rows,tup)} for tup in self.__cur.fetchall()]
        
            
if __name__ == "__main__":
    try:
        db.shutdown()
    except:
        pass
    db = Database()