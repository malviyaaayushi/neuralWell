from __future__ import print_function

import sys, random, os, yaml

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def makePixel(binary):
	return (1 if random.random() > 0.5 else 0) if binary else random.random()

def rfiCurtain(img_name, op_path, size_x, size_y, rfi_axis, rfi_start, rfi_width, binary):
	dataString = list()
	dataString.append(1)
	img = [[0 for j in range(size_x)] for i in range(size_y)]
	for i in range(size_y):
		for j in range(size_x):
			intensity = makePixel(binary)
			if ((rfi_axis=='y' or rfi_axis=='Y') and (j>=rfi_start and j<=rfi_start+rfi_width)) or ((rfi_axis=='x' or rfi_axis=='X') and (i>=rfi_start and i<=rfi_start+rfi_width)):
				bais = 0.1 if ((rfi_axis=='y' or rfi_axis=='Y') and (j<=rfi_start+int(rfi_width*0.1) or j>=rfi_start+int(rfi_width*0.1))) or ((rfi_axis=='x' or rfi_axis=='X') and (i<=rfi_start+int(rfi_width*0.1) and i>=rfi_start+int(rfi_width*0.9))) else 0.0
				intensity = 0 if random.random() < 0.01+bais else 1				
			img[i][j] = intensity
			dataString.append(intensity)
	populateData(img_name,dataString)
	#plotImg(img, op_path+img_name+'.png')

def pulsarCurtain(img_name, op_path, size_x, size_y, rfi_start_x, rfi_end_x, rfi_start_y, rfi_end_y, rfi_width, binary):
	dataString = "0"
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
			dataString+=", "+str(intensity)
	populateData(img_name, dataString)
	plotImg(img, op_path+img_name+'.png')

def plotImg(img, imgName=''):
	H = np.matrix(img)
	fig = plt.figure(frameon=False)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
	plt.imshow(H, interpolation='none', aspect='auto')
	plt.savefig(imgName)


def populateData(imgName, dataString):
	document = dict(
		imgName = imgName,
		dataString = dataString
	)
	with open("dataFile.yaml", "a") as dataFile:
		dataFile.write(yaml.dump(document, default_flow_style=True))
	#doc = open('dataFile.yaml').read()
	#print(yaml.load(doc))

if __name__ == "__main__":
	if len(sys.argv)!=11:
		print ("Usage: fakeData.py op_path size_x size_y rfi_start_range_x rfi_end_range_x rfi_start_range_y rfi_end_range_y rfi_width num_images binary")
		exit(-1)

	op_path = sys.argv[1]+"/"
	size_x = int(sys.argv[2])
	size_y = int(sys.argv[3])	
	rfi_start_range_x = int(sys.argv[4])
	rfi_end_range_x = int(sys.argv[5])
	rfi_start_range_y = int(sys.argv[6])
	rfi_end_range_y = int(sys.argv[7])
	rfi_width = int(sys.argv[8])
	num_images = int(sys.argv[9])
	binary = 1 if int(sys.argv[10]) else 0
	
	if(not rfi_start_range_x and not rfi_end_range_x):
		rfi_axis = 'y'
		for i in range(num_images):
			rfi_start = random.randint(rfi_start_range_y, rfi_end_range_y)
			rfiCurtain(rfi_axis+"_"+str(i), op_path, size_x, size_y, rfi_axis, rfi_start, rfi_width, binary)
	elif(not rfi_start_range_y and not rfi_end_range_y):
		rfi_axis = 'x'
		for i in range(num_images):
			rfi_start = random.randint(rfi_start_range_x, rfi_end_range_x)
			rfiCurtain(rfi_axis+"_"+str(i), op_path, size_x, size_y, rfi_axis, rfi_start, rfi_width, binary)
	else:
		rfi_axis = 'pulsar'
		for i in range(num_images):
			pulsarCurtain(rfi_axis+"_"+str(i), op_path, size_x, size_y, rfi_start_range_x, rfi_end_range_x, rfi_start_range_y, rfi_end_range_y, rfi_width, binary)