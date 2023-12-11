import os
import cv2
import time
import numpy as np
import devmem
import re

cap = cv2.VideoCapture(0)
mem = devmem.DevMem(0xffec006000, length=100)

def adb_shell(cmd):
    result=os.popen(cmd,'r',1).read()
    return result
    #执行调用程序
    
def img_change(img,brightness,gamma):
    img_hsv= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img_hsv[:,:,2]=np.clip(img_hsv[:,:,2]+brightness,0,255)
    img_output1 =cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
    #亮度调节
    img_output2 = np.power(img_output1/float(np.max(frame)),gamma)
    img_output2 = np.uint8(img_output2 *255)
    #GAMMA调节
    img_yuv = cv2.cvtColor(img_output2,cv2.COLOR_BGR2YUV)
    img_yuv [:,:,0] =cv2.equalizeHist(img_yuv[:,:,0])
    img_output3 = cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
    #直方图均值化
    
    return img_output3  
    #图像数据处理
      
while(1):

    mem.write(0x0,[0x00402078])
    io=mem.read(0x0, 32).hexdump(4)
    print(io)
    #io="".join(io)
    #re=re.findall('0xffec006050:   ........',io)
    #re=re.findall('\d\d\d\d\d\d\d\d',io)
    #re=re.findall('0xffec006050:   \d\d\d\d\d\d\d\d',io)
    #print(re[0])
    #if (re[0]=='0xffec006050:   7d49ffee'):
    if('0xffec006050:   7d49bfff'in io):
    	ret,frame = cap.read()
    	#读取一帧图像
    	current_time = time.localtime()
    	formatted_time = time.strftime("%Y-%m-%d_%H:%M:%S", current_time)
    	#设定图片名称为时间，格式年月日时分秒
    	nanodet_cmd='./nanodet {}.jpg'.format(formatted_time)
    	#调用NANODET的指令
    
    	img_change(frame,50,1)    
    	cv2.imwrite(r"/home/sipeed/ncnn/build/examples/"+ str(formatted_time) + ".jpg",frame) 
    	#存储路径/home/sipeed/ncnn/build/examples/
    
    	list1=adb_shell(nanodet_cmd)
    	#将执行完成NANODET返回的指令
    	#print(list1)
	#ncnn
    	os.popen('sudo pkill nanodet')
    	cap.release()
    	
    	

