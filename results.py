import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import matplotlib.ticker as plticker


K=1 #weighting
files = ['1L','3L','4L','5L','10L','9L','12L','22L','29L','30L','35L','39L','40L','43L','51L','63L','64L','71L','77L','78L','88L','100L','102L','103L','105L']
numbersonly=[]
genuines=[]
all=[]
threshold=0.454
for numbers in files:
	relevant=[]
	file = open('text'+numbers+'.txt','r')
	text=file.readlines()
	i=0
	start=0
	for lines in text: #find where to start recording values
		if lines =='################DISTANCES###############\n':
			start = i
			print('start is ',i)
			break
		i+=1
	matches = text[1:start]
	genuine=[]

	count=0
	skip=False
	print(genuine)
	start+=1 #start after distance header
	relevant = text[start:] #only consider values after header

	for elements in relevant:
		if elements[0]=='|': #ignore  lines containing subject name
			line = elements.split(' ')
#		print(line[1])

		#b = line[1].rstrip('_')
			b = line[1].strip('Subject:')
			b=b.strip('\n')
			b = b.strip('_')
			if int(numbers[:len(numbers)-1])==int(b):
			#gen.append()for i in range(0,11):
				skip=True
				if int(b)<13:
					count=10
				else:
					count=5
			else:
				pass
		elif count==0:
			numbersonly.append(elements.strip('\n'))
		elif skip==True and count !=0:
			count-=1
			genuines.append(elements.strip('\n'))
#		print('skipped: '+elements)
			pass

print(genuines)
threshes = np.arange(0,1.01,0.001)
FAR=[]
FAR_k=[]
FRR_k=[]
FRR=[]
try:
	while True:
		genuines.remove('0.0') #added to ignore unsuitable or subject image
except ValueError:
	pass

#remove multiline comment to get graph (takes long so commented out for now)
'''
#print(genuines)
for value in threshes:
	FAR_count=0
	FRR_count=0
	#FRR_count_k=0
	#FAR_count_k=0
	for j in genuines:
#                print(j)
		if float(j)>value:
			FRR_count+=K
		else:
			print(float(j), 'and thresh: ',value)
	FRR.append(FRR_count/len(genuines)*100)
	for k in numbersonly:
		if float(k)<=value:
			FAR_count+=1
	FAR.append(FAR_count/len(numbersonly)*100)

print('FRR:',FRR)
print('length of FRR:',len(FRR),'vs','length of threshes:',len(threshes))
print('length of FRR:',len(FAR),'vs','length of threshes:',len(threshes))
#plt.stem(FRR,[threshes])
plt.xlabel('Decision Threshold')
plt.ylabel('Accept/Reject Probability (%)')
plt.plot(threshes,FAR,'r',threshes,FRR,'b')
plt.title('Accuracy versus Sensitivity')
plt.legend(('FAR','FRR'))
plt.show()


plt.xlabel('FAR (%)')
plt.ylabel('FRR (%)')
plt.plot(FAR,FRR,'g')
plt.title('Relation between FAR and FRR')
plt.show()
'''


print('Number imposters: ',len(numbersonly))
print('Number genuines: ',len(genuines))
#print(genuines)
numbersonly = [round(float(num),2) for num in numbersonly] #round numbers to 2 sig figures
numbersonly.sort() #ascending order
genuines = [round(float(num),2) for num in genuines] #round numbers to 2 $
genuines.sort() #ascending order
gen_match = [i for i in genuines if i<=threshold]
#print('matches:', gen_match)
'''
threshes = np.arange(0,1.01,0.01)
FAR=[]
FRR=[]
for value in threshes:
	FAR_count=0
	FRR_count=0
	for j in genuines:
		#print(j)
		if j>=value:
			FRR_count+=1
	FRR.append(FRR_count/len(genuines))

	for k in numbersonly:
		if k<=value:
			FAR_count+=1
	FAR.append(FAR_count/len(numbersonly))

print('FRR:',FRR)
print('length of FRR:',len(FRR),'vs','length of threshes:',len(threshes))
print('length of FRR:',len(FAR),'vs','length of threshes:',len(threshes))
plt.stem(FRR,[threshes])
plt.plot(threshes,FAR,'r',threshes,FRR,'b')
plt.show()
'''




print('Max is ',(max(numbersonly)), ' Min is ', min(numbersonly))
labels,values = zip(*Counter(numbersonly).items())
print(labels)
indices = np.arange(len(labels))
width = 1
imposters=plt.bar(indices,values,width,color='red')
plt.xticks(indices+width*0.5,labels)
plt.title('Imposter scores')
plt.xlabel('Hamming distances')
plt.ylabel('Number of scores')
plt.show()



#fig,ax = plt.subplots()
labels2,values2 = zip(*Counter(genuines).items())
#labelscombined=labels+labels2
#print(labels2)
indices2 = np.arange(len(labels2))
#print(indices2)
#indicescombined = np.arange(len(indices)+len(indices2))
#print(indicescombined)
width2 = 1
gens=plt.bar(indices2,values2,width2,color='blue')

#plt.xticks(indices+width*0.5,labels)
#loc = plticker.MultipleLocator(base=1)
#ax.xaxis.set_major_locator(loc)
#plt.setp(labels2,rotation=30,horizontal_alignment='right')
plt.xticks(indices2+width2*0.5,labels2)
plt.title('Genuine scores')
plt.xlabel('Hamming distances')
plt.ylabel('Number of scores')
plt.show()

file.close()
