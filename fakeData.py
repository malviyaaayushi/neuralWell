from __future__ import print_function

import sys
import random 
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def makePixel(binary):
	if binary:
		coin = random.random()
		if coin > 0.5:
			intensity = 1
		else:
			intensity = 0
	else:
		intensity = random.random()
	return intensity

def greenCurtain(img_name, op_path, size_x, size_y, rfi_axis, rfi_start, rfi_width, binary):
	img = [[0 for j in range(size_x)] for i in range(size_y)]
	
	for i in range(size_y):
		for j in range(size_x):
			intensity = makePixel(binary)
			if ((rfi_axis=='y' or rfi_axis=='Y') and (j>=rfi_start and j<=rfi_start+rfi_width)) or ((rfi_axis=='x' or rfi_axis=='X') and (i>=rfi_start and i<=rfi_start+rfi_width)):
				coin = random.random()
				if ((rfi_axis=='y' or rfi_axis=='Y') and (j<=rfi_start+int(rfi_width*0.1) or j>=rfi_start+int(rfi_width*0.1))) or ((rfi_axis=='x' or rfi_axis=='X') and (i<=rfi_start+int(rfi_width*0.1) and i>=rfi_start+int(rfi_width*0.9))):
					bais = 0.1
				else:
					bais = 0.0
				if coin < 0.01+bais:
					intensity = 0
				else:
					intensity = 1
				
			img[i][j] = intensity
			#print(str(intensity)+" ", end='')
		#print()

	plot(img, op_path+img_name+'.png')

def pulsar(img_name, op_path, size_x, size_y, rfi_start_x, rfi_end_x, rfi_start_y, rfi_end_y, rfi_width, binary):
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
				if ((i*j>c_1 and i*j<c_2) or (i*j>c_3 and i*j<c_4)):
					bais = 0.1
				else:
					bais = 0.0
				if coin < 0.01+bais:
					intensity = 0
				else:
					intensity = 1

				
			img[i][j] = intensity
			#print(str(intensity)+" ", end='')
		#print()

	plot(img, op_path+img_name+'.png')

def plot(img, imgName=''):
	H = np.matrix(img)
	fig = plt.figure(frameon=False)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
	#ax = fig.add_subplot(1,1,1)
	plt.imshow(H, interpolation='none', aspect='auto')
	#ax.set_aspect('equal')
	#plt.colorbar(orientation='vertical')
	plt.savefig(imgName)
	#plt.show()


if __name__ == "__main__":
	if len(sys.argv)!=11:
		print ("Usage: fakeData.py op_path size_x size_y rfi_start_range_x rfi_end_range_x rfi_start_range_y rfi_end_range_y rfi_width num_images binary")
		exit(-1)

	op_path = sys.argv[1]+"/"
	size_x = int(sys.argv[2])
	size_y = int(sys.argv[3])
	#rfi_axis = sys.argv[4]
	#if rfi_axis!='x' and rfi_axis!='X' and rfi_axis!='y' and rfi_axis!='Y' and rfi_axis!='p' and rfi_axis!='P':
	#	print("RFI axis incorrect. Choose one of the following values: x, y, p, X, Y, P\n")
	#	sys.exit(-1)
	
	rfi_start_range_x = int(sys.argv[4])
	rfi_end_range_x = int(sys.argv[5])
	rfi_start_range_y = int(sys.argv[6])
	rfi_end_range_y = int(sys.argv[7])
	rfi_width = int(sys.argv[8])
	num_images = int(sys.argv[9])
	if int(sys.argv[10]):
		binary = 1
	else:
		binary = 0
	
	if(not rfi_start_range_x and not rfi_end_range_x):
		rfi_axis = 'y'
		for i in range(num_images):
			rfi_start = random.randint(rfi_start_range_y, rfi_end_range_y)
			greenCurtain(rfi_axis+"_"+str(i), op_path, size_x, size_y, rfi_axis, rfi_start, rfi_width, binary)
	elif(not rfi_start_range_y and not rfi_end_range_y):
		rfi_axis = 'x'
		for i in range(num_images):
			rfi_start = random.randint(rfi_start_range_x, rfi_end_range_x)
			greenCurtain(rfi_axis+"_"+str(i), op_path, size_x, size_y, rfi_axis, rfi_start, rfi_width, binary)
	else:
		rfi_axis = 'pulsar'
		for i in range(num_images):
			pulsar(rfi_axis+"_"+str(i), op_path, size_x, size_y, rfi_start_range_x, rfi_end_range_x, rfi_start_range_y, rfi_end_range_y, rfi_width, binary)

	#subset.saveAsTextFile(opFileName)
