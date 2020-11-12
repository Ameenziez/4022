import cv2
import numpy as np
from matplotlib import pyplot as plt
from iris_code5 import feature_extract,match
from proto3 import recognition #changed

which = input('which template?')
which = int(which)
lr=str(input('left or right?'))
lr=lr.upper()
text= 'textfinal/text'+str(which)+lr+'.txt'
file = open(text,'w')
template='codes2/CODE'+str(which)+'_'+lr+'.bmp'
distances_total = []
distances_subject=[]
problems = []
lower = input('Enter lower bound:' )
upper = input('Enter upper bound:' )
matches = []
threshold = 0.44 #was 0.44 not final
#if subject<10:
#	subject_string = '00'+str(subject)
#else:
#	subject_string ='0'+str(subject)

for subject in range(int(lower),int(upper)+1):
	#distances_subject.clear()
#	if subject==59:
	#	subject=60 #59 has unknown error
	print('######## SUBJECT'+ str(subject)+' ############')
	distances_subject.append('| Subject:'+str(subject)+'__________________')
	for photos in range(1,11):
			if subject<10:
				subject_string = '00'+str(subject)
			elif subject>=100:
				subject_string = str(subject)
			else:
				subject_string ='0'+str(subject)
			if subject>13 and photos>5 and subject !=27 and subject != 55 and subject != 65:
				LR='R'
			elif (subject==27 or subject==65 or subject==55) and photos>6:
				LR='R'
			else:
				LR='L'

			if photos>9:
				photo_string=str(photos)
			else:
				photo_string='0'+str(photos)
		#im = '/media/ameen/B301-16DE/IITD Database/001/08_L.bmp' #2,4 JUNK 9 needs bigger centre guess
			im = '/media/ameen/B301-16DE/IITD Database/'+subject_string+'/'+photo_string+'_'+LR+'.bmp' #2,4 JUNK 9 needs bigger centre guess
			HD,found = recognition(im,template,1,False) # number for waitkey
			distances_subject.append(HD)
			if HD<threshold:
				matchy = 'SUBJECT '+str(subject)+' photo number: '+str(photos)+' w HD: '+str(HD)
				matches.append(matchy)
			if found==False: #problem subjects for inspection
				issue='SUBJECT '+str(subject)+ 'photo number '+ str(photos)
				problems.append(issue)
	#distances_total.append(distances_subject)


#for el in distances_subject:
#	print(el)
#print(distances_subject)
HEADING1 = '################ MATCHES:################\n'
print(HEADING1)
file.write(HEADING1)
for j in  matches:
	print(j)
	file.write(str(j)+'\n')
HEADING2 = '################DISTANCES###############\n'
file.write(HEADING2)
for d in distances_subject:
	print(d)
	file.write(str(d)+'\n')
HEADING2= '############### Problems:#################### \n '
print(HEADING2)
#file.write(HEADING2)
for q in problems:
	print(q)
#	file.write(str(q)+'\n')
file.close()


