import cv2

cap = cv2.VideoCapture(0)
cv2.namedWindow('win')
myColors = [(84,124,0),(360,255,255)] #1st:lower range & 2nd:upper range 

myPoints=[] # at first we don't have any point 🤷🏻‍♂️ so its None!

# find cooridents of marker
def Contours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:

            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True) # find shape type of contour
            x, y, w, h = cv2.boundingRect(approx)  # set up a rectangle arounf contours
    return x,y


#draw on camera
def drawing(myPoints):
    for myp in myPoints:
        cv2.circle(imgResult, (myp[0],myp[1]), x , (255,128,0),-1)

#get Mask
def mask(img,myColors):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = [] # at first we don't have newpoint
    for color in myColors:
        lower = (84,124,0)  #if you cant draw . you should  change this value from HSV guides
        upper = (360,255,255)
        mask = cv2.inRange(imgHSV,lower,upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        x,y = Contours(mask)
        cv2.circle(imgResult,(x,y),10,(255,128,0),cv2.FILLED)
        if x !=0 and y !=0:
            newPoints.append([x,y,count])
        if lower == (71,168,142):
            cv2.circle(imgResult,(x,y),10,(71,168,142),-1)
        #cv2.imshow(str(color[0]),result)
    return newPoints
def none(x):
    print(x)
cv2.createTrackbar('x','win',1
,100,none)
while True:
    ret, img =cap.read()
    x=cv2.getTrackbarPos('x','win')
    imgResult = img.copy()
    newPoints = mask(img,myColors)
    if len(newPoints) !=0:
        # if we had any marker so you can draw
        for newP in newPoints:
            myPoints.append(newP) # to save the last paint
    else:
        cv2.putText(imgResult,'no marker found!',(50,60),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
     
    if len(myPoints) !=0:
        drawing(myPoints) 
        cv2.putText(imgResult,'a thing drawn',(50,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,140,0),2)
    else:
        cv2.putText(imgResult,'No painting',(50,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
    
    cv2.imshow("win", imgResult) # show Result
    if cv2.waitKey(1) & 0xFF == ord('q'):
    
        #press (q) to exit 
        break
    elif cv2.waitKey(1) & 0xFF==ord('c'):
        imgResult=img    