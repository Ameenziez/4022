
#segmentation of iris+transform
#Ameen Jardine
#does it by columns
 #import libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt
#import scikit-image
from scipy import ndimage



def eyelid_filter(norm):
	half_y = int(norm.shape[0]/2)
	quarter_x=int(norm.shape[1]/4)
	mean = np.mean(norm)
	dev = np.std(norm)
	new_dev = np.std(norm[half_y,quarter_x])
	new_mean= np.mean(norm[half_y,quarter_x])
#	print('-----------------mean value of: ',mean,' and std dev of ',dev)
#	print('new mean: ', new_mean, ' and dev ',new_dev)
        #print('min value of ',np.min(norm))
        #adjusted = np.where(norm>mean+dev,0,norm)
	adjusted=np.where(norm>=180,0,norm)
	adjusred=np.where(norm<40,0,norm)
	return adjusted

#0.7 and no fftshift works decent
def feature_extract(normalised):
	#ultimately, can control how many bytes, 2048 bits recommended
	#transform each row FFT
	CODE_HEIGHT=8 #16,32
	CODE_WIDTH=64 # 8,64 was okay
	template_shape = [CODE_WIDTH,CODE_HEIGHT] #same width, diff height
	w=23 #wavelet size
	step = normalised.shape[1]/2
	#print('step size',step)
	f0 = np.linspace(0.01,0.5,int(step)) #centre freqs
	sigma=0.5
	gaborfilter =np.exp(-(np.log(w*f0)**2)/(2*np.log(sigma)**2)) #diy gabor
	n = gaborfilter.shape[0]
	downA = gaborfilter
	downA = cv2.resize(downA,(1,int(2*n)),fx=0.5,fy=0.5,interpolation=cv2.INTER_NEAREST) #get to size required for arrays to match sizes
	down=[]
	for elements in downA:
		down.append(elements[0])
	print('n is:',n,'down length: ', len(down), 'vs gabor ',len(gaborfilter))
	print('original gabor: ',gaborfilter)
	print('adjusted gabor:',down)
#	print(gaborfilter.shape, 'vs',down.shape)
#	print('Gabor',gaborfilter)
#	plt.stem(f0,gaborfilter)
#	plt.xlabel('f0')
#	plt.ylabel('g')
#	plt.title('Log-Gabor filter')
#	plt.show()
	print('normalised shape',normalised.shape)
	print('-------------------------------------------------------')
	freq = []
	filtered=[]
	filtered_real,filtered_imag=[],[]
	normalised=eyelid_filter(normalised)
	black = np.count_nonzero(normalised==0)
#	print('number of black pixels= ',black)
	mean=np.sum(normalised)/(np.prod(normalised.shape)-black)
#	print('mean is ',mean).
	normalised[normalised<1]=mean #turn black areas into mean
	normalised_T=normalised
	norm_T=np.float32(normalised_T)
	norm_freq=np.fft.fft(norm_T)
#	norm_freq=np.fft.fftshift(norm_freq)
	norm_real=np.real(norm_freq)
	norm_imag=np.imag(norm_freq)

	print('actual shape',normalised.shape, 'versus what I did',len(normalised_T))
	for rows in range(norm_T.shape[0]): #rows was 0

		Areal=norm_real[rows,:]*down
		Aimag=norm_imag[rows,:]*down
		filtered_real.append(Areal)
		filtered_imag.append(Aimag)
		#multiply each row with filter
	real_freq=np.array(filtered_real)
	imag_freq=np.array(filtered_imag)
	real_freq,imag_freq=np.fft.fftshift(real_freq),np.fft.fftshift(imag_freq)
#	real_freq,imag_freq = real_freq[0:,0:int(real_freq.shape[1]/2)],imag_freq[0:,0:int(imag_freq.shape[1]/2)]
	reconstruction = real_freq+imag_freq #illustration only
	reconstruction = np.fft.ifftshift(reconstruction)
	reconstruction = np.fft.ifft(reconstruction)
	r=np.abs(reconstruction)
	r= reconstruction-np.min(reconstruction)
	r = r/np.max(r)*255
	cv2.imshow('reconstructed',np.uint8(r))
	test_real = real_freq.astype('uint8')*255 #out of curiosity
	test_imag = imag_freq.astype('uint8')*255 #out of curiosity
#	cv2.imshow('Real',(test_real))
#	cv2.imshow('Imag',(test_imag))

	#now quantize
	print('real size',real_freq.shape, 'versus',normalised.shape)
	patch_th = int(np.ceil(real_freq.shape[1]/(CODE_WIDTH)))
	patch_r = int(np.ceil(real_freq.shape[0]/(CODE_HEIGHT))) #r patch along transpoe 
	diff_th = patch_th*CODE_WIDTH - real_freq.shape[1] #check if theres difference WAS
	diff_r = patch_r*CODE_HEIGHT-real_freq.shape[0]
	if diff_th>0: #patch too big for image, append some values to be close
		print('patch is too big, appending th...')
		real_freq = np.hstack([real_freq]*2)
		imag_freq = np.hstack([imag_freq]*2)
	if diff_r>0: #patch too big for image, append some values to be close
		print('patch is too big, appending R...')
		real_freq = np.vstack([real_freq]*2)
		imag_freq = np.vstack([imag_freq]*2)

	print('PATCH TH:',patch_th,'PATCH R',patch_r) #swapped names above
	print('checking NOW...',real_freq.shape)
	BIT3,BIT4=255,255
	counter=0
	code = np.zeros((CODE_HEIGHT,CODE_WIDTH*2),np.uint8)
	noise=np.zeros((CODE_HEIGHT,CODE_WIDTH*2),np.uint8)
	AREA = patch_r*patch_th
	for i in range(0,CODE_HEIGHT): #19:
		for j in range(0,CODE_WIDTH):
			patch_real = np.sum(real_freq[i*patch_r:(i+1)*patch_r,j*patch_th:(j+1)*patch_th])/AREA
			patch_imag = np.sum(imag_freq[i*patch_r:(i+1)*patch_r,j*patch_th:(j+1)*patch_th])/AREA
			if (patch_real>=0) and (patch_imag>=0):
				BIT1,BIT2=255,255
			elif (patch_real>=0) and (patch_imag<0):
				BIT1,BIT2 = 0,255
			elif (patch_real<0) and (patch_imag<0):
				BIT1,BIT2 = 0,0
			elif (patch_real<0) and (patch_imag>=0):
				BIT1,BIT2 = 255,0
			code[i,2*j]=BIT1
			code[i,2*j+1]=BIT2
	#quantized based on phase

	print('code size: ',code.size)
	return code,noise


def match(code,template):
	code_original = np.ravel(code)
	template=cv2.imread(template,0)
	template=np.ravel(template)
	template=template/255
	code=code_original/255
#	code_original=np.random.randint(2,size=len(template)) #was to test
	#print('size',len(code),'code',code)
	#print('size',len(template),'template',template)
	tally=0
	distances=[]
	shift=[]
	for shifts in range(-2,3,1): #was -100 and 101,2 -10.11,2
		tally=0
		t = np.roll(code_original,shifts)
		t=np.ravel(t)/255
		for i in range(0,len(code)): #was template
			tally+=int(t[i])^int(template[i])
		HD=tally/len(template) #per rotation
		print('HD of',HD,'for shift of: ',shifts*0.024,'degrees')
		distances.append(HD)
	min_HD = min(distances)
	print('Min distance of',min_HD)

	return min_HD






####################### end of functions ###############################
