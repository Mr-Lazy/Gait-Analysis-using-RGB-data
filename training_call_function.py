import os
import numpy as np
import cv2
import time

def take_input():
	for i in xrange (0,folders):
	    print("Enter "+str(i)+" for "+list_folder[i])
	print ("Enter -1 for all training elements")
	folder=int(raw_input("Enter your choice: "))
	return folder

def create_folder(folder_name):
	try:
		os.mkdir(str(folder_name))
	except WindowsError:
		print (str(folder_name)+" already exists...proceeding with further code...!")

def binary_generator(training_element):
	create_folder("binaryfeatures")


	if (training_element == -1):
	    for j in xrange (0,folders):
	        create_folder("binaryfeatures/"+list_folder[j])
	        list_imgs=os.listdir("rgbfeatures/"+list_folder[j])
	        for i in xrange(0,(len(list_imgs)-1)):
	            img1 = cv2.imread("rgbfeatures/"+list_folder[j]+"/001.jpeg",0)
	            bgsub = img1
	            img2 = cv2.imread("rgbfeatures/"+list_folder[j]+"/"+list_imgs[i+1],0)
	            cv2.absdiff(img2, img1, bgsub)
	            bgsub_blur2 = cv2.GaussianBlur(bgsub,(5,5),0)
	            (thresh, im_bw) = cv2.threshold(bgsub_blur2, 55, 255, cv2.THRESH_BINARY)
	            a='{0:03}'.format(i+1)
	            cv2.imwrite("binaryfeatures/"+list_folder[j]+"/bw_"+a+".png",im_bw)

	else:
		list_imgs=os.listdir("rgbfeatures/"+list_folder[training_element])
		create_folder("binaryfeatures/"+list_folder[training_element])
		for i in xrange(0,(len(list_imgs)-1)):
		    img1 = cv2.imread("rgbfeatures/"+list_folder[training_element]+"/001.jpeg",0)
		    bgsub = img1
		    img2 = cv2.imread("rgbfeatures/"+list_folder[training_element]+"/"+list_imgs[i+1],0)
		    cv2.absdiff(img2, img1, bgsub)
		    bgsub_blur2 = cv2.GaussianBlur(bgsub,(5,5),0)
		    (thresh, im_bw) = cv2.threshold(bgsub_blur2, 55, 255, cv2.THRESH_BINARY)
		    a='{0:03}'.format(i+1)
		    cv2.imwrite("binaryfeatures/"+list_folder[training_element]+"/bw_"+a+".png",im_bw)

def edge_generator(training_element):
	create_folder("edge_shift")
	if (training_element == -1):
	    for j in xrange (0,folders):
	        list_imgs = os.listdir("binaryfeatures/"+list_folder[j])
	        create_folder("edge_shift/"+list_folder[j])

	        for i in xrange(0,(len(list_imgs)-1)):
	            thresh = cv2.imread("binaryfeatures/"+list_folder[j]+"/"+list_imgs[i],0)
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
	                    cv2.imwrite("edge_shift/"+list_folder[j]+"/edge_"+a+".png",shift_sketch)


	else:
		list_imgs=os.listdir("binaryfeatures/"+list_folder[training_element])
		create_folder("edge_shift/"+list_folder[training_element])
		for i in xrange(0,(len(list_imgs)-1)):
		    thresh = cv2.imread("binaryfeatures/"+list_folder[training_element]+"/"+list_imgs[i],0)
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
		            cv2.imwrite("edge_shift/"+list_folder[training_element]+"/edge_"+a+".png",shift_sketch)

def filled_body_generator(training_element):
	create_folder("filled_body")
	if(training_element == -1):
	    for j in range (0,folders):
	        list_imgs = os.listdir("binaryfeatures/"+list_folder[j])
	        create_folder("filled_body/"+list_folder[j])

	        for i in xrange(0,(len(list_imgs)-1)):
	            thresh = cv2.imread("binaryfeatures/"+list_folder[j]+"/"+list_imgs[i],0)
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
	                    cv2.imwrite("filled_body/"+list_folder[j]+"/filled_"+a+".png",shift_sketch)



	else:
		list_imgs = os.listdir("binaryfeatures/"+list_folder[training_element])
		create_folder("filled_body/"+list_folder[training_element])
		for i in xrange(0,(len(list_imgs)-1)):
		    thresh = cv2.imread("binaryfeatures/"+list_folder[training_element]+"/"+list_imgs[i],0)
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
		            cv2.imwrite("filled_body/"+list_folder[training_element]+"/filled_"+a+".png",shift_sketch)


def training_check_generator(training_element):
	if (training_element == -1):
		for j in range (0,folders):
			list_imgs = os.listdir("edge_shift/"+list_folder[j])
			#minima_points = []
			#maxima_points = []
			shortlisted_imgs = np.zeros((40, 2),dtype=np.int)
			array = []
			for i in range(0,(len(list_imgs)-1)):
				cvImg = cv2.imread("edge_shift/"+list_folder[j]+"/"+list_imgs[i],0)
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
				#print step_dist
			print (len(array))

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

			print len(final_imgs_max)
			create_folder("training_check")


			create_folder("training_check/max_images")
			create_folder("training_check/mid_images")
			create_folder("training_check/min_images")

			c=(list_folder[j]).split("_")
			list_imgs_filled = os.listdir("filled_body/"+list_folder[j])
			create_folder("training_check/max_images/"+str(c[0]))
			create_folder("training_check/max_images/"+str(c[0])+"/"+str(c[1]))
			for k in range(0,3):
				a=final_imgs_max[k]
				img_max_copy=cv2.imread("filled_body/"+list_folder[j]+"/"+str(list_imgs_filled[a-1]),0)
				cv2.imwrite("training_check/max_images/"+str(c[0])+"/"+str(c[1])+"/"+str(k)+".png",img_max_copy)

			create_folder("training_check/mid_images/"+str(c[0]))
			create_folder("training_check/mid_images/"+str(c[0])+"/"+str(c[1]))
			for k in range(0,4):
				a=final_imgs_mid[k]
				img_mid_copy=cv2.imread("filled_body/"+list_folder[j]+"/"+str(list_imgs_filled[a-1]),0)
				cv2.imwrite("training_check/mid_images/"+str(c[0])+"/"+str(c[1])+"/"+str(k)+".png",img_mid_copy)

			create_folder("training_check/min_images/"+str(c[0]))
			create_folder("training_check/min_images/"+str(c[0])+"/"+str(c[1]))
			for k in range(0,2):
				a=final_imgs_min[k]
				img_min_copy=cv2.imread("filled_body/"+list_folder[j]+"/"+str(list_imgs_filled[a-1]),0)
				cv2.imwrite("training_check/min_images/"+str(c[0])+"/"+str(c[1])+"/"+str(k)+".png",img_min_copy)

	else:
		list_imgs = os.listdir("edge_shift/"+list_folder[training_element])
		#minima_points = []
		#maxima_points = []
		shortlisted_imgs = np.zeros((40, 2),dtype=np.int)
		array = []
		for i in range(0,(len(list_imgs)-1)):
			cvImg = cv2.imread("edge_shift/"+list_folder[training_element]+"/"+list_imgs[i],0)
			npImg = np.array(cvImg)
			coordList = np.argwhere(npImg == 255)
			numWhitePoints = len(coordList)
			min_vertical=240
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
			#print step_dist
	

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

		print len(final_imgs_max)
		create_folder("training_check")


		create_folder("training_check/max_images")
		create_folder("training_check/mid_images")
		create_folder("training_check/min_images")

		c=(list_folder[training_element]).split("_")
		list_imgs_filled = os.listdir("filled_body/"+list_folder[training_element])
		create_folder("training_check/max_images/"+str(c[0]))
		create_folder("training_check/max_images/"+str(c[0])+"/"+str(c[1]))
		for k in range(0,3):
			a=final_imgs_max[k]
			img_max_copy=cv2.imread("filled_body/"+list_folder[training_element]+"/"+str(list_imgs_filled[a-1]),0)
			cv2.imwrite("training_check/max_images/"+str(c[0])+"/"+str(c[1])+"/"+str(k)+".png",img_max_copy)

		create_folder("training_check/mid_images/"+str(c[0]))
		create_folder("training_check/mid_images/"+str(c[0])+"/"+str(c[1]))
		for k in range(0,4):
			a=final_imgs_mid[k]
			img_mid_copy=cv2.imread("filled_body/"+list_folder[training_element]+"/"+str(list_imgs_filled[a-1]),0)
			cv2.imwrite("training_check/mid_images/"+str(c[0])+"/"+str(c[1])+"/"+str(k)+".png",img_mid_copy)

		create_folder("training_check/min_images/"+str(c[0]))
		create_folder("training_check/min_images/"+str(c[0])+"/"+str(c[1]))

		for k in range(0,2):
			a=final_imgs_min[k]
			img_min_copy=cv2.imread("filled_body/"+list_folder[training_element]+"/"+str(list_imgs_filled[a-1]),0)
			cv2.imwrite("training_check/min_images/"+str(c[0])+"/"+str(c[1])+"/"+str(k)+".png",img_min_copy)



if __name__=="__main__":
	list_folder=os.listdir("rgbfeatures/")
	folders=len(list_folder)
	
	training_element=take_input()

	start_time=time.time()
	
	binary_generator(training_element)
	edge_generator(training_element)
	filled_body_generator(training_element)
	training_check_generator(training_element)

	print ("Total time taken: "+str(time.time()-start_time)+" seconds")
