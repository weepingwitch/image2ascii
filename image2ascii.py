#HA i coded this in an hour and a half and it doesn't look too bad

#import libraries for reading/writing images
from PIL import Image, ImageFilter
import os

#import libraries for reading command line arguments
import sys, getopt

#import numpy for processing arrays
import numpy

def main(argv):
    inputfile, outputfile, depth = processargs(argv)

    #try opening the image
    try:
        myimg = Image.open(inputfile)
    except IOError:
        print "Error reading image file"
        sys.exit(2)

    #prepare the image
    pixelatedimage = prepareimage(myimg, depth)
    #turn it to an array
    pixarray = makearray(pixelatedimage)
    #process the array
    procarray = converttochars(pixarray)

    #write the output
    fo = open(outputfile,'w')
    for row in procarray:
        #print row
        for val in row:
            fo.write(val)
        fo.write('\n')
    fo.close()



#convert to characters based on value
def converttochars(pixarray):
    #array of chars in increasing darnkess
    chars = [' ', '.','-','~','!',']','}','$','%','&','@','#']
    procarray = numpy.chararray(pixarray.shape)
    k = 0
    for row in pixarray:
        j = 0
        for val in row:
            val = 255.0-val
            i =  ((len(chars)-1)*(val/255.0))
            i = int(i)
            procarray[k][j] = chars[i]
            j+=1
        k+=1
    return procarray


#get array of  pixel values
def makearray(pixelatedimage):
    pixels = numpy.asarray(pixelatedimage)
    return pixels


#turn image into a square, black and white, and pixelated
def prepareimage(myimg, depth):
        #find dimensions for square image
        width, height = myimg.size
        if (width > height):
            newsize = width
        else:
            newsize = height
        if (newsize%2 == 1):
            newsize += 1

        #create white square, paste original image over it
        sqimg = Image.new('RGBA', (newsize, newsize), (255, 255, 255, 255))
        offset = ((newsize - width)/2, (newsize - height) / 2)
        sqimg.paste(myimg, offset)

        #turn to monochrome
        sqimg = sqimg.convert("L")


        #calculate pixelation depth
        depth = depth / 100
        pixfactor = newsize * depth
        pixfactor = int(pixfactor)


        #pixelate
        pixelatedimage = sqimg.copy()
        pixelatedimage.thumbnail((pixfactor,pixfactor))
        pixelatedimage = pixelatedimage.resize((pixfactor*2,pixfactor))

        #output progress image, for debugging
        progimg = pixelatedimage.resize((newsize,newsize))
        progimg.save("progress.png","png")

        return pixelatedimage




# process command line arguments
def processargs(argv):
    #set defaults
    inputfile = ''
    outputfile = 'out.txt'
    depth = 8.0;
    #try reading args using getopt
    try:
       opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=","ofile=","depth="])
    except getopt.GetoptError:
       print 'usage: image2ascii.py -i <inputfile> -o <outputfile> -d <depth>\n<depth> should be between 1 and 100 inclusive'
       sys.exit(2)
    #process the args
    for opt, arg in opts:
        if opt == '-h':
            print 'usage: image2ascii.py -i <inputfile> -o <outputfile> -d <depth>\n<depth> should be between 1 and 100 inclusive'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--depth"):
            depth = float(arg)

    #make sure there is an input file
    if inputfile == '':
         print 'usage: image2ascii.py -i <inputfile> -o <outputfile> -d <depth>\n<depth> should be between 1 and 100 inclusive'
         sys.exit(2)


    #make sure depth is correct
    if depth < 1 or depth > 100:
        print 'usage: image2ascii.py -i <inputfile> -o <outputfile> -d <depth>\n<depth> should be between 1 and 100 inclusive'
        sys.exit(2)

    #print 'Input file is "', inputfile
    #print 'Output file is "', outputfile
    #print 'Depth is ', depth

    return inputfile, outputfile, depth



if __name__ == "__main__":
   main(sys.argv[1:])
