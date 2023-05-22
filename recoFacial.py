import cv2
import os
import numpy
import time
from logAcces import insertLogAcces

def ReconnaissanceFacial(identifiant, id, path_dir): #return true if the face correspond with the identifiant, else false
    print("allons-y")
    identite=0
    size = 2
    path = path_dir
    time_start = time.time()
    fn_haar = "/home/piwadoux/haarcascade_frontalface_default.xml"
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/piwadoux/work/trainer.yml')
    haar_cascade = cv2.CascadeClassifier(fn_haar)
    cam = cv2.VideoCapture(0)
    pasreconnu=True
    retour=False
    compteur=0
    identifiants={}
    (im_width, im_height) = (112, 92)

    

    for subdir in os.listdir(path):
        identifiants[identite]=subdir
        identite+=1
        
    while pasreconnu:
        ret, frame = cam.read()
        # Flip the image (optional)
        frame=cv2.flip(frame,1,0)
        # Convert to grayscalel
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize to speed up detection (optinal, change size above)
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        # Detect faces and loop through each one
        faces = haar_cascade.detectMultiScale(mini)
        
        if len(faces)>1:
            insertLog('3',identifiant,str(id),'Plusieur visage detécté')
            print('Insertion validé')
            pasreconnu=False
            
        for i in range(len(faces)):
            face_i = faces[i]
            
            # Coordinates of face after scaling back by `size`
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (im_width, im_height))

            prediction = recognizer.predict(face_resize)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (232, 1, 253), 2)
            
            # Try to recognize the face

            # [1]
            # Write the identifiant of recognized face
            #cv2.putText(frame,'%s - %.0f' % (identifiants[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
            if prediction[1]<90:
                cv2.putText(frame, '%s' % (identifiants[prediction[0]]), (x+5,y-5), font, 1, (203,204,0), 2)
                cv2.putText(frame, '%.0f' %  (prediction[1]), (x+5,y+h-5), font, 1, (0,255,0), 1)                #print(prediction[1])
                #cv2.putText(frame,'%s - %.0f' % (identifiants[prediction[0]]),(x-10, y-10), font,1,(0, 255, 0))
                #cv2.putText(frame, '%s-%.0f'% (identifiants[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                #print('%s - %.0f' % (identifiants[prediction[0]],prediction[1]))
                if identifiants[prediction[0]]==identifiant:
                    if compteur<5:
                        print (compteur, identifiant)
                        compteur+=1
                    else:
                        retour=True
                        print("C'est bon")
                        pasreconnu=False
            else:
                cv2.putText(frame,'not recognized',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 0, 255))

                    
        time_current = time.time()
        if (time_current - time_start) > 60:
            pasreconnu = False
            insertLog('3',identifiant,str(id),'Temps dépassé, aucune personne reconnu')
            print('Insertion validé')
        # Show the image and check for ESC being pressed
        cv2.imshow('OpenCV', frame)
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    cam.release()
    cv2.destroyAllWindows()
    return retour

def insertLog(numPhase,identifiant,numBadge,commentaire):
    insertLogAcces(numPhase,identifiant,numBadge,commentaire)
    
    
    