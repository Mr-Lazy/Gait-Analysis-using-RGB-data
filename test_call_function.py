import os
import numpy as np
import cv2
import time

def take_input():
	for i in xrange (0,folders):
	    print("Enter "+str(i)+" for "+list_folder[i])
	folder=int(raw_input("Enter your choice: "))
	return folder

def create_folder(folder_name):
	try:
		os.mkdir(str(folder_name))
	except WindowsError:
		print (str(folder_name)+" already exists...proceeding with further code...!")

def binary_generator(test_element):
	create_folder("binarytestfeatures")
	list_imgs=os.listdir("rgbtestfeatures/"+list_folder[test_element])
	create_folder("binarytestfeatures/"+list_folder[test_element])
	for i in xrange(0,(len(list_imgs)-1)):
	    img1 = cv2.imread("rgbtestfeatures/"+list_folder[test_element]+"/001.jpeg",0)
	    bgsub = img1
	    img2 = cv2.imread("rgbtestfeatures/"+list_folder[test_element]+"/"+list_imgs[i+1],0)
	    cv2.absdiff(img2, img1, bgsub)
	    bgsub_blur2 = cv2.GaussianBlur(bgsub,(5,5),0)
	    (thresh, im_bw) = cv2.threshold(bgsub_blur2, 55, 255, cv2.THRESH_BINARY)
	    a='{0:03}'.format(i+1)
	    cv2.imwrite("binarytestfeatures/"+list_folder[test_element]+"/bw_"+a+".png",im_bw)

def edge_generator(test_element):
	create_folder("edge_test_shift")
	list_imgs=os.listdir("binarytestfeatures/"+list_folder[test_element])
	create_folder("edge_test_shift/"+list_folder[test_element])
	for i in xrange(0,(len(list_imgs)-1)):
	    thresh = cv2.imread("binarytestfeatures/"+list_folder[test_element]+"/"+list_imgs[i],0)
	    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	    cnt = len(contours)
	    if(cnt!=0):
	        temp=0.0
	        max_area=0.0
	        cnt_count=0
	        for x in range (0, cnt):
	            area=cv2.contourArea(contours[x])
	            temp=area
	            if(temp>max_area):
	                max_area=temp
	                cnt_count=x
	        max_cont=contours[cnt_count]
	        M = cv2.moments(max_cont)
	        if(M['m00']!=0):
	            cx = int(M['m10']/M['m00'])
	            cy = int(M['m01']/M['m00'])
	            cv2.drawContours(thresh, [max_cont],0, (255), 1)
	            ret,thresh = cv2.threshold(thresh,254,255,0)
	            rows,cols = thresh.shape
	            N = np.float32([[1,0,(320-cx)],[0,1,(240-cy)]])
	            shift_sketch = cv2.warpAffine(thresh,N,(cols,rows))
	            a='{0:03}'.format(i+1)
	            cv2.imwrite("edge_test_shift/"+list_folder[test_element]+"/edge_"+a+".png",shift_sketch)

def filled_body_generator(test_element):
	create_folder("filled_test_body")
	list_imgs = os.listdir("binarytestfeatures/"+list_folder[test_element])
	create_folder("filled_test_body/"+list_folder[test_element])
	for i in xrange(0,(len(list_imgs)-1)):
	    thresh = cv2.imread("binarytestfeatures/"+list_folder[test_element]+"/"+list_imgs[i],0)
	    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	    cnt = len(contours)
	    if(cnt!=0):
	        temp=0.0
	        max_area=0.0
	        cnt_count=0
	        for x in range (0, cnt):
	            area=cv2.contourArea(contours[x])
	            temp=area
	            if(temp>max_area):
	                max_area=temp
	                cnt_count=x
	        max_cont=contours[cnt_count]
	        M = cv2.moments(max_cont)
	        if(M['m00']!=0.0):
	            cx = int(M['m10']/M['m00'])
	            cy = int(M['m01']/M['m00'])
	            cv2.drawContours(thresh, [max_cont],0, (255), -1)
	            ret,thresh = cv2.threshold(thresh,254,255,0)
	            rows,cols = thresh.shape
	            N = np.float32([[1,0,(320-cx)],[0,1,(240-cy)]])
	            shift_sketch = cv2.warpAffine(thresh,N,(cols,rows))
	            a='{0:03}'.format(i+1)
	            cv2.imwrite("filled_test_body/"+list_folder[test_element]+"/filled_"+a+".png",shift_sketch)


def test_check_generator(test_element):
	list_imgs = os.listdir("edge_test_shift/"+list_folder[test_element])
	shortlisted_imgs = np.zeros((40, 2),dtype=np.int)
	array = []
	for i in range(0,(len(list_imgs)-1)):
	    cvImg = cv2.imread("edge_test_shift/"+list_folder[test_element]+"/"+list_imgs[i],0)
	    npImg = np.array(cvImg)
	    coordList = np.argwhere(npImg == 255)
	    numWhitePoints = len(coordList)
	    min_vertical = 240
	    for h in range(0,len(coordList)):
	    	if(min_vertical<coordList[h,0]):
	    		min_vertical = coordList[h,0]
	    min_point = [370,320]
	    max_point = [370,325]
	    for k in range(0,numWhitePoints):
	        if (coordList[k,0]>(min_vertical-60)):
	            if (min_point[1]>coordList[k,1]):
	                min_point = coordList[k]
	                
	            if (max_point[1]<coordList[k,1]):
	                max_point = coordList[k]
	                
	    step_dist=max_point[1]-min_point[1]
	    array.append(step_dist)
	final_imgs_max =[]
	final_imgs_min =[]
	final_imgs_mid =[]
	a=0
	flag_min=1
	for i in range(10,(len(array)-10)):
	    if ((array[i]>=array[i-2]) & (array[i]>=array[i-1]) & (array[i]>array[i+1]) & (array[i]>array[i+2])):
	        #maxima_points.append(i+1)
	        if (array[i]>95):
	            shortlisted_imgs[a][0]=i
	            shortlisted_imgs[a][1]=1
	            a=a+1
	            if(flag_min==1):
	                print ('Maxima: '+str(i))
	                final_imgs_max.append(i)
	                flag_min=0
	    if ((array[i]<=array[i-2]) & (array[i]<=array[i-1]) & (array[i]<array[i+1]) & (array[i]<array[i+2])):
	        #minima_points.append(i+1)
	        if ((array[i]>40) & (array[i]<95)):
	            shortlisted_imgs[a][0]=i
	            shortlisted_imgs[a][1]=0
	            a=a+1
	            if(flag_min==0):
	                print ('Minima: '+str(i))
	                final_imgs_min.append(i)
	                flag_min=1
	for i in range (0,len(final_imgs_max)-1):
	    final_imgs_mid.append(int((final_imgs_max[i]+final_imgs_min[i])/2))
	    final_imgs_mid.append(int((final_imgs_max[i+1]+final_imgs_min[i])/2))
	print (shortlisted_imgs)
	print final_imgs_max,final_imgs_mid,final_imgs_min
	create_folder("test_check")
	list_imgs_filled = os.listdir("filled_test_body/"+list_folder[test_element])
	create_folder("test_check/"+str(list_folder[test_element]))
	create_folder("test_check/"+str(list_folder[test_element])+"/"+"max_images")
	for k in range(0,3):
	    a=final_imgs_max[k]
	    img_max_copy=cv2.imread("filled_test_body/"+list_folder[test_element]+"/"+str(list_imgs_filled[a-1]),0)
	    cv2.imwrite("test_check/"+str(list_folder[test_element])+"/"+"max_images"+"/"+str(k)+".png",img_max_copy)
	create_folder("test_check/"+str(list_folder[test_element])+"/"+"mid_images")
	for k in range(0,4):
	    a=final_imgs_mid[k]
	    img_mid_copy=cv2.imread("filled_test_body/"+list_folder[test_element]+"/"+str(list_imgs_filled[a-1]),0)
	    cv2.imwrite("test_check/"+str(list_folder[test_element])+"/"+"mid_images"+"/"+str(k)+".png",img_mid_copy)
	create_folder("test_check/"+str(list_folder[test_element])+"/"+"min_images")
	for k in range(0,2):
	    a=final_imgs_min[k]
	    img_min_copy=cv2.imread("filled_test_body/"+list_folder[test_element]+"/"+str(list_imgs_filled[a-1]),0)
	    cv2.imwrite("test_check/"+str(list_folder[test_element])+"/"+"min_images"+"/"+str(k)+".png",img_min_copy)

def matching_scores(test_element):
	list_lengthfolder = os.listdir("test_check/"+str(list_folder[test_element]))
	list_imgsubsec = []
	list_maxtrain_sub = os.listdir("training_check/max_images/")
	list_midtrain_sub = os.listdir("training_check/mid_images/")
	list_mintrain_sub = os.listdir("training_check/min_images/")
	list_datano = []
	list_submaximgs = []
	a=[]
	for k in range (0,(len(list_maxtrain_sub))):
	    a.append([])
	min_max=[]
	min_mid=[]
	min_min=[]
	for i in range (0,len(list_lengthfolder)):      # Entering test_check/name/"max,mid,min"
	    if (i==0):
	        list_imgsubsec=(os.listdir("test_check/"+str(list_folder[test_element])+"/"+str(list_lengthfolder[0])))   #test_max_imgs
	        for j in range (0,(len(list_imgsubsec))):               #every test image
	            img_test = cv2.imread("test_check/"+str(list_folder[test_element])+"/"+"max_images"+"/"+str(list_imgsubsec[j]),0)
	            contours,hierarchy = cv2.findContours(img_test,2,1)
	            cnt1 = contours[0]
	            for k in range (0,(len(list_maxtrain_sub))):   #testing with every training man
	                arbit= 1000.0
	                list_datano = os.listdir("training_check/max_images/"+str(list_maxtrain_sub[k]))
	                for m in range (0,len(list_datano)):
	                    list_submaximgs = os.listdir("training_check/max_images/"+str(list_maxtrain_sub[k])+"/"+str(list_datano[m]))
	                    for n in range (0,len(list_submaximgs)):
	                        img_train = cv2.imread("training_check/max_images/"+str(list_maxtrain_sub[k])+"/"+str(list_datano[m])+"/"+str(list_submaximgs[n]),0)
	                        contours2,hierarchy2 = cv2.findContours(img_train,2,1)
	                        cnt2 = contours2[0]
	                        ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
	                        if(arbit>=ret):
	                            arbit=ret
	                a[k].append(arbit)
	    if (i==1):
	        list_imgsubsec=(os.listdir("test_check/"+str(list_folder[test_element])+"/"+str(list_lengthfolder[1])))
	        for j in range (0,(len(list_imgsubsec))):
	            img_test = cv2.imread("test_check/"+str(list_folder[test_element])+"/"+"mid_images"+"/"+str(list_imgsubsec[j]),0)
	            contours,hierarchy = cv2.findContours(img_test,2,1)
	            cnt1 = contours[0]
	            for k in range (0,(len(list_maxtrain_sub))):
	                arbit= 1000.0
	                list_datano = os.listdir("training_check/mid_images/"+str(list_midtrain_sub[k]))
	                for m in range (0,len(list_datano)):
	                    list_submaximgs = os.listdir("training_check/mid_images/"+str(list_midtrain_sub[k])+"/"+str(list_datano[m]))
	                    for n in range (0,len(list_submaximgs)):
	                        img_train = cv2.imread("training_check/mid_images/"+str(list_midtrain_sub[k])+"/"+str(list_datano[m])+"/"+str(list_submaximgs[n]),0)
	                        contours2,hierarchy2 = cv2.findContours(img_train,2,1)
	                        cnt2 = contours2[0]
	                        ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
	                        if(arbit>=ret):
	                            arbit=ret
	                a[k].append(arbit)
	    if (i==2):
	        list_imgsubsec=(os.listdir("test_check/"+str(list_folder[test_element])+"/"+str(list_lengthfolder[2])))
	        for j in range (0,(len(list_imgsubsec))):
	            img_test = cv2.imread("test_check/"+str(list_folder[test_element])+"/"+"min_images"+"/"+str(list_imgsubsec[j]),0)
	            contours,hierarchy = cv2.findContours(img_test,2,1)
	            cnt1 = contours[0]
	            for k in range (0,(len(list_maxtrain_sub))):
	                arbit= 1000.0
	                list_datano = os.listdir("training_check/min_images/"+str(list_mintrain_sub[k]))
	                for m in range (0,len(list_datano)):
	                    list_submaximgs = os.listdir("training_check/min_images/"+str(list_mintrain_sub[k])+"/"+str(list_datano[m]))
	                    for n in range (0,len(list_submaximgs)):
	                        img_train = cv2.imread("training_check/min_images/"+str(list_mintrain_sub[k])+"/"+str(list_datano[m])+"/"+str(list_submaximgs[n]),0)
	                        contours2,hierarchy2 = cv2.findContours(img_train,2,1)
	                        cnt2 = contours2[0]
	                        ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
	                        if(arbit>=ret):
	                            arbit=ret
	                a[k].append(arbit)
	summation=np.zeros((len(list_maxtrain_sub), 2),dtype=np.float32)
	for i in range (0,(len(list_maxtrain_sub))):
	    summation[i][0]=i
	    summation[i][1]=(float(sum(a[i])))
	sorted_rank=summation[summation[:,1].argsort()]
	for i in range (0,(len(list_maxtrain_sub))):
	    a=int(sorted_rank[i][0])
	    print(str(i+1)+" Nearest Neighbour --> "+str(list_maxtrain_sub[a]+": "+str(sorted_rank[i][1])))


if __name__=="__main__":
	list_folder=os.listdir("rgbtestfeatures/")
	folders=len(list_folder)
	
	test_element=take_input()

	start_time=time.time()
	
	binary_generator(test_element)
	edge_generator(test_element)
	filled_body_generator(test_element)
	test_check_generator(test_element)
	matching_scores(test_element)

	print ("Total time taken: "+str(time.time()-start_time)+" seconds")
