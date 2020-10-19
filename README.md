# Masking-Augmentation-Opencv-Keras-Image-Processing
Mask creation for segmentation tasks and Image augmentation pipeline with imaug and Keras's ImageDataGenerator

## masking_op.py
This program helps the user to create custom segmentation maps

### File variables
#### These variables shall be changed upon convenience of the user.

1. BREAK_LIMIT - Program exits after defined number of images for convenience of the user as it runs for loop for the images in that range. Default is 10.
2. DATASET_PATH = Path to the Dataset
3. MASK_OUTPUT_PATH = Path to save the created mask
3. MASK_INV = Path to save the color image mask

## Prerequisite
1. Opencv package - cv2
2. Numpy package - numpy
### Make sure you have created directories to save the mask and mask_inv and "dataset" folder must contain images with name as numbers starting from 1,2,3...

## Keys used while sketching the mask:
1. r     - Mask the image
2. SPACE - Reset the inpainting mask
3. ESC   - Skip current image
4. z     - Exit program

## Program Flow
Make sure that you satisfied the Prerequisite

1. Images from the dataset folder will start appearing one at a time.
2. Select the region to mask using mouse.
3. Press "r" if the free hand marking is appropriate.
4. Press "space" to reset the image or ESC to skip the current image or Z to exit the program.
5. After pressing "r" your masked region will be displayed in color to check the correctness of your masking.
6. Press "y" if satisfied and this will write the mask image to the specified directory.
7. Press any other button to redo the masking process.

Exception Handling is in place for a MouseCallbackError which exists in pip installation of opencv but fixed in apt installed opencv, still not sure why it exists. If you haven't installed opencv yet then i would advise to install using this command for ubuntu users "sudo apt install libopencv-dev python3-opencv"
It's okay if you have pip installed version that's why the exception handling is in place. 
Happy Masking!

## imgaug_augmentation.py

### Augmentation program using imgaug library.
1. IMG_PATH           - Path to the dataset directory of images
2. MASK_PATH          - Path to the dataset of masks of the images
3. OUTPUT_IMAGE_PATH  - Path to write the augmented images
4. OUTPUT_MASK_PATH   - Path to write the augmented mask images
5. AUG_NUM            - Number of augmentation to be done per image
6. TOTAL_IMGS         - Total images in the directory, will be helpful for tqdm to track the progress
7. paths1 and paths2 image extension must as you have in your dataset for example ".jpg" or ".png".

### Augmentation Operations Performed:
1. Affine Transformation with rotation and shearing
2. Coarse Dropout
3. Guassian Noise only for image

imgaug library has much more heavy augmentation operations and more sophiticated functions for various necessities.[imguag documentation](https://imgaug.readthedocs.io/en/latest/index.html)



