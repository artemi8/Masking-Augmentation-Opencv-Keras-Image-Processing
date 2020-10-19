"""
Augmentation Operations:
1. Affine Transformation with rotation and shearing
2. Coarse Dropout
3. Guassian Noise only for image
"""

import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm

IMG_PATH = "dataset/images/leafs/"		# Path to the dataset directory
MASK_PATH = "dataset/masks/masks/"		# Path to mask dataset directory
OUTPUT_IMAGE_PATH = "augmented/images/"		# Path to write the augmented images
OUTPUT_MASK_PATH = "augmented/masks/"		# Path to write the augmented mask images
AUG_NUM = 4  					# Number of augmentation to be done per image
TOTAL_IMGS = 2 					# Total images in the directory, will be helpful for tqdm to track the progress
i = 0 						# For naming the output images
paths1 = Path(IMG_PATH).glob("**/*.jpg")	# Generator to iterate through the directory of the dataset
paths2 = Path(MASK_PATH).glob("**/*.jpg")

for (img_path, segmap_path) in tqdm(zip(paths1, paths2), total = TOTAL_IMGS,desc = "Augmenting"):

	image = cv2.imread(str(img_path))
	segmap = cv2.imread(str(segmap_path))
	segmap = np.asarray(segmap)
	image = np.asarray(image)

	# Augmentation pipeline for images
	aug_images = iaa.Sequential([
    	iaa.Affine(rotate=(-20, 20),
    		shear=(-16, 16),
    		mode= "reflect", random_state=1),
    	iaa.CoarseDropout(0.2, size_percent=0.05, random_state=2),
    	iaa.AdditiveGaussianNoise(scale=0.2*255, random_state=3)
	], random_state=4)

	# Augmentation pipeline for segmentation masks
	aug_segmaps = iaa.Sequential([
    	iaa.Affine(rotate=(-20, 20),
    		shear=(-16, 16),
    		mode= "reflect", random_state=1),
    	iaa.CoarseDropout(0.2, size_percent=0.05, random_state=2)
	], random_state=4)

	#Applying AUG_NUM number of augmentation per image.
	for j in range(AUG_NUM):
		# Applying Image Augmentation Pipeline
		image_aug = aug_images(image=image)

		# Applying Mask Augmentation Pipeline
		segmap_aug = aug_segmaps(image=segmap)

		# Writing images to local directory
		cv2.imwrite(OUTPUT_IMAGE_PATH + "img_aug_" + str(i) + "_" +str(j)+ ".png", image_aug)
		cv2.imwrite(OUTPUT_MASK_PATH + "seg_aug_" + str(i) + "_" +str(j)+ ".png", segmap_aug)
	i += 1
