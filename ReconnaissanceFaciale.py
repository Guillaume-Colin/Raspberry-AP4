import cv2
import os
import time

"""
def reconnaissanceFaciale(identifiantAReconnaitre,path_dir):
    try:
        # Chargement du modèle d'entraînement
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')

        # Chargement du classificateur de visages
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Initialisation du flux vidéo
        cap = cv2.VideoCapture(0)

        # Initialisation des variables pour le renforcement de la confiance
        current_id = identifiantAReconnaitre
        confidence_threshold = 90
        confidence_counter = 0
        name = 'Inconnu'
        path = path_dir
        names = {}
        pasreconnu = True
        id=0

        for subdir in os.listdir(path):
            names[id]=subdir
            id+=1

        while pasreconnu:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            #if len(faces)>1:
            #    pasreconnu = False
            # Reconnaissance des visages détectés
            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(roi)
                if confidence < confidence_threshold:
                    name = "Personne {}".format(names[label])
                    print (name)
                    if current_id == names[label]:
                        confidence_counter += 1
                        print(confidence_counter+" -> Reconnu :"+names[label])
                        if confidence_counter >= 5:
                            pasreconnu = False
                else:
                    name = "Inconnu"
                    print (name)
                    
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,141,247), 2)
                cv2.putText(img, str(int(confidence))+"%", (x, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (88,181,247), 2)

            cv2.imshow('Reconnaissance de visages', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                pasreconnu = False

        cap.release()
        cv2.destroyAllWindows()
        return "OK"
    except Exception as e:
        print("Erreur", e)
        
#reconnaissanceFaciale('test','Images-visages')
"""        
        
import cv2,os,numpy, time

def reconnaissanceFaciale(identifiant, path_dir): #return true if the face correspond with the identifiant
    print("c'est parti")
    id=0
    size = 2
    path = path_dir
    time_start = time.time()
    fn_haar = "haarcascade_frontalface_default.xml"
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('leCoach.yml')
    haar_cascade = cv2.CascadeClassifier(fn_haar)
    cam = cv2.VideoCapture(0)
    pasreconnu=True
    vretour = False
    compteur=0
    identifiants={}
    (im_width, im_height) = (112, 92)

    for subdir in os.listdir(path):
        identifiants[id]=subdir
        id+=1
        
    j = 0
    cptpasreconnu = 0
    #while pasreconnu:
    while j<50:
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
            vretour = "Plusieurs visages détectés"
            
        if len(faces)<2:
            
            for i in range(len(faces)):
                face_i = faces[i]
                
                # Coordinates of face after scaling back by `size`
                (x, y, w, h) = [v * size for v in face_i]
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (im_width, im_height))

                prediction = recognizer.predict(face_resize)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (232, 1, 253), 2)
                
                if prediction[1]<90:
                    cv2.putText(frame, '%s' % (identifiants[prediction[0]]), (x+5,y-5), font, 1, (203,204,0), 2)
                    cv2.putText(frame, '%.0f' %  (prediction[1]), (x+5,y+h-5), font, 1, (0,255,0), 1)
                    if identifiants[prediction[0]]==identifiant:
                        compteur+=1
                        
                        if compteur >= 5:
                            print("c'est ok")
                            pasreconnu=False
                else:
                    cptpasreconnu += 1
                    cv2.putText(frame,'Inconnu',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 0, 255))
                    print("pas reconnu")
        
        time_current = time.time()
        cv2.imshow('OpenCV', frame)
        k = cv2.waitKey(10) & 0xff
        j += 1
    cam.release()
    cv2.destroyAllWindows()
    if compteur > cptpasreconnu:
        vretour =True
        print ("Validée")
    return vretour
def insertLog(numPhase,identifiant,numBadge,commentaire):
    insertLogAcces(numPhase,identifiant,numBadge,commentaire)       
#reconnaissanceFaciale('jeanne', 'Images-visages')