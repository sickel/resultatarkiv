import datetime

from .dbconnector import *

class searchdata(dbconnector):

       
    def countsamples(self,req):
        #req=dict(req)
        table='sample'
        self.preparequeryfields(table,req)
        sql="select projectid,count(sample.id),projects.name,projects.contact,projects.dataowner,projects.restrictions from sample left join projects on projectid=projects.id  where "+' and '.join(self.fields)+ \
        " group by projects.name,projects.restrictions,projectid,projects.contact,projects.dataowner"
        self.cursor.execute(sql,self.values)
        res=self.cursor.fetchall()
        return(res)
    
    def preparequeryfields(self,table,req,multival=None):
        self.fields=[]
        self.values=[]
        self.getcolnames(table)
        cols=self.colnames
        for k,v in req.items():
            if k in cols:
                self.fields.append(k+"=?")
                self.values.append(v)
    
    
    def preparequeryfields2(self,table,req,multival=None):
        self.fielddata=tree()
        self.getcolnames(table)
        for k,v in req.items():
            if k in self.colnames:
                self.fielddata[k]=v
            elif v=="on":
                p=k.split("_")
                if p[0] in self.colnames:
                    if self.fielddata[p[0]]=={}:
                        self.fielddata[p[0]]=[p[1]]
                    else:
                        self.fielddata[p[0]].append(p[1])
        self.fields=[]
        self.values=[]
        for k,v in self.fielddata.items():
            if type(v)==list:
                k=k+" in ("+",".join("?"*len(v)) +")"
                self.values.extend(v)
            else:
                k=k+"=?"
                self.values.append(v)
            self.fields.append(k)
            
                
                
    
    
    def download(self,req,folder):
        print(req)
        table='sample'
        self.preparequeryfields2(table,req)
        cols=self.colnames
        subselect="(select id from sample where "+' and '.join(self.fields)+")"
        sql="select distinct name from metadatalist right join samplemetadata on metadatalist.id = metadataid where sampleid in"+subselect
        self.cursor.execute(sql,self.values)
        fetch=self.cursor.fetchall()
        metadata=[]
        for i in fetch:
            metadata.append(i[0])
        print(metadata)
        sql="select * from fullsample where id in "+subselect
        #sql="select "+",".join(cols)+" from sample where "
        # self.getcolnames(table)
        timestamp=datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.filename="resultatarkiv_"+timestamp+".csv"
        wf=open(folder+"/"+self.filename,"w")
        sep=";"
        wf.write(sep.join(cols)+sep+sep.join(metadata)+"\n")
        self.cursor.execute(sql,self.values)
        while True: 
            row=self.cursor.fetchone()
            if row is None: 
                break
            row = list(map(str,row))
            wf.write(sep.join(row)+"\n")
        
        
        
        
    def  overviewfields(self):
        return( ["Antall","Prosjekt","Kontaktperson","Dataeier","Restriksjoner"] )


    def __init__(self):
        self.connecttodb()        

        
    
        
    def search(self):
        True
    

    
