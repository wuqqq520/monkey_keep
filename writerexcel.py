# coding=utf-8
import time 
import os
import xlsxwriter


class wriexl(object):
    def __init__(self,fname):
        self.wbook=xlsxwriter.Workbook(fname)
        self.wbook.add_worksheet('汇总')
        self.percent_format = self.wbook.add_format({'num_format': '0%'})
        self.Title=[]
        self.line={}
        
    #----------------------------------------------------------------------
    def wri(self,data):
        ti=data[1].replace(":", "_")
        if ti not in self.wbook.sheetnames:
            self.sheet=self.wbook.add_worksheet(ti)
            self.sheet.write_row(0, 0, self.Title)
            self.sheet.set_column(3,3, cell_format=self.percent_format)
            self.line[ti]=1
        else:
            self.sheet=self.wbook.get_worksheet_by_name(ti) 

        self.sheet.write_row(self.line[ti], 0, data)
        self.line[ti]=self.line[ti]+1
        self.sheet.write_row
        
    def addchar(self):    
        Pid=self.wbook.add_chart({'type': 'scatter'})
        for sheet in self.wbook.sheetnames:
            if sheet !='汇总':
                Pid.add_series(
                    {'name':sheet,
                     'categories':'='+sheet+'!$A2:$A'+str(self.line[sheet]),
                     'values':'='+sheet+'!$C2:$C'+str(self.line[sheet]),
                     'line':{'width':1}
                     })                            
        Pid.set_title({'name': "Pid"})  
        Pid.set_size({'width': 800, 'height': 400})
        Pid.set_legend({'position': 'bottom'})
        self.wbook.get_worksheet_by_name('汇总').insert_chart('B2', Pid, {'x_offset': 25, 'y_offset': 10})          
        
        Memory_vss=self.wbook.add_chart({'type': 'line'})
        for sheet in self.wbook.sheetnames:
            if sheet !='汇总':
                Memory_vss.add_series(
                    {'name':sheet,
                     'categories':'='+sheet+'!$A2:$A'+str(self.line[sheet]),
                     'values':'='+sheet+'!$E2:$E'+str(self.line[sheet]),
                     #'x2_axis': 1,
                     'line':{'width':1.5}
                     })                            
        Memory_vss.set_title({'name': self.Title[4]})  
        Memory_vss.set_size({'width': 800, 'height': 400})
        Memory_vss.set_legend({'position': 'bottom'})
        #Memory_vss.set_x_axis({'name': 'Days', })
        self.wbook.get_worksheet_by_name('汇总').insert_chart('B23', Memory_vss, {'x_offset': 25, 'y_offset': 10}) #将图标插入表单中 
        
        Memory_rss=self.wbook.add_chart({'type': 'line'})
        for sheet in self.wbook.sheetnames:
            if sheet !='汇总':
                Memory_rss.add_series(
                    {'name':sheet,
                     'categories':'='+sheet+'!$A2:$A'+str(self.line[sheet]),
                     'values':'='+sheet+'!$F2:$F'+str(self.line[sheet]),
                     #'y2_axis': 1,
                     'line':{'width':1.5}
                     })                            
        Memory_rss.set_title({'name': self.Title[5]})  
        Memory_rss.set_size({'width': 800, 'height': 400})
        Memory_rss.set_legend({'position': 'bottom'})
        Memory_vss.set_x_axis({'major_gridlines':{'visible': True,'line':{'none': True}}})
        self.wbook.get_worksheet_by_name('汇总').insert_chart('B44', Memory_rss, {'x_offset': 25, 'y_offset': 10})        
                
        cpu=self.wbook.add_chart({'type': 'area','subtype':'stacked'})
        for sheet in self.wbook.sheetnames:
            if sheet !='汇总':
                cpu.add_series(
                    {'name':sheet,
                     'categories':'='+sheet+'!$A2:$A'+str(self.line[sheet]),
                     'values':'='+sheet+'!$D2:$D'+str(self.line[sheet]),
                     'line':{'width':1}
                     })                   
        cpu.set_title({'name': "CPU"})  
        cpu.set_size({'width': 800, 'height': 400})
        cpu.set_legend({'position': 'bottom'})
        self.wbook.get_worksheet_by_name('汇总').insert_chart('B65', cpu, {'x_offset': 25, 'y_offset': 10}) #将图标插入表单中        

        
    def work_close(self):
        self.wbook.close()



    







