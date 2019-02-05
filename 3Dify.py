from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import time


def translate(value, leftMin, leftMax, rightMin, rightMax):
    #Maps values from one range to another
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

path = 'yourpath/imagename.extension'
subdir = 'subdirectory/for/your/output'

img1=mpimg.imread(path)
f = plt.figure(100)
plt.imshow(img1)
f.show()
f.suptitle('Does this image look correct? Close it to proceed :)', fontsize=12)

plt.show()
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



print("Maximum: " + str(img.max()) + " Brightness\nSize: " + str(img.size) + " Pixel\nShape: " + str(img.shape) + " Pixel")
x, y = img.shape
x_axis = np.arange(x)
y_axis = np.arange(y)


#since rotating by hand takes so long, this function will save you an image at various angles and save it to your specified subdirectory

substeps= 15 #how many images do you want?

for step in range(substeps):

    fig = plt.figure(step) # this results in all $substeps amount of images will open and close after the script finished. To avoid this, just name all figures 1, but then you will render one image on top of the other and you will see the axis labels as artifacts on the sides
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

        ax.scatter(xs, ys, zs, zdir='z', s=20, c=colormap, marker='$.$', depthshade=True)

    ax.view_init(azim=(step*10), elev=90-(step*(90/substeps)))
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
