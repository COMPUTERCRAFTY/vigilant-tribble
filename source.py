import cv2
import time
import numpy as np

#To save the output in a file known as output.avi
fourcc = cv2.cv.CV_FOURCC(*'XVID')
output_file=VideoWriter('output.avi',fourcc,20.0,(640,480))

#Starting the webcam
cap=cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for a bit
time.sleep(2)
bg=0

# CApturing Background for 60 frames
for i in range(60):
    ret,bg=cap.read()
#Flipping background
bg=np.flip(bg,axis=1)

#Reading every frame until camera is open
while cap.isOpen():
    ret,img=cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img=np.flip(img,axis=1)
    #Converting the color from BGR to HSV
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #generating the mask to detect red color(Values can be changed)
    lower_red=np.array([0,120,50])
    upper_red=np.array(10,255,255)
    mask1=cv2.inRange(hsv,lower_red,upper_red)
    lower_red=np.array([170,120,70])
    upper_red=np.array(180,255,255)
    mask2=cv2.inRange(hsv,lower_red,upper_red)
    mask1=mask1+mask2
    #Open and Expand the image where ther is mask 1
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    #Selecting only the part that does not contain the mask1 and saving it in mask2
    mask2=cv2.bitwise_not(mask1)
    #Keeping only the images without red color
    result1=cv2.bitwise_and(img,img,mask=mask2)
    result2=cv2.bitwise_and(img,img,mask=mask1)
    #generating final output by merging result1 and 2
    final_output=cv2.addWeighted(result1,1,result2,1,0)
    output_file.write(final_output)
    #displaying the output to the user
    cv2.imshow('Image',final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()