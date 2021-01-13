import cv2



face_detector=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')


cap=cv2.VideoCapture(0)
count=0



def face_extract(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_lens = face_detector.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)

    if len(face_lens)==0:
        return None

    for (x, y, w, h) in face_lens:
        x,y = (x - 10, y - 10)
        face = frame[y:y + h + 50, x:x + w + 50]

    return face


while True:
    res, frame = cap.read()
    if face_extract(frame) is None:
        print('face not found')
        pass
    else:
        count=count+1
        face=cv2.resize(face_extract(frame),(400,400))

        file_path='./Images/test/'+str(count)+'.jpg'
        cv2.imwrite(file_path,face)

        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('face',face)

    if cv2.waitKey(1)==13 or count==100:
        break

cap.release()
cv2.destroyAllWindows()
print("Done")
