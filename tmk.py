#!usr/bin/python
# coding=utf-8
import argparse
import time
import threading
import domonkey
import os


dxc=domonkey.mymonkey()
#dxc.writeexcel('report\\top_201908051833.txt')
def endth(file):
    s=input('Press Enter to exit:')
    dxc.event.clear()
    

parser = argparse.ArgumentParser()
parser.description="脚本用来执行monkey,并保存logcat,monkey日志以及记录设备的内存cpu等信息"
parser.add_argument('-p',"--package", help="包名",required=True)
parser.add_argument("-monkey","--monkey",action='store_true', default=False,help="执行monkey")
parser.add_argument("-n","--count", help="monkey执行次数",default='5000')
parser.add_argument("-log","--logcat",action='store_true', default=False,help="抓取logcat日志")
parser.add_argument("-E","--level", help="日志等级",default='v')
parser.add_argument("-top","--top", help="抓取内存，CPU信息",action='store_true', default=False)
parser.add_argument("-s","--devices", help="devices attached", default='default')
args = parser.parse_args()

if args.devices !='default':
    devices='-s '+args.devices
else:
    devices=''

command_m=devices+' shell  monkey  --throttle 500 --pct-motion 92 --pct-majornav 3 --pct-syskeys 5 --ignore-timeouts --ignore-crashes -p '+args.package+' -s 1000 -v -v -v '+args.count
command_l=devices+' shell logcat -v time *:'+args.level
#command_t='adb shell top -d 1 -m 200 |Find \"'+args.package+'\"'
command_t='adb '+devices+' shell top -d 1 -m 20 -o pid,args,virt,res,shr,%cpu,%MEM |Find \"'+args.package+'\"'
#command_t="adb  shell top  -d 1 -m 20 -H |find /v \"Tasks:\" |find /v \"Mem:\"|find /v \"Swap:\"|find /v \"%host\"|find /v \"PID\""

print('command_t: ',command_t)
topfile='report\\top_'+args.devices+str(time.strftime("%Y%m%d%H%M"))+'.txt'

monkey_instruct=command_m.split(' ')
monkey_instruct=list(filter(None, monkey_instruct)) 
monkey_instruct.insert(0, os.environ['ANDROID_HOME']+'\\platform-tools\\adb.exe')

logcat_instruct=command_l.split(' ')
logcat_instruct=list(filter(None, logcat_instruct)) 
logcat_instruct.insert(0, os.environ['ANDROID_HOME']+'\\platform-tools\\adb.exe')

top_instruct=command_t.split(' ')
top_instruct=list(filter(None, top_instruct)) 
top_instruct.insert(0, os.environ['ANDROID_HOME']+'\\platform-tools\\adb.exe')
print('monkey_instruct: ',monkey_instruct)


if args.monkey or args.logcat:
    th=threading.Thread(target=dxc.Division,args=(args.devices,))
    th.setDaemon(True)
    th.start()     
if args.monkey:
    monkey=threading.Thread(target=dxc.getmonkey,args=(monkey_instruct,topfile))
    monkey.setDaemon(True)
    monkey.start() 
    time.sleep(1)
if args.logcat:
    logcat=threading.Thread(target=dxc.getlogcat,args=(logcat_instruct,))
    logcat.setDaemon(True)
    logcat.start()  
    time.sleep(1)
if args.top:    
    top=threading.Thread(target=dxc.gettop,args=(topfile,command_t,))
    top.setDaemon(True)
    top.start()
    
end=threading.Thread(target=endth,args=(topfile,))
end.setDaemon(True)
end.start()

if args.monkey:
    monkey.join()
else:
    end.join()

dxc.writeexcel(topfile)
