import cv2, time,pandas
from datetime import datetime
video=cv2.VideoCapture(0)
df=pandas.DataFrame(columns=["Start","End"])
#a=1
first_frame=None
status_list=[None,None]
times=[]
while True:
    #a=a+1
    check, frame= video.read() #check is a boolean variable to check if the camera is running
    #, frame is the numpy array representing the first image the camera captured
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #time.sleep(3) #keep the prgram wait for 3 sec
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)
    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) <10000:
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    status_list.append(status)
    status_list=status_list[-2:] #avoid big memory
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Capturing",gray)
    cv2.imshow("dealta_frame",delta_frame)
    cv2.imshow("TreshHold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)
    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    print(status)
print(status_list)
print(times)
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv("Times.csv")

#print(a)
video.release()
cv2.destroyAllWindows()
