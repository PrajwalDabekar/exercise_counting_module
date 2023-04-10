from flask import Flask,render_template,Response
import cv2
# import numpy as np
import mediapipe as md
#from database import attendance


app = Flask(__name__)
cap = cv2.VideoCapture(0)
start_frame_number = 300   #No. of frames to be skipped
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)  #for skipping the frames


# md_drawing = md.solutions.drawing_utils
# md_drawing_styles = md.solutions.drawing_styles
# md_pose = md.solutions.pose
# pose = md_pose.Pose()
global count 
global position

mpPose = md.solutions.pose
pose = mpPose.Pose()
mpDraw = md.solutions.drawing_utils






@app.route("/")
def home ():
    return render_template("index.html")

def getframe():
    count = None
    position = None
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    imlist = []
    # print("im here")
    if results.pose_landmarks:
        # print("i m also here")
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id, im in enumerate(results.pose_landmarks.landmark):
            h,w,_ = img.shape
            X,Y = int(im.x*w),int(im.y*h)
            imlist.append([id,X,Y])
    
        # print(imlist)
    # if results.pose_landmarks:
    #     md_drawing.draw_landmarks(img,results.pose_landmarks,md_pose.POSE_CONNECTIONS)
    #     for id,im in enumerate(results.pose_landmarks.landmark):
            
    if len(imlist) != 0:
        if (imlist[16][2] and imlist[15][2] >= imlist[14][2] and imlist[13][2]):
            position = "down"
            print(position)
        if (imlist[16][2] and imlist[15][2] <= imlist[14][2] and imlist[13][2]):
            position = "up"
            print(position)
            count +=1
            
            
            print(count)
        cv2.putText(img,str(count),(100,100),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2,cv2.LINE_AA)

    ret, jpeg = cv2.imencode('.jpg', img)
    cv2.waitKey(3)
    return jpeg.tobytes()


def gen(cap):
    while True:
        #print("im here")
        frame = getframe()
        yield (b'--frame\r\n'b'Content-Type: video/mp4\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/videofeed")
def videofeed():
    
    global cap
    return Response(gen(cap),mimetype='multipart/x-mixed-replace; boundary=frame'),render_template("/video.html")

if __name__ == '__main__':
    app.run(debug=True)