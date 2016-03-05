from __future__ import print_function

import sys, random, os, yaml, pickle, gzip

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def makePixel(binary):
	return (1 if random.random() > 0.5 else 0) if binary else random.random()

def rfiCurtain(img_name, op_path, size_x, size_y, binary):
	rfi_axis = 'x' if random.random()>0.5 else 'y'
	if rfi_axis == 'x':
		rfi_start = random.randint(1,size_x)
		rfi_width = int(size_x/(10*random.randint(1,size_x)))
	else:
		rfi_start = random.randint(1,size_y)
		rfi_width = int(size_y/(10*random.randint(1,size_y)))
	img = [[0 for j in range(size_x)] for i in range(size_y)]
	for i in range(size_y):
		for j in range(size_x):
			intensity = makePixel(binary)
			if ((rfi_axis=='y') and (j>=rfi_start and j<=rfi_start+rfi_width)) or ((rfi_axis=='x') and (i>=rfi_start and i<=rfi_start+rfi_width)):
				bais = 0.1 if ((rfi_axis=='y') and (j<=rfi_start+int(rfi_width*0.1) or j>=rfi_start+int(rfi_width*0.1))) or ((rfi_axis=='x') and (i<=rfi_start+int(rfi_width*0.1) and i>=rfi_start+int(rfi_width*0.9))) else 0.0
				intensity = 0 if random.random() < 0.01+bais else 1				
			img[i][j] = intensity
	return (np.matrix(img),1)
	#plotImg(img, op_path+img_name+'.png')

def pulsarCurtain(img_name, op_path, size_x, size_y, binary):
	rfi_start_x = random.randint(1,size_x)
	rfi_end_x =  random.randint(1+rfi_start_x,size_x)
	rfi_start_y = random.randint(1,size_y)
	rfi_end_y = random.randint(1+rfi_start_y,size_y)
	rfi_width = random.randint(1,3)
	img = [[0 for j in range(size_x)] for i in range(size_y)]
	c_1 = (((rfi_start_x+rfi_end_x)/2.0)*((rfi_start_y+rfi_end_y)/2.0))
	c_2 = (((rfi_start_x+rfi_end_x)/2.0+rfi_width*0.1)*((rfi_start_y+rfi_end_y)/2.0+rfi_width*0.1))
	c_3 = (((rfi_start_x+rfi_end_x)/2.0+rfi_width*0.9)*((rfi_start_y+rfi_end_y)/2.0+rfi_width*0.9))
	c_4 = (((rfi_start_x+rfi_end_x)/2.0+rfi_width)*((rfi_start_y+rfi_end_y)/2.0+rfi_width))
	for i in range(size_y):
		for j in range(size_x):
			intensity = makePixel(binary)
			if ((i>=rfi_start_y and i<=rfi_end_y and j>=rfi_start_x and j<=rfi_end_x) and (i*j>c_1 and i*j<c_4)):
				coin = random.random()
				bais = 0.1 if ((i*j>c_1 and i*j<c_2) or (i*j>c_3 and i*j<c_4)) else 0.0
				intensity = 0 if coin < 0.01+bais else 1				
			img[i][j] = intensity
	return (np.matrix(img),-1)
	#plotImg(img, op_path+img_name+'.png')

def plotImg(img, imgName=''):
	H = np.matrix(img)
	fig = plt.figure(frameon=False)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
	plt.imshow(H, interpolation='none', aspect='auto')
	plt.savefig(imgName)


def generateRandomData(img_name, op_path, size_x, size_y, binary):
	if(random.random()>0.5):
		return rfiCurtain(img_name, op_path, size_x, size_y, binary)
	else:
		return pulsarCurtain(img_name, op_path, size_x, size_y, binary)

def generateNormalData():
	pass

if __name__ == "__main__":
	if len(sys.argv)!=6:
		print ("Usage: fakeData.py op_path size_x size_y binary num_images")
		exit(-1)

	op_path = sys.argv[1]+"/"
	size_x = int(sys.argv[2])
	size_y = int(sys.argv[3])	
	binary = 1 if int(sys.argv[4]) else 0
	num_images = int(sys.argv[5])
	
	samples = list()
	for imgcnt in xrange(1,num_images):
		img_name = "img_"+str(imgcnt)
		samples.append(generateRandomData(img_name, op_path, size_x, size_y, binary))

	with gzip.open("data/data.pkl.gz", "wb") as zipFile:
		pickle.dump(samples, zipFile)
	zipFile.close()

	with gzip.open("data/data.pkl.gz", "rb") as f:
		file_content = f.read()
	print(file_content)