#!/usr/bin/python3.5
# coding=utf-8
import re
import time
import threading
import os
import subprocess
import chardet
import queue
import writerexcel
import argparse
import sys
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
########################################################################
class mymonkey():
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.event = threading.Event()
        self.event.set()
        self.lq = queue.Queue()
        self.mq = queue.Queue() 
    #----------------------------------------------------------------------
    def getlogcat(self,instruct):
        logfilenema='report\\logcat.txt'
        pi= subprocess.Popen(instruct,stdout=subprocess.PIPE)
        for i in iter(pi.stdout.readline, 'b'):
        #while self.event.is_set():
            if self.lq.empty()==False:
                logfilenema='report\\logcat'+self.lq.get()+'.txt'
            #i = pi.stdout.readline()
            if self.event.is_set():
                if len(i)>1:
                    try:
                        if type(i)==bytes:
                            encode_type = chardet.detect(i)
                            if encode_type['encoding'] == 'gbk':
                                si=i.decode('gbk')
                            elif encode_type['encoding'] == 'Windows-1252':
                                si=i.decode('Windows-1252')
                            elif encode_type['encoding'] == 'gb2312':
                                si=i.decode('gb2312')  
                            elif encode_type['encoding'] == 'ascii':
                                si=i.decode('ascii')  
                            elif encode_type['encoding'] == 'ISO-8859-1':
                                si=i.decode('gbk')
                            elif encode_type['encoding'] == 'utf-8':
                                si=i.decode('utf-8')                            
                        f=open(logfilenema,'a+')
                        si=si.strip()
                        f.write(si+'\n')
                        f.close() 
                    except:
                        pass
            else:
                pi.terminate()
                pi.kill() 
                break             
            '''    
            try:
                if type(i)==str:
                    encode_type = chardet.detect(i)
                    if encode_type['encoding'] == 'gbk':
                        i=i.decode('gbk')
                    elif encode_type['encoding'] == 'Windows-1252':
                        i=i.decode('Windows-1252')
                    elif encode_type['encoding'] == 'gb2312':
                        i=i.decode('gb2312')  
                    elif encode_type['encoding'] == 'ascii':
                        i=i.decode('ascii') 
                #elif type(i)==bytes:
                #i=str(i,encoding="utf-8")  
                f=open(logfilenema,'a+')
                i=i.strip()
                f.write(i+'\n')
                f.close() 
            except:
                print(type(i))
            '''


    def getmonkey(self,instruct,topfile):
        num=0
        logfilenema='report\\monkey.txt'
        pi= subprocess.Popen(instruct,stdout=subprocess.PIPE)
        while self.event.is_set():
            if self.mq.empty()==False:
                logfilenema='report\\monkey_'+self.mq.get()+'.txt'
            i = pi.stdout.readline() 
            i=str(i,encoding="utf-8")
            i=i.strip()
            if len(i)!=0:
                f=open(logfilenema,'a+')
                f.write(str(time.strftime("%Y-%m-%d %H:%M:%S"))+'  '+i+'\n')
                f.close() 
                num=0
            else:
                num=num+1
                time.sleep(1)
                if num>20:
                    self.event.clear()
                    self.writeexcel(topfile)
        else:
            pi.terminate()
            pi.kill()
    def Division(self,devices):
        while self.event.is_set():
            self.lq.put(devices+str(time.strftime("%Y%m%d%H%M")))
            self.mq.put(devices+str(time.strftime("%Y%m%d%H%M")))
            time.sleep(3600)         
   
       
    def gettop(self,topfile,instruct):
        instr=instruct[:instruct.find('|')]+"-n 1|find \"PID\""
        cs=os.popen(instr)
        cn=cs.read()
        cn=cn.rstrip() 
        f=open(topfile,'a+')
        f.write(cn+'\n')
        f.close() 
        cs.close()
        pi= subprocess.Popen(instruct,stdout=subprocess.PIPE,shell=True,bufsize=1)#shell=True
        for i in iter(pi.stdout.readline, 'b'):
            #print('I:...',i)
            #if not subprocess.Popen.poll(pi) is None:
            if self.event.is_set():
                    i=str(i,encoding="utf-8")
                    i=i.rstrip()
                    f=open(topfile,'a+')
                    f.write(str(time.strftime("%H:%M:%S"))+' '+i+'\n')
                    f.close()
            else:
                    pi.terminate()
                    pi.kill()  
                    break  

        pi.stdout.close()        
        '''
        while self.event.is_set():
            i = pi.stdout.readline()
            #i=i.decode() 
            i=str(i,encoding="utf-8")
            i=i.rstrip()
            if len(i)>1:
                f=open(topfile,'a+')
                f.write('%s %s%s'%(str(time.strftime("%H:%M:%S")),i,'\n'))
                f.close() 
        else:
            pi.terminate()
            pi.kill() 
        '''
        
    def writeexcel(self,topfile):
        write_excel=writerexcel.wriexl('report\\Top_'+str(time.strftime("%Y%m%d%H%M"))+'.xlsx')
        f = open(topfile,"r")   #设置文件对象
        line = f.readlines()
        f.close        
        cn=line[0]
        
        if 'VIRT' in cn:
            cn=cn.replace(']',' ')
            cn=cn.replace('[','')
            cn=cn.replace('%',' ')
            cn=cn.rstrip()
            cs=re.split('\s|\[%',cn)
            cs=list(filter(None, cs)) 
            cs.pop(0)
            cs.pop(-1)
            cs.insert(0, 'Time')
            #['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', 'CPU', '%MEM', 'TIME+', 'ARGS']
            ta=[cs.index("Time"),cs.index("ARGS"),cs.index("PID"),cs.index("CPU"),cs.index("SHR"),cs.index("RES")]
        if 'RSS' in cn:
            cn=cn.rstrip()
            cs=cn.split(" ")
            cs=list(filter(None, cs))
            cs.insert(0, 'Time')
            ta=[cs.index("Time"),cs.index("Name"),cs.index("PID"),cs.index("CPU%"),cs.index("VSS"),cs.index("RSS")]
        Title=[]
        for u in range(0,6):
            Title.append(cs[ta[u]])
        sort=sorted(ta,reverse=True)
        for t in sort:
            cs.pop(t)
        Title.extend(cs)
        
        write_excel.Title=Title
   
        for n in line[1:]:
            n=n.rstrip()
            n=n.split(" ")
            n=list(filter(None, n))
            
            if len(n)>=6:
                try:
                    data=[]
                    data.append(n[ta[0]])
                    data.append(n[ta[1]].replace('/','_').replace(':','_').replace('*','_'))
                    data.append(int(n[ta[2]]))
                    data.append(float(float(n[ta[3]].replace('%',''))/100))
                    data.append(int(n[ta[4]].replace('K','').replace('M','')))
                    data.append(int(n[ta[5]].replace('K','').replace('M','')))
                    for t in sort:
                        n.pop(t) 
                    data.extend(n)
                    write_excel.wri(data) 
                except:
                    pass
                   

        write_excel.addchar()
        write_excel.work_close()
        print('测试结束，报告文件:'+'report\\Top_'+str(time.strftime("%Y%m%d%H%M"))+'.xlsx')
    
    
if __name__== '__main__':
    mym=mymonkey()
    mym.event.set()
    mym.writeexcel('report\\top_default201911181842.txt')
