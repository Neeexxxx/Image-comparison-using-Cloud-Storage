from skimage.metrics import structural_similarity as SSIM
from skimage.transform import resize
from PIL import Image
from io import BytesIO
import imagehash
import cv2
import requests

def clean_ORB(image1_URL, image2_URL):
    orb = cv2.ORB_create()
    img1 = cv2.imread(image1_URL, 0)  #Ref img 1
    img2 = cv2.imread(image2_URL, 0)  #Ref img 2
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc_a, desc_b)
    bounds=80
    similar_regions = [i for i in matches if i.distance < bounds]  
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)

def clean_SSIM(image1_URL, image2_URL):

    #In case of accessing network images
    # response = requests.get(image1_URL)
    # img1 = Image.open(BytesIO(response.content))
    # response = requests.get(image2_URL)
    # img2 = Image.open(BytesIO(response.content))

    img1 = cv2.imread(image1_URL, 0)  #Ref img 1
    img2 = cv2.imread(image2_URL, 0)  #Ref img 2   
    img2 = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
    dRange = img1.dtype
    sim, diff = SSIM(img1, img2, full=True,)
    return sim

def clean_pHash(img_URL):
    SizeOfHash=4
    # SizeOfHash=int(input("How sensitive you want the pHash to be : (2^x)"))
    SizeOfHash=2**SizeOfHash
    hash=imagehash.phash(image=Image.open(img_URL), hash_size=SizeOfHash)
    return str(hash)

