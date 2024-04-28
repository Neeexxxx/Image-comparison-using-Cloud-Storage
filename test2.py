# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage
from clean_algorithms import clean_SSIM 
from clean_algorithms import clean_ORB 
from clean_algorithms import clean_pHash 
from string_hextobin import hexStr_to_binStr
from get_similarity_float import get_similarity

import os
# import numpy as np
# import cv2

# cred = credentials.Certificate('newAccessKey.json')
# app = firebase_admin.initialize_app(cred,{'storageBucket':'exceedcloudsystem.appspot.com'})

# bucket=storage.bucket()
# blob=bucket.blob("car0_0.jpg")
# blob.download_to_filename("testImageForSsimAndOrb.jpg")

#testing SSIM
try:
    testval = clean_SSIM("test image set A\cars1.jpg","test image set B\car0.jpg")
except:
    print("starting the comparison")
#testing done


testA = {"test image set A\cars1.jpg":"1110010010110010",
         "test image set A\cars2.jpg":"1110100110100010"}

compareB={"test image set B\car0.jpg":"1110110101000001",
          "test image set B\car1.jpg":"1010110110101000",
          "test image set B\car2.jpg":"1010110110011000"}

maxval_phash,maxval_ssim,maxval_orb=-1,-1,-1
maxvalID_phash,maxvalID_ssim,maxvalID_orb="","",""
maxval_phash_list,maxval_ssim_list,maxval_orb_list=[],[],[]

threshold=int(input("threshold value for SSIM/ORB : "))
for image_test in testA.keys():
    current_pHash = testA[image_test]
    for image_compare in compareB.keys():
        compare_phash = compareB[image_compare]
        phash_similarity = float(get_similarity(current_pHash,compare_phash))
        
        if(phash_similarity>=maxval_phash):
            maxval_phash=phash_similarity
            maxvalID_phash=image_compare
            
        
        if(phash_similarity>threshold):
            ssim_similarity = float(clean_SSIM(image_test,image_compare))
            orb_similarity = float(clean_ORB(image_test,image_compare))
            
            if(ssim_similarity>=maxval_ssim):
                maxval_ssim=ssim_similarity
                maxvalID_ssim=image_compare
                
            if(orb_similarity>=maxval_orb):
                maxval_orb=orb_similarity
                maxvalID_orb=image_compare
            
            
    maxval_phash_list.append({image_test:[maxvalID_phash,maxval_phash]})
    maxval_ssim_list.append({image_test:[maxvalID_ssim,maxval_ssim]})
    maxval_orb_list.append({image_test:[maxvalID_orb,maxval_orb]})

print("\n************************************************\n")    
print("printing most similar images as per pHash : ")
for element in maxval_phash_list:
    print(element)
print("\n************************************************\n")
print("printing most similar images as per SSIM : ")
for element in maxval_ssim_list:
    print(element)
print("\n************************************************\n")    
print("printing most similar images as per ORB : ")
for element in maxval_orb_list:
    print(element)
            
        
# print("pHash -- ",image_test," : ",image_compare," - > ",phash_similarity)
# print("SSIM -- ",image_test," : ",image_compare," - > ",ssim_similarity)
# print("ORB -- ",image_test," : ",image_compare," - > ",orb_similarity)
        
    