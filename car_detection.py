
#Detecting cars in inputed video using OpenCV and Haar Cascades
# using pretrained Haar Cascades classifier for car detection
import cv2
#source of the cascade from vehicle_detection_haarcascades directory
cascade_src = 'vehicle_detection_haarcascades/cars.xml'
#video source
video_src = 'image/video.avi'
# perfoming video capture
cap = cv2.VideoCapture(video_src)
#creating object for CascadeClassifier class which takes cascade_src as argument
car_cascade_ = cv2.CascadeClassifier(cascade_src)

#creating infinite loop which read the video frame by frame
while True :
    #reading frame by frame
    ret, frame = cap.read()
    #if statement for end video condition
    if(type(frame) ==type(None)):
        break
    #converting our BGR aka RGB image into gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #using detec multiscale command
    #second argument 1.1 is scaling factor i.e. resize to increase the operation speed
    #last argument is minimum numbers of neigbours to retain the detection rectangle window
    #Higher value of min neighbours means that number of detection will be low but quality of detection will increase
    cars = car_cascade_.detectMultiScale(gray , 1.4, 1)

    #printing rectanlge around detected object
    for(x,y,w,h) in cars :
        #(x,y) are the lower x and y values for the bouding rectangle
        #(x+w ,y+h) are the top left and top right value for the bounding rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    #displaying the detection
    cv2.imshow('car_detection',frame)
    if cv2.waitKey(33) ==27: # 27 is the escape key to stop and 33 is dealy time in ms
        break
#releasing the cap object
cap.release()
#performing cleanups
cv2.destroyAllWindows()
