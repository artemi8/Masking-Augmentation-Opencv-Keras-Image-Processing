#!/usr/bin/env python
 
# Make sure you have three folders namely
# dataset, masks, mask_inv
# dataset folder must contain images with name as numbers starting from 1,2,3...
'''
Keys:
  r     - Mask the image
  SPACE - Reset the inpainting mask
  ESC   - Skip current image
  z     - Exit program
'''
from __future__ import print_function
 
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import sys # Enables the passing of arguments
import os #Enables walking through the directories
 
class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)
 
    def show(self):
        cv2.namedWindow(self.windowname,cv2.WINDOW_NORMAL)
        cv2.imshow(self.windowname, self.dests[0])
 
    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_pt = None
 
        if self.prev_pt and flags & cv2.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_pt, pt, color, 3)
            self.dirty = True
            self.prev_pt = pt
            self.show()
 
 
# Define the path of the dataset and mask
IMG_PATH = "DATASET DIRECTORY"
MASK_OUTPUT_PATH = "MASK OUTPUT PATH"
MASK_INV = "MASK INV DIRECTORY"


BREAK_LIMIT = 10 # Program exits after every 20 images
COUNTER_FILE = "counter_file.txt" #counter file to pause and resume mask operation



def masked_region(mask, src_img):
    mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR) #change mask to a 3 channel image 
    mask_out=cv2.subtract(mask,src_img)
    mask_out=cv2.subtract(mask,mask_out)
    return mask_out

def read_file(file):
    try:
        counter_file = open(file, "r") 
        count = counter_file.read()
        counter_file.close()
        return int(count)
    except FileNotFoundError:
        count = 0
        print("Creating counter file...")
        write_file(file, count)
        return int(count)


def write_file(file, count):
    counter_file = open(file, "w")
    counter_file.write(str(count))
    counter_file.close()
    


def main():

    # Load the image and store into a variable
    COUNT = read_file(COUNTER_FILE)
    OCCURENCES = 0

    for img_name in range(COUNT+1, COUNT + BREAK_LIMIT + 1):
        while True :
            try:
                image = cv2.imread(IMG_PATH + str(img_name) + ".jpg")
                print(IMG_PATH + str(img_name) + ".jpg")
        
                if image is None:
                    print('Failed to load image file:', image)
                    sys.exit(1)
 
                # Create an image for sketching the mask
                image_mark = image.copy()
                sketch = Sketcher('Image', [image_mark], lambda : ((175, 160, 255), 255))

                # Sketch a mask
                while True:
                    ch = cv2.waitKey()
                    if ch == 27: # ESC - exit
                        break
                    if ch == ord('r'): # r - mask the image
                        break
                    if ch == ord(' '): # SPACE - reset the inpainting mask
                        image_mark[:] = image
                        sketch.show()
                    if ch == ord("z"): # z - exit program
                        write_file(COUNTER_FILE, img_name-1)
                        print("Exited at " + str(img_name-1))
                        sys.exit(1)
 
                # define range of pink color in HSV
                lower_white = np.array([155, 140, 255])
                upper_white = np.array([175 ,160, 255])
 
                # Create the mask
                border_mask = cv2.inRange(image_mark, lower_white, upper_white)
                mask_copy = border_mask.copy()
    
                # Perform morphology
                se = np.ones((7,7), dtype='uint8')
                image_close = cv2.morphologyEx(mask_copy, cv2.MORPH_CLOSE, se)

                # Your code now applied to the closed image
                cnt = cv2.findContours(image_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
                filled_mask = np.zeros(border_mask.shape[:2], np.uint8)
                cv2.drawContours(filled_mask, cnt, -1, 255, -1)

                masked_reg = masked_region(filled_mask, image)
                cv2.destroyAllWindows()
                

                cv2.namedWindow("Masked Region", cv2.WINDOW_NORMAL)
                cv2.imshow("Masked Region", masked_reg)
                FLAG = cv2.waitKey()

                if FLAG == ord("y"):
                    cv2.imwrite(MASK_INV + "mask_inv_" + str(img_name) + ".jpg", masked_reg) #FOR DEBUGGING PURPOSE
                    cv2.imwrite(MASK_OUTPUT_PATH + "mask_" + str(img_name) + ".jpg", filled_mask)
                    # COUNT = img_name
                    if  img_name == COUNT + BREAK_LIMIT: 
                        write_file(COUNTER_FILE, img_name)
                        print("Exited at " + str(img_name))
                        cv2.destroyAllWindows()
                        # sys.exit(1)
                    cv2.destroyAllWindows()
                    break
                else:
                    cv2.destroyAllWindows()
                    continue

        
            except Exception as e:
                print(str(e) + "\nTrying again...")
                OCCURENCES += 1
                cv2.destroyAllWindows()
                continue
                if OCCURENCES > 25:
                    cv2.destroyAllWindows()
                    break

 
if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()
