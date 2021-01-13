from tensorflow.keras.models import load_model                    # TO LOAD THE OUR MODEL
from tensorflow.keras.preprocessing.image import img_to_array     # TO CONVERT IMAGE TO NUMPY ARRAY
import cv2                                                        # FOR FACE DETECTION
import numpy as np                                                # TO HANDLE IMAGE MATRICES
# from audio import speak                                         # TO WARN PEOPLE THROUGH SPEECH
import os
# from mail import MailAlert                                       # violation mail will be transfered to admin
from sound import SoundAlert

model1 = load_model('./models/mask_detection_model_vgg16.h5')      # TRAINED MASK DETECTION MODEL
model2= load_model('./models/face_recognition_model_vgg16.h5')      # TRAINED FACE RECOGNITION MODEL

# GET LIST OF FACES NAMES THAT ARE TRAINED
names=os.listdir('./Image_Dataset/train')
mask_options={0:'MASK',1:'NO_MASK'}

# PRETRAINED FACE DETECTION MODEL
face_detector=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

# STARTING THE WEBCAM
cap=cv2.VideoCapture(0)

# INITIALIZE THE MAIL CLASS
# mail=MailAlert()

# INITIALIZE THE SOUND CLASS
sound=SoundAlert()


# MASK DETECTION AND FACE RECOGNITION
def mask_and_face_recognition():

    while True:
        res, frame = cap.read()                                    # CAPTURING THE FRAMES FROM VIDEO

        try:
            if res==False:                                         # If no frame is captured, come out of loop
                raise NoFrameException
                break
        except NoFrameException:
            print('UNABLE TO CAPTURE THE FRAMES')

        gray_img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)             # CONVERTING INTO GRAYSCALE IMAGE
        face_images=face_detector.detectMultiScale(gray_img,1.3,5)  # DETETCTING FACES IN THE IMAGE

        for face in face_images:
            (x,y,w,h)=face                                           # EXTRACTING THE CO ORDINATES OF DETECTED FACES
            crop_face=frame[y:y+h+50,x:x+w+50]                       # EXTRACTING REGION OF INTEREST

            resize_face=cv2.resize(crop_face,(224,224))               # GENERALLY TRANSFER LEARNING TECHNIQUES TAKES INPUT AS (224,224)
            norm_face=img_to_array(resize_face)/255                   # NORMAILZED THE IMAGE
            detect_image=np.expand_dims(norm_face,axis=0)             # FOR MODEL WE NEED TO GIVE 4-D INPUT
            prob1=model1.predict(detect_image)                        # PREDICTION HAPPENS, RETURNS PROBABILISTIC PREDICTION
            prob2=model2.predict(detect_image)
            pred1 = np.argmax(prob1)                                  # TAKING THE INDEX WITH MORE PROBABILITY
            pred2= np.argmax(prob2)


            if pred1==0:

                # DRAW THE RECTANGLE AROUND THE FACE
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # WRITE THE SCENARIO IN THE IMAGE
                cv2.putText(frame, '{} with {} -- '.format(names[pred2], mask_options[pred1])+" %.2f"%(round(prob1[0][pred1],2)), (50, 50),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, '{} with {} -- '.format(names[pred2], mask_options[pred1])+" %.2f"%(round(prob1[0][pred1],2)), (50, 50),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                # speak('{} please wear the mask'.format(names[pred2]))
                # mail.mailAlert('MASK VIOLATION', "{} DIDN'T WORE THE MASK".format(names[pred2]))
                sound.sound_alert()

        cv2.imshow('Video',frame)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    mask_and_face_recognition()
