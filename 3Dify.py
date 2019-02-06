from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import time
import cv2
import os
import imageio


#####init
filename = 'lenna.png'
path = '/path/to/your/image/'
subdir, disregard = filename.split('.')  # subdir to save images and gif
substeps = 16  #how many images do you want?
horRot = 10  #how many degrees horizontal rotation per step
verRot = 90/substeps  #how many degrees vertical rotation per step
mymarker = '$.$' #set any marker style you want like 'o', ',', '*',...
gifFPS = 5 #frames per second of the resulting gif
####endinit


def translate(value, leftMin, leftMax, rightMin, rightMax):
    #Maps values from one range to another
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

if not os.path.exists(subdir):
    os.makedirs(subdir)


img1=mpimg.imread(path+filename)
start = time.time()


print("Image dimensions:")

print(img1.shape)

if(len(img1.shape)>2):
    #bringing it down to a 2x2 array with only the greyscale values
    hoehe, breite, z = img1.shape
    img2 = img1[:, :, 0]
else:
    hoehe, breite = img1.shape
    img2= img1


if( hoehe > breite ):
    size = breite
else:
    size = hoehe

#cropping the image to a square
img = img2[0:size, 0:size]

if(size>1000): #if the image has more than 1MP we scale it down
    img = cv2.resize(img, (1000, 1000))

f = plt.figure(100)
plt.imshow(img)
f.show()
f.suptitle('Does this image look correct? Close it to proceed :)', fontsize=12)

plt.show()


#histogram equalisation for better outcome
# create a CLAHE object (Arguments are optional).
plt.hist(img.ravel(), 256, [0, 256])  #check histogramm for debugging
plt.show()
try:
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    print(img.shape)
    img = clahe.apply(img)
    f = plt.figure(100)
    plt.imshow(img)
    f.show()
    f.suptitle('Does this image look correct? Close it to proceed :)', fontsize=12)
    plt.show()

except:
    print("check the histogram of this file")



print("Maximum: " + str(img.max()) + " Brightness\nSize: " + str(img.size) + " Pixel\nShape: " + str(img.shape) + " Pixel")
x, y = img.shape
x_axis = np.arange(x)
y_axis = np.arange(y)

#since rotating by hand takes so long, this function will save you an image at various angles and save it to your specified subdirectory


fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
column1 = img[:, [0]]
colormap = np.empty(size)
xs = np.arange(size)

for i in range(size):
    ys = np.full((y), i)
    zs = img[:, [i]]
    max = zs.max()
    for o in range(zs.size):
        colormap[o]=translate(zs[o], 0, 255, 0, 1)

    ax.scatter(xs, ys, zs, zdir='z', s=20, c=colormap, marker=mymarker, depthshade=True)

for step in range(substeps):
    ax.view_init(azim=(step*horRot), elev=90-(step*verRot))
    ax.set_xlabel('Image Height')
    ax.set_ylabel('Image Width')
    ax.set_zlabel('Pixel Brightness')
    ax.margins(x=0, y=-0.25)   # Values in (-0.5, 0.0) zooms in to center

    fig.show()
    plt.savefig(subdir+'/'+str(step)+'.png')

    # uncomment this if you want to show the png for live movement
    # plt.show()

end = time.time()
print("Done in " + str(end - start) + " seconds")


filenames = []

for i in reversed(range(substeps)):
    filenames.append(subdir+'/'+str(i)+'.png')

filenames.append(subdir+'/'+str(0)+'.png')
filenames.append(subdir+'/'+str(0)+'.png')

for i in range(substeps):
    filenames.append(subdir+'/'+str(i)+'.png')

images = []
for myfilename in filenames:
    images.append(imageio.imread(myfilename))
imageio.mimsave(path + subdir + '/' +subdir +'_3D.gif', images, fps=gifFPS)

end = time.time()
print("Gif created in " + str(end - start) + " seconds")
