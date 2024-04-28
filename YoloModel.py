import torch
from PIL import Image
import os
import pandas

def LoadYoloModelAndCrop():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5x',force_reload=True)
    model.conf=0.5
    im = Image.open("testImage.jpg")
    results = model(im)
    crops = results.crop(save=True)
# LoadYoloModelAndCrop()