import cv2
import numpy as np
import vehicles
import time

cnt_up=0
cnt_down=0


cap=cv2.VideoCapture("surveillance.m4v")

#Get width and height of video
w=cap.get(3)
h=cap.get(4)
# Frame Area
frameArea=h*w
areaTH=frameArea/400

#Lines
#position of the Red and Blue line on the input video frame
line_up=int(2*(h/5))
line_down=int(3*(h/5))

#region of interest
up_limit=int(1*(h/5))
down_limit=int(4*(h/5))

print("Red line y:",str(line_down))
print("Blue line y:",str(line_up))

line_down_color=(255,0,0) # Red color line
line_up_color=(255,0,255) # Blue color line

pt1 =  [0, line_down]
pt2 =  [w, line_down]
# type  = np.int32 [32 bit int]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))

pt3 =  [0, line_up]
pt4 =  [w, line_up]

pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]

pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))

pt7 =  [0, down_limit]
pt8 =  [w, down_limit]

pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))
'''
 Background Subtractor
 we are going to use Background subtraction method where we separate people and objects that move (the foreground)
 from the fixed environment( the background)
 lessen the effect of small repetitive motions like moving tress and bushes
 Background subtraction produces binary image : white where frame is changing i.e. moving object and black elsewhere
'''
#extracting foreground using cv2.createBackgroundSubtractorMOG2(detectShadows = True)
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True) # we are also detecting shadows

'''
 Kernals //  used for blurring of the original image
 Below is the good link for the explanation of kernels use
 https://github.com/atduskgreg/opencv-processing-book/blob/master/book/filters/blur.md
'''
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((11,11),np.uint)


font = cv2.FONT_HERSHEY_SIMPLEX
#creating a class Car object
cars = []
max_p_age = 5
pid = 1


while(cap.isOpened()):
    #Reading frame of the inputed image
    ret,frame=cap.read() # if return  = false  that means no more video frame to process
    for i in cars:
        i.age_one()
    fgmask=fgbg.apply(frame) # Apply background subtractor to get our foreground mask
    fgmask2=fgbg.apply(frame) # Apply background subtractor again to get foreground mask2

    if ret==True: # if code still getting input video frames
        '''
        Binarization
        If the pixel value is greateer than the threshold value , it is assigned one value, else it is assigned another value
        cv2.threshold(source image converted to grayscale , threshold value ,  value to be given if pixel value is more than threshold value)
        cv2.THRESH_BINARY convert the image to either one value or another value depending on threshold value of the pixel
        '''
        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2=cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
        '''
        morphological transformation
        two basic morphological operaators are Erosion and Dilation i.e. Opening and Closing
        Link for basic operation Theory
        https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        Erosion : A pixel in the orignial image (either 1 or 0 ) will be considered 1 only if all the pixels under the kernel is 1, otherwise
        it is eroded (made to zero)
        Dilation : Here, a pixel element is '1' if atleast one pixel under the kernel is '1'.
        so it increases the white region in the image of size of foreground object increases. usually used for noise removal
        erosion is followed by dilation
        '''


        #OPening i.e First Erode the dilate
        #useful in removing noise
        mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)
        mask2=cv2.morphologyEx(imBin2,cv2.MORPH_CLOSE,kernalOp)

        #Closing i.e First Dilate then Erode
        #useful in closing small holes in the foreground objects or small black points on the boject after threshold image conversion
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)
        mask2=cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernalCl)

        '''
        Code for Finding Contours
        cv2.CHAIN_APPROX_NONE will result in printing out all the data points of the Contours in our image
        cv2.RETR_EXTERNAL will give us external contours of the detected object
        '''
        countours0,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        #loops through the all the contours in the file and calculate area of  all the Contours in pixels
        for cnt in countours0:
            area=cv2.contourArea(cnt) # finding the area bounded by given contour : cnt
            print(area)
            if area>areaTH:

                ''' T    R    A     C    K     I    N    G
                cv2.moments is used to find the centroid of the contour i.e. our detected vehicles
                '''
                m=cv2.moments(cnt)
                #Centroid
                cx=int(m['m10']/m['m00']) # x coordinate of the centroid of the detected vehicle
                cy=int(m['m01']/m['m00']) # y coorddinate of the centroid of the detected vehicle
                '''The cv2.boundingRect() function of OpenCV is used to draw an approximate rectabgle around the binary image.
                This function is used mainly to higlight the region of interest after obtaining contours from an image.
                '''
                x,y,w,h=cv2.boundingRect(cnt) # gives rectangular overlay of contour cnt
                # x and y are starting point of the bounding rectangle and w and h are width and height respectively

                new=True


                # if the y value of the centroid is between up_limit  and down_limit range start the for loop on cars
                if cy in range(up_limit,down_limit):
                    for i in cars:
                        #checking if bounding rectangle for the detected object is in the frame or not
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)

                            if i.going_UP(line_down,line_up)==True: # if car is going up the way
                                cnt_up+=1 # up going cars counter
                                #print("ID:",i.getId(),'crossed going up at', time.strftime("%c"))
                            elif i.going_DOWN(line_down,line_up)==True: # if car is going down the way
                                cnt_down+=1 # down going  cars counter
                                #print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                            break
                        #getting  state of the current car
                        if i.getState()=='1':

                            #if direction is dodwn and y coordinate of the car > down limit // car centre coordinate is out of the ROI set DONE = TRUE
                            if i.getDir()=='down'and i.getY()>down_limit:
                                i.setDone() # setting done = true
                            # if direction is up and y coordinate of the car <up_limit // car centree coordinate is out of the ROI set DONE = TRUE
                            elif i.getDir()=='up'and i.getY()<up_limit:
                                i.setDone()#setting done = true
                        if i.timedOut(): # if done = true
                            #index=cars.index(i)
                            cars.pop(cars.index(i)) # removing the car from the cars list
                            del i # deleting the car // element

                    if new==True: #If nothing is detected,create new
                        #creating new car object fro class Car
                        p=vehicles.Car(pid,cx,cy,max_p_age)
                        cars.append(p) # appending new car to cars [] list
                        pid+=1

                #placing Centroid at the centre of the contour rectangle
                # cv2.circle(img, center , radius, color , thickness, optional :: [lineType = ?, shift = ?])
                cv2.circle(frame,(cx,cy),5,(231,219,0),-1) # -1 for completely filling the centroid circle
                #Drawing bounding rectangle around the detected car
                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        # just for testing purpose // remove it later        
        for i in cars:
            #cv2.putText(img, text, (x,y), fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)




        str_up='UP: '+str(cnt_up) # string to be displayed on the output screen "UP : cnt_up"
        str_down='DOWN: '+str(cnt_down) # string to be displayed on the oupput screen "DOWN :  cnt_down"
        '''
        draw several polygon curves
        cv2.polylines(img, pts, isClosed, color[, thickness[, lineType[, shift]]])
        cv.PolyLine(img, polys, is_closed, color, thickness=1, lineType=8, shift=0
        '''
        frame=cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        frame=cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        '''
        putting text on the output real time video stream at (x,y) coordinate location on the Frames
        cv2.putText(img, text, (x,y), fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        '''
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA) # white color line
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA) # red color line
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA) # white color line
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) # blue color line
        #playing the Processed Video Stream as a output until the loop breaks
        cv2.imshow('Processed Video Stream',frame)
        '''
        cv2.waitKey() returns a 32 Bit integer value (might be dependent on the platform). The key input is in ASCII which is an 8 Bit integer value.
        So you only care about these 8 bits and want all other bits to be 0. This you can achieve with:
         0xff is used to mask off the last 8 bit digits
        '''
        #quit the output streaming  after pressing 'q'
        if cv2.waitKey(1)&0xff==ord('q'):
            break

    else:
        break
# Releasing Video Frames
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()
