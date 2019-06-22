#detecting pedestrians in inputed video using OpenCV and HaarCascades using
#pretrainted Haar Cascades classifier for car detection
import cv2
import numpy as np

#creating classifier object people for pedestrian
#using pre-exisiting  HaarCascades classifier for pedestrian classification
people_classifier  = cv2.CascadeClassifier('haarcascade_fullbody.xml')
#Initiate video capture for inputed video fiile
#using the most famous walking sample for OPENCV out there
cap  = cv2.VideoCapture('image/pedestrians.avi')
#loop  starts when video is successfuly loaded
#infinte loop breaks at the end of the video contiion is true
while True:
    #reading first frame
    ret , frame = cap.read()

    #if input is null that is variable gray is empty  usually occurs at the end of the video input so we add foloowing line of code to prevent that from happening
    #end of the video condition
    if(type(frame) == type(None)):
        break
    #Now we are going to decrease the resolution of the frame to fast up the
    #calculation process // INTER_LINEAR  is quicker interpolation method
    #frame = cv2.resize(frame , None , fx =0.5 , fy =0.5 , interpolation = cv2.INTER_LINEAR)
    #Converting the given frame to grayscale using openCV cvtColor method
    gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #passing frames to our people classifiers
    #(gray,value,3) larger value makes the detection faster but beware because it will produce some false positive too
    #but these parameter works brilliantly with our given sample video of walking pedestrians
    person = people_classifier.detectMultiScale(gray, 1.4 , 1)
    #ploting the above people point array
    #Extract bounding boxes for any person identified
    for (x,y,w,h) in person :
        #making a rectangle frame around the detected person
        #using different colors than car_detection.py code
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        #displaying the Pedestrians with bounded rectangles
    cv2.imshow('Pedestrians detection',frame)
    if cv2.waitKey(33) ==27 : # 27 is the escape key to stop and 33 is dealy time in ms
        break
#release the video object
cap.release()
#perfoming cleanups
cv2.destroyAllWindows()
