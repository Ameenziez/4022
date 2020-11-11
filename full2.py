import cv2
import numpy as np
from matplotlib import pyplot as plt
from iris_code5 import feature_extract,match
from proto3 import recognition
#change source of templates again

temp_choice = input('USE X or NUMBER? ')
leftright=str(input('Left or Right?' ))
leftright2 = str(input('Compare against L or R?'))
if temp_choice =='X' or temp_choice=='x':
	template='codes2/CODEX.bmp' #convention is CODESUBJECT_L.BMP #was not code2
	#template_noise = 'noise/CODEX.bmp'
else:
	if leftright == 'R' or leftright== 'r':
		template='codes2/CODE'+str(temp_choice)+'_R.bmp'
	else:
		template='codes2/CODE'+str(temp_choice)+'_L.bmp'
distances_total = []
distances=[]
not_found = []
subject = input('enter subject: ')
lower = input('enter lower: ')
upper = input('enter upper: ')
save = input('SAVE?(1 or 0):' )
wait = input('Wait? 1 or 0: ' )
if eval(subject)<10:
	subject_string = '00'+str(subject)
elif(eval(subject))>=100:
	subject_string=str(subject)
else:
	subject_string ='0'+str(subject)



for i in range(int(lower),int(upper)):
	if i>=10:
		photo = str(i)
		print('zzz')
	else:
		photo = '0'+str(i)
	if leftright2 =='L' or leftright2=='l':
		#im = '/media/ameen/B301-16DE/IITD Database/'+subject_string+'/0'+str(i)+'_L.bmp'
		im = '/media/ameen/B301-16DE/IITD Database/'+subject_string +'/'+photo+'_L.bmp' #2,4 JUNK 9 needs bigger centre guess
	elif leftright2 =='R' or leftright2 =='r':
		im = '/media/ameen/B301-16DE/IITD Database/'+subject_string+'/'+photo+'_R.bmp'
	HD,found,C = recognition(im,template,1-int(wait),int(save)) # number for waitkey
	distances.append(HD)


for el in distances:
	print(el)


