import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from clean_algorithms import clean_pHash 
from clean_algorithms import clean_SSIM 
from clean_algorithms import clean_ORB 
from get_similarity_float import get_similarity
from string_hextobin import hexStr_to_binStr
from YoloModel import LoadYoloModelAndCrop
from renameCropsToClass import rename
from delete_runs_folder import delete_crops

try:
    delete_crops()
except:
    print(" Ready to Execute ")
print("\n\n************************************************************")
print("\t\t\tStarting the system ...")
print("************************************************************\n")

print("Loading object detection model ...")
LoadYoloModelAndCrop()
print("Object detected & saved\n")
print("************************************************************\n")
print("Performing some pre-requisite tasks ... ")
rename()
print("Ready to proceed further\n")
print("************************************************************\n")
print("Accessing the cloud database ...")
cred = credentials.Certificate('newAccessKey.json')
app = firebase_admin.initialize_app(cred,{'storageBucket':'exceedcloudsystem.appspot.com'})
db = firestore.client()
bucket=storage.bucket()
print("Connection established !")
testval = clean_SSIM("testSSIM.jpg","testSSIM.jpg")
print("\n\n********************************************************\n")

maxval_phash,maxval_ssim,maxval_orb=-1,-1,-1
maxvalID_phash,maxvalID_ssim,maxvalID_orb="-","-","-"
maxval_phash_list,maxval_ssim_list,maxval_orb_list=[],[],[]

threshold=int(input("Set Threshold value for comparison (0-100): "))
try:
    os.remove("test_img_SSIMORB.jpg")
except:
    print("Computing similarity, please wait ...\n")
    

test_classes=os.listdir("runs\detect\exp\crops")
for Class in test_classes: #car
    
    path="runs\detect\exp\crops"+"\\"+Class #crops\car
    Crops = os.listdir(path) #car1, car2 ...
    
    for test_image in Crops:
        
        test_image_path=os.path.join(path,test_image)
        test_image_hash = clean_pHash(test_image_path)
        test_image_hash = hexStr_to_binStr(test_image_hash)
        docs = db.collection(u'Training').stream()
        
        for doc in docs:
            obj=doc.to_dict()
            
            if(obj['imgID'].__contains__(Class)):
                print(obj['imgID'],"\t",Class)
                cloud_img_hash=obj['pHash']
                phash_similarity=float(get_similarity(cloud_img_hash,test_image_hash))
                
                if(phash_similarity>=maxval_phash):
                    maxval_phash=phash_similarity
                    maxvalID_phash=obj['imgID']
                    
                if(phash_similarity>threshold):
                    
                    blob=bucket.blob(maxvalID_phash)
                    blob.download_to_filename("test_img_SSIMORB.jpg")
                    image_test="test_img_SSIMORB.jpg"
                    ssim_similarity = float(clean_SSIM(image_test,test_image_path)*100)
                    orb_similarity = float(clean_ORB(image_test,test_image_path)*100)
                    
                    if(ssim_similarity>=maxval_ssim):
                        maxval_ssim=ssim_similarity
                        maxvalID_ssim=obj['imgID']
                        
                    if(orb_similarity>=maxval_orb):
                        maxval_orb=orb_similarity
                        maxvalID_orb=obj['imgID']
                        
                    os.remove("test_img_SSIMORB.jpg")
                
        maxval_phash_list.append({test_image:[maxvalID_phash,maxval_phash]})
        maxval_ssim_list.append({test_image:[maxvalID_ssim,maxval_ssim]})
        maxval_orb_list.append({test_image:[maxvalID_orb,maxval_orb]})
        
        maxval_phash,maxval_ssim,maxval_orb=-1,-1,-1
        maxvalID_phash,maxvalID_ssim,maxvalID_orb="-","-","-"
        
print("All images compared ... ")  
print("\n\t\tHere's what the algorithm thinks\n")  
print("\n************************************************\n")    
print("printing most similar images as per pHash : \n")
print("Test_Image_ID\t\tMost_Similar_Image_ID\t\tPercentage")
for element in maxval_phash_list:
    temp1=list(element.keys())
    print(temp1[0],end="\t\t")
    temp2=list(element.values())
    temp2=temp2[0]
    print(temp2[0],"\t\t",temp2[1])
print("\n************************************************\n")
print("printing most similar images as per SSIM : \n")
print("Test_Image_ID\t\tMost_Similar_Image_ID\t\tPercentage")
for element in maxval_ssim_list:
    temp1=list(element.keys())
    print(temp1[0],end="\t\t")
    temp2=list(element.values())
    temp2=temp2[0]
    print(temp2[0],"\t\t",temp2[1])
print("\n************************************************\n")    
print("printing most similar images as per ORB : \n")
print("Test_Image_ID\t\tMost_Similar_Image_ID\t\tPercentage")
for element in maxval_orb_list:
    temp1=list(element.keys())
    print(temp1[0],end="\t\t")
    temp2=list(element.values())
    temp2=temp2[0]
    print(temp2[0],"\t\t",temp2[1])
print("\n************************************************\n") 
        

            
            