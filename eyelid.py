import cv2
import numpy as np
#from proto3 import acquire,approx_centre,find_pupil,find_iris,crop_iris,transform

#use for eyelid detection
#aim to crop most of the eyelids out using canny edges


def eyelid_segment(im,pupil_centre,pupil_radius,iris_radius):
	mask = np.copy(im)
#	cv2.imwrite('report/beforeeyelid.png',mask)
	empty_circle = np.zeros_like(mask)
	pupil_mask = np.zeros_like(mask)
	PUPIL_LIMIT = pupil_radius+5
	cv2.circle(empty_circle,(int(empty_circle.shape[1]/2),int(empty_circle.shape[0]/2)),iris_radius,(255,255,255),-1)
	cv2.circle(pupil_mask,(int(empty_circle.shape[1]/2),int(empty_circle.shape[0]/2)),PUPIL_LIMIT,(0,0,0),-1)
	only = np.bitwise_and(mask,empty_circle)
	LEFT_PUPIL = pupil_centre[0]-pupil_radius
	RIGHT_PUPIL=pupil_centre[0]+pupil_radius
	LOWER_PUPIL = pupil_centre[1]+pupil_radius
	UPPER_PUPIL = pupil_centre[1]-pupil_radius
	UPPER_PUPIL_LIMIT = pupil_centre[1]-PUPIL_LIMIT-10
	RIGHT_PUPIL_LIMIT=pupil_centre[0]+PUPIL_LIMIT+10
	only = cv2.GaussianBlur(only,(7,9),0) #was 9,9
	hi,thresh=cv2.threshold(only,10,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	lower = 0.5*hi
	bounds = cv2.Canny(only,lower,255)
#	cv2.imwrite('report/cannyeyelidprior.png',bounds)
	#only = np.bitwise_and(bounds,pupil_mask)
	cv2.circle(bounds,(int(empty_circle.shape[1]/2),int(empty_circle.shape[0]/2)),PUPIL_LIMIT,(0,0,0),-1)
#	cv2.imwrite('report/cannyeyelidafter.png',bounds)
	eyelid = np.argwhere(bounds>0) #INDICES WHERE THERE ARE BOUNDARIES
	eyelid_upper_y=np.argwhere(eyelid[:,0]<mask.shape[0]/3) #was /3 initially
	eyelid_lower_y=np.argwhere(eyelid[:,0]>9*mask.shape[0]/10) #was 9/10
	if len(eyelid_upper_y)>500: #check if edges are significant
		print('Upper Eyelid Detected:',len(eyelid_upper_y))
		eyelid_upper_use = eyelid[eyelid_upper_y[0][0]:eyelid_upper_y[-1][0]]
		for coords in eyelid_upper_use:
                	mask[0:coords[0],coords[1]]=0
	if len(eyelid_lower_y)>300:
		print('Lower Eyelid Detected:', len(eyelid_lower_y))
		eyelid_lower_use = eyelid[eyelid_lower_y[0][0]:eyelid_lower_y[-1][0]]
		for coords in eyelid_lower_use:
			mask[coords[0]:mask.shape[1],coords[1]]=0
	mask = np.bitwise_and(mask,empty_circle)
	#print('1st and last', eyelid_upper_y[0],eyelid_upper_y[-1])
	return mask,bounds





