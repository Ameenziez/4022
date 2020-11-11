import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

number = str(input('which file? '))
lr = str(input('L or R?'))
file = open('text'+number+lr.upper()+'.txt','r')
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
gens=[]


count=0
skip=False
print(genuine)
start+=1 #start after distance header
relevant = text[start:] #only consider values after header
numbersonly =[]
for elements in relevant:
	if elements[0]=='|': #ignore  lines containing subject name
		line = elements.split(' ')
#		print(line[1])
		#b = line[1].rstrip('_')
		b = line[1].strip('Subject:')
		b=b.strip('\n')
		b = b.strip('_')
		if int(number)==int(b):
			#gen.append()for i in range(0,11):
			skip=True
			count=10
		else:
			pass
	#if skip==True and count!=0:
		#count-=1
		#pass
	elif count==0:
		numbersonly.append(elements.strip('\n'))
	elif skip==True and count !=0:
		count-=1
#		print('skipped: '+elements)
		gens.append(elements.strip('\n'))
		pass

print('Number imposters: ',len(numbersonly))
numbersonly = [round(float(num),2) for num in numbersonly] #round numbers to 2 sig figures
numbersonly.sort() #ascending order
gens = [round(float(num),2) for num in gens]
gens.sort()
gens.remove(0.0)
print('mean is',np.mean(gens),' and std dev is ',np.std(gens))
#print('initial length of: ',len(numbersonly))
#for i in range(len(genuine)):
#	numbersonly.remove(genuine[i]) #remove genuine scores from imposter list
#print('number of genuines: ',len(genuine))
#print('adjusted length of: ',len(numbersonly))


print('Max is ',(max(numbersonly)), ' Min is ', min(numbersonly))
labels,values = zip(*Counter(numbersonly).items())
indices = np.arange(len(labels))
width = 1
BAR=plt.bar(indices,values,width,color='red')
plt.xticks(indices+width*0.5,labels)
plt.title('Imposter scores')
plt.xlabel('Hamming distances')
plt.ylabel('Number of scores')
plt.show()


print('Max is ',(max(gens)), ' Min is ', min(gens))
labels,values = zip(*Counter(gens).items())
indices = np.arange(len(labels))
width = 1
BAR=plt.bar(indices,values,width,color='blue')
plt.xticks(indices+width*0.5,labels)
plt.title('Genuine scores')
plt.xlabel('Hamming distances')
plt.ylabel('Number of scores')
plt.show()





file.close()
