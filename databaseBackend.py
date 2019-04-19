import os
import sqlite3
import datetime as dt

class strList(list):
    def __init__(self,List):
        assert hasattr(List,"__iter__"), "Input must be iterable"
        l = [str(e) for e in List]
        for s in l:
            assert not ";;" in s, "Invalid string value: cannot contain ';;'"
        list.__init__(self,l)
    
#    def __repr__(self):
#        return "("+";;".join(self)+")"
        
def adapt_strList(strlist):
    return ("%s" % (";;".join(strlist))).encode('ascii')

def convert_strList(s):
    return strList([e.decode() for e in s.split(b";;")])

sqlite3.register_adapter(strList,adapt_strList)
sqlite3.register_converter("strlist",convert_strList)

rows = ["i","date","creator","material","submaterial","phase","device_host",
        "measurement_type","measurement_subtype","experimental_notes",
        "data_notes","broken_link","faulty","directory","files"]

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
  'directory':'/home2/gaussian/OPEDatabase',
  'files': strList(['/home2/gaussian/OPEDatabase/all.db-journal',
                    '/home2/gaussian/OPEDatabase/metadata.py',
                    '/home2/gaussian/OPEDatabase/saveF.py']),
  'material': 'ADT',
  'measurement_subtype': '',
  'measurement_type': 'Absorption',
  'phase': 'Solution',
  'submaterial': 'TES',
  'broken_link': '0',
  'faulty': '0',
  'i':dt.datetime.now()}

class Database:
    def __init__(self):
        self._conn = sqlite3.connect("all.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._cur = self._conn.cursor()
        self.limit = 50
        
    def shutdown(self):
        self._conn.close()
    
    def commit(self):
        self._conn.commit()
        
    def pull(self,dateRange=[0,999999],limit=True):
        t = "SELECT *"
        t += " FROM md WHERE date BETWEEN "
        t += " AND ".join([str(i) for i in dateRange])
        if limit:
            t += (" LIMIT %s" % str(self.limit))
        self._cur.execute(t)
        return self.fetch()
    
    def push(self,dic):
        assert len(dic)==len(rows), "Invalid dictionary structure"
        for k in dic.keys():
            assert k in rows, "Provided key: {} is invalid".format(k)
        dic2 = dic.copy()
        dic2["files"] = strList(dic['files'])
        return self._cur.execute("INSERT INTO md VALUES ("+",".join(len(rows)*["?"])+")",
                                  tuple([dic2[k] for k in rows]))
    
    def fetch(self):
        return [{kw:val for kw,val in zip(rows,tup)} for tup in self._cur.fetchall()]
    
    def pullIndex(self,dtIndex):
        self._cur.execute("SELECT * FROM md WHERE i=?",
                           (dtIndex.isoformat(" "),))
        return self.fetch()
    
    def removeIndex(self,dtIndex):
        self._cur.execute("DELETE FROM md WHERE i=?",
                           (dtIndex.isoformat(" "),))
        return self.fetch()
    
    def pullLike(self,params={},dateRange=[0,999999],limit=True):
        t = "SELECT *"
        t += " FROM md WHERE date BETWEEN "
        t += " AND ".join([str(i) for i in dateRange])
        l = []
        for k in params:
            assert k in rows, "Invalid row name"
            for p in params[k].split(","):
                assert not ";" in p, "Invalid search string"
                t += " AND {0} LIKE '%{1}%'".format(k,p)
        if limit:
            t += (" LIMIT %s" % str(self.limit))
        self._cur.execute("{}".format(t),l)
        return self.fetch()
            
if __name__ == "__main__":
    try:
        db.shutdown()
    except:
        pass
    db = Database()