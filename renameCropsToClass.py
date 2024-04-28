import os
def rename():
    # Function to rename multiple files
    classes=os.listdir("runs\detect\exp\crops")
    for folder in classes:
        path="runs\detect\exp\crops"+"\\"+folder
        # print(path)
        for filecount, filename in enumerate(os.listdir(path)):
            dst = folder+str(filecount)+".jpg"
            src =f"{path}/{filename}" # foldername/filename, if .py file is outside folder
            dst =f"{path}/{dst}"
            # rename() function will
            # rename all the files
            os.rename(src, dst)
    # print("success")
