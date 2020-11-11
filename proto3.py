#segmentation of iris+transform
#Ameen Jardine
#import libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt
from iris_code5 import feature_extract,match
from eyelid import eyelid_segment

#start timing
t1=cv2.getTickCount()
#get picture, greyscale and blur
im = '/media/ameen/B301-16DE/IITD Database/001/02_L.bmp' #2,4 JUNK 9 needs bigger centre guess
template = 'codes/CODE1_L.bmp' #tester
###################### functions ###########################

def acquire(img):
	im = cv2.imread(img,0)
	blur = cv2.GaussianBlur(im,(3,7),0)
	blurx2= cv2.GaussianBlur(im,(3,3),0)
	blurx3=cv2.GaussianBlur(im,(5,5),0)
	blurx4=cv2.GaussianBlur(im,(7,7),0)
	return im,blur

#approximate centre
def approx_centre(ROI,blur):
	ROI_y, ROI_x = ROI.shape
	ROI_x=np.uint16(np.floor(ROI_x/2)) #this is our guess
	ROI_y= np.uint16(np.floor(ROI_y/2))
	print('ROIs:',ROI_x,ROI_y)
	centre_mask = np.zeros_like(ROI)
	print('centre',ROI_x,ROI_y)
#FIND CENTRE
#HAVE GUESS CENTRE (MIDDLE OF IMAGE)
	cv2.circle(centre_mask,(ROI_x,ROI_y),np.uint16(np.floor(ROI_x/1.6)),(255,255,255),-1) #was divided by 1.9
	ret, thresh=cv2.threshold(blur,80,255,2) #was 80 worked (first arg)
	#cv2.imshow('thresh',thresh)
	centre_guess = np.bitwise_and(centre_mask,thresh)
#	cv2.imshow('guess',centre_guess)
#CIRCLE METHOD
	circle_found=False
	circles = cv2.HoughCircles(centre_guess,cv2.HOUGH_GRADIENT,1,80,param1=20,param2=30,minRadius=30,maxRadius=70) #works
	try:
		circles=np.uint16(np.around(circles))
		circle_found=True
	except TypeError:
		print('None found, trying again')
		circles = cv2.HoughCircles(centre_guess,cv2.HOUGH_GRADIENT,1,50,param1=20,param2=30,minRadius=24,maxRadius=90)
		#circles = cv2.HoughCircles(centre_guess,cv2.HOUGH_GRADIENT,1,180,param1=20,param2=30,minRadius=70,maxRadius=130)
		if circles is not None:
			circles=np.uint16(np.around(circles))
			circle_found=True
	if circle_found==True:
		radii=[]
		print('Hough Circles found...')
		for i in circles[0,:]:
#CIRCLES
			radii.append(i[2]) #keep all radii
			cv2.circle(centre_guess,(i[0],i[1]),i[2],(0,255,0),2)
		min = np.argmin(radii)
		circle_to_use = circles[0,min]
		i=circle_to_use #takes smallest circle
		cv2.circle(centre_guess,(i[0],i[1]),i[2],(0,255,0),2) #draw smallest circle

		centre = [i[0],i[1]]
		radius=i[2]
#		cv2.imshow('What was found',centre_guess)
#		cv2.imwrite('report/offpupil.png',centre_guess)
		print('Circles:',circles)
		print('Approx centre went from',ROI_x,ROI_y,'to',centre)
	else:
		centre=[ROI_x,ROI_y] #worst case just use centre of img
		print('No Hough Circles found...')
		radius=np.uint16(np.floor(ROI_x/1.9))
	return centre[0],centre[1],circle_found,radius #x and y centre



def approx_centre2(ROI,blur):
	ROI_y, ROI_x = ROI.shape
	ROI_x=np.uint16(np.floor(ROI_x/2)) #this is our guess
	ROI_y= np.uint16(np.floor(ROI_y/2))
	print('ROIs:',ROI_x,ROI_y)
	centre_mask = np.zeros_like(ROI)
	print('centre',ROI_x,ROI_y)
#FIND CENTRE
#HAVE GUESS CENTRE (MIDDLE OF IMAGE)
        #cv2.circle(centre_mask,(ROI_x,ROI_y),300,(255,255,255),-1) #should hit$
	cv2.circle(centre_mask,(ROI_x,ROI_y),np.uint16(np.floor(ROI_x/1.3)),(255,255,255),-1)
	ret, thresh=cv2.threshold(blur,80,255,2) #was 80 worked (first arg)
        #cv2.imshow('thresh',thresh)
	centre_guess = np.bitwise_and(centre_mask,thresh)
	cv2.imshow('guess',centre_guess)
#CIRCLE METHOD
	circle_found=False
	circles = cv2.HoughCircles(centre_guess,cv2.HOUGH_GRADIENT,1,80,param1=20,param2=30,minRadius=30,maxRadius=70)
	try:
		circles=np.uint16(np.around(circles))
		circle_found=True
	except TypeError:
		print('None found, trying again')
		circles = cv2.HoughCircles(centre_guess,cv2.HOUGH_GRADIENT,1,50,param1=20,param2=20,minRadius=30,maxRadius=70)
                #circles = cv2.HoughCircles(centre_guess,cv2.HOUGH_GRADIENT,1,1$
		if circles is not None:
			circles=np.uint16(np.around(circles))
			circle_found=True
	if circle_found==True:
		radii=[]
		print('Hough Circles found...')
		for i in circles[0,:]:
#CIRCLES
			radii.append(i[2]) #keep all radii

			cv2.circle(centre_guess,(i[0],i[1]),i[2],(0,255,0),2)
		min = np.argmin(radii)
		circle_to_use = circles[0,min]
		i=circle_to_use
		cv2.circle(centre_guess,(i[0],i[1]),i[2],(0,255,0),2)
		centre = [i[0],i[1]]
		radius=i[2]
#		cv2.imshow('What was found',centre_guess)
		print('Circles:',circles)
		print('Approx centre went from',ROI_x,ROI_y,'to',centre)

	else:
		centre=[ROI_x,ROI_y] #worst case just use centre of img
		print('No Hough Circles found...')
		radius=np.uint16(np.floor(ROI_x/1.9))
	return centre[0],centre[1],circle_found,radius #x and y centre





############################# DAUGMAN #####################
#now work on ROI only
#consider daugman for this ROI, basically just keep making circles
#integrate and repeat on slightly larger radius
#then compare the gradients between these two circles and store it in array
#continue this process until circle cant be expanded anymore
#take max gradient from array  and use the smaller radius value that was used to get this gradient

#store values here
def find_pupil(img,ROI_centre_x,ROI_centre_y,circle_found,guess_radius):
	ROI=img
	mask = np.zeros_like(ROI) #create blank image of same size and type
	integral_values=[]
	deriv_values=[]
	radius_values=[]
	best_radii = [] #holds results of max intensity radius for each location
	pupil_x=[]
	pupil_y=[]
	pupil=0
	y_count=0
	x_count=0
	x_lower,x_upper,y_lower,y_upper =0,10,0,20
	if circle_found==False:
		x_lower,x_upper,y_lower,y_upper= 50,50,0,50 #WAS 50,50,0,50
	x_range = range(ROI_centre_x-x_lower,ROI_centre_x+x_upper,5)
	y_range= range(ROI_centre_y-y_lower,ROI_centre_y+y_upper,2)
#integrate
	for x_direction in x_range: #SWEEP RIGHT, was -20 up till 20 in incr of 20 
		for y_direction in y_range: #SWEEP UP
			for dr in range(guess_radius-5,guess_radius+5): #was -5,+5
				radius_values.append(dr)
				cv2.circle(mask,(ROI_centre_x,ROI_centre_y),dr,(255,255,255),1)
				rad = cv2.bitwise_and(ROI, mask) #get only outer rinh
				integral_values.append(rad[rad>0].sum()/(2*np.pi*dr)) #integro
				mask.fill(0) #reset
			for bound in range(1,len(integral_values)):
				deriv_values.append(integral_values[bound]-integral_values[bound-1])
			y_count+=y_direction
			pupil_y.append(y_direction)
			integral_values.clear() #reset
		x_count+=x_direction
		pupil_x.append(x_direction)

#FIND WAY TO MATCH INDICES BC DERIV WILL HAVE WAY MORE
	deriv_length_original=len(deriv_values)
	deriv_values=np.array(deriv_values)
	deriv_values = np.abs(deriv_values)
	deriv_length = len(deriv_values)
	if np.argmax(deriv_values) == 0:
		optimal_index = 0
		#optimal_index = np.argmax(deriv_values)-1 #should probs first check that not 0
	else:
		optimal_index=np.argmax(deriv_values)-1
	print('optimal index is: ', optimal_index)
	adjusted_index_x = np.ceil(optimal_index/deriv_length_original * len(pupil_x)) #scales to get correct index for position
	adjusted_index_x=np.uint8(adjusted_index_x)
	adjusted_index_y = np.ceil(optimal_index/deriv_length_original * len(pupil_y)) #scales to get $
	adjusted_index_y=np.uint8(adjusted_index_y)
	if adjusted_index_x>=len(pupil_x):
		adjusted_index_x=len(pupil_x)-1
	elif adjusted_index_x==0:
		adjusted_index_x=0
	else:
		adjusted_index_x=adjusted_index_x-1
	if adjusted_index_y>=len(pupil_y):
		adjusted_index_y=len(pupil_y)-1
#	best_x=pupil_x[adjusted_index_x-1]
	elif adjusted_index_y==0:
		adjusted_index_y=0
	else:
		adjusted_index_y=adjusted_index_y-1
	best_x=pupil_x[adjusted_index_x]
	best_y=pupil_y[(adjusted_index_y)]
	#print('length of radius values:',len(radius_values))
	best_radius = radius_values[optimal_index]
	pupil=best_radius
	print('best centre is: ', best_x, best_y)
	print('Daugman Pupil Radius to be used: ',pupil)
	cv2.circle(ROI,(best_x,best_y),pupil,(0,255,0),3)
#	cv2.imwrite('report/pupil1.png',ROI)
	return best_x,best_y,pupil

def find_iris(img,ROI_x,ROI_y,pupil_radius):
	ROI=img
	mask = np.zeros_like(ROI) #create blank image of same size and type
#now repeat to find iris
	integral_values2=[]
	deriv_values2=[]
	radius_values2=[]
#integrate
#bounds: upper and lower
	lower_scalar=2
	if 30<pupil_radius<40:
		upper_scalar=3.3 #was 3.5
	elif 52>pupil_radius>=40: #changed this 26 oct was just 46
		upper_scalar=2.3
	elif pupil_radius>=52: #added 12 oct
		lower_scalar=1.7
		upper_scalar=2.1

	elif pupil_radius<=30: #added this 12 oct
		upper_scalar =3.6
	elif 40<=pupil_radius<46:
		upper_scalar = 2.5
	else:
		upper_scalar=2
		lower_scalar=1.7
	for dr in range(np.uint16(pupil_radius*lower_scalar),np.uint16(pupil_radius*upper_scalar)): #was 2 and 2.5

        	radius_values2.append(dr)
        	cv2.circle(mask,(ROI_x,ROI_y),dr,(255,255,255),1)
        	rad = cv2.bitwise_and(ROI, mask)
        	integral_values2.append(rad[rad>0].sum()/(2*np.pi*dr))
        #integration=0
        	mask.fill(0) #reset
	for bound in range(1,len(integral_values2)):
        	deriv_values2.append(integral_values2[bound]-integral_values2[bound-1])
	deriv_values2=np.array(deriv_values2)
	deriv_values2 = cv2.GaussianBlur(deriv_values2,(3,7),0) #3,3 is best
	deriv_values2 = np.abs(deriv_values2)
	iris_index = np.argmax(deriv_values2)-1 #get index of max value but should probs first check !0
	iris=radius_values2[iris_index]
	print('Daugman Iris Radius to be used: ',iris)
	cv2.circle(ROI, (ROI_x,ROI_y),iris,(0,255,0),3)
	#cv2.imshow('Original',img)
	#cv2.imshow('Daugman iris',ROI)
#	cv2.imwrite('report/iris1.png',ROI)
	return ROI, iris



def transform(polar,centre,pupil_radius,iris_radius):
	#now map from polar to cartesian
	# for each polar pixel, map along radial length, to left column of cartesian
	#done by considering cartesian_X = (pupil_radius:iris_radius)*cos(theta)
	#cartesian_y = (pupil_radius:iris_radius)*sin(theta)
	#in code need to do it per pixel so cartesian[x][y] = polar[][]
	#cartesian=np.zeros((iris_radius*2+1,iris_radius*2+1))
	cartesian = np.zeros_like(polar)
	row = polar.shape[0]
	column = polar.shape[1]
	theta = np.arange(0,2*np.pi,2*np.pi/(2*iris_radius)) #only scale by width of iris
	centre_x = centre[0]
	centre_y = centre[1]
	print('Image has a shape of',polar.shape)
	print('iris radius is:', iris_radius)
	print('Number of pixels of original:',row*column)
	print('Number of pixels in rubber sheet:',np.size(theta)*(iris_radius-pupil_radius))
	sheet_columns = np.size(theta)
	sheet_rows = iris_radius-pupil_radius
	rubber = np.zeros((sheet_rows,sheet_columns))
	for x in range(0,sheet_columns):
		for y in range(0,sheet_rows):
			th=theta.item(x) #speedup
			r = y/sheet_rows #r in range [0,1]
			inner_x = centre_x+pupil_radius*np.cos(th)
			outer_x = centre_x+iris_radius*np.cos(th)
			inner_y = centre_y+pupil_radius*np.sin(th)
			outer_y = centre_y+iris_radius*np.sin(th)
			cartesian_x = np.uint16(np.floor((1-r)*inner_x+outer_x*r))
			cartesian_y = np.uint16(np.floor((1-r)*inner_y+outer_y*r))
#			print(cartesian_x,cartesian_y)
			#rubber[y][x]=polar[cartesian_y][cartesian_x]
			#this is slightly faster
			rubber.itemset((y,x),polar.item((cartesian_y,cartesian_x)))
	rubber =rubber.astype('uint8')*255
#	cv2.imwrite('report/normalised2.png',rubber)
	return rubber

def crop_iris(image,centre,iris_radius):
	centre_x = centre[0]
	centre_y = centre[1]
	cropped = image
	image_width  = image.shape[0]
	image_height = image.shape[1]
	OFFSET=100
	cropped = cv2.copyMakeBorder(image,OFFSET,OFFSET,OFFSET,OFFSET,cv2.BORDER_CONSTANT) #make black border
	centre_x =centre_x+OFFSET
	centre_y =centre_y+OFFSET
	cv2.imshow('before cropping...',cropped)
	cropped = cropped[centre_y-iris_radius:centre_y+iris_radius,centre_x-iris_radius:centre_x+iris_radius]
	new_centre_x = np.uint16(cropped.shape[1]/2)
	new_centre_y = np.uint16(cropped.shape[0]/2)
	return cropped, [new_centre_x,new_centre_y]

####################### end of functions ###############################
#actual code implementation

def recognition(img,template,mode,enroll):
	ROI,blur = acquire(img)
	ROI_x, ROI_y,centre_found,guess_radius = approx_centre(ROI,blur) #decent approx of pupil centre
	print(ROI_x)
	if centre_found==False:
		ROI_x,ROI_y,centre_found,guess_radius=approx_centre2(ROI,blur)
	print('Found centre')
	best_x,best_y,pupil_radius = find_pupil(ROI,ROI_x,ROI_y,centre_found,guess_radius) #locate pupil
	print('Found pupil')
	local, iris_radius = find_iris(ROI,best_x,best_y,pupil_radius) #find iris
#cv2.imwrite('results/localised.png',local) #remember to comment out
	print('Found iris')
#normalised = transform(local,[best_x,best_y],pupil_radius,iris_radius)
	cropped, new_centre = crop_iris(ROI,[best_x,best_y],iris_radius)
	cropped2,canny = eyelid_segment(cropped,[best_x,best_y],pupil_radius,iris_radius)
	normalised = transform(cropped2,new_centre,pupil_radius,iris_radius)
	print('Normalised')
	cv2.imshow('Original',ROI)
	cv2.imshow('Daugman Localisation',local)
	cv2.imshow('Cropped',cropped)
	cv2.imshow('Cropped with eyelids segmented',cropped2)
	cv2.imshow('Normalised',normalised)
#cv2.imshow('Adjusted Normalised',new_normalised)
	print('Extracting features...')
	tl=cv2.getTickCount()
	bitcode,noise =feature_extract(normalised) #imported
	tlf=(cv2.getTickCount()-tl)/cv2.getTickFrequency()
	print('tlf',tlf) #timed feature extraction
	cv2.imshow('Bitcode',bitcode)

	#print('HD:',HD)
	if enroll==1:
	#	cv2.imwrite('codes/CODEX.bmp',bitcode)
		cv2.imwrite('codes2/CODEX.bmp',bitcode)
		cv2.imwrite('noise/CODEX.bmp',noise)
	else:
		pass
	#HD = match2(bitcode,template,noise,template_noise)
	HD = match(bitcode,template)
	print('HD: ',HD)
	t2= cv2.getTickCount()
	elapsed = (t2-t1)/cv2.getTickFrequency()
	print("It took",elapsed, "seconds to run code.")
	cv2.waitKey(mode) #change back to 0
	cv2.destroyAllWindows()
	return HD, centre_found,bitcode



#fin = recognition(im,template,0)
