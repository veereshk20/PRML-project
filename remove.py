import cv2 as cv
import os
import stat


path = 'C:\\Users\\veere\\OneDrive\\Desktop\\PRML Project\\dataset\\side\\side'

i = 0

for file in os.listdir(path):
    file_path = os.path.join(path, file)
    
    img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
    
    if img is None:
        print(file_path)
        os.chmod(file_path, stat.S_IWRITE)
        os.remove(file_path)

    i+=1

    if (i%10000==0):
        print(i)





