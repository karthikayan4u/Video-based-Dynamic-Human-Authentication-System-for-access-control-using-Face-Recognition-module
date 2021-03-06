import face_recognition
import cv2
import numpy as np
from PIL import Image
import easygui
import re 
import datetime
import csv
import io

try:
    video_capture = cv2.VideoCapture(0)
except:
    video_capture = cv2.VideoCapture(1)

import os 
from array import array 
known_face_encodings = []
known_face_names = []
w="Your file directory"
p=os.listdir(w)
for j in p:
    if('.' not in j):
        a="Your file directory"+j
        b=os.listdir(a)
        for i in b:
            if i[-1] == 'y' :
                img_enc = np.load(os.path.join(a,i))
                if img_enc!=[]:
                    known_face_encodings.append(img_enc)
                    known_face_names.append(i[:-4])
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
guest_id = 0

while True:
    # Grab a single frame of video
    z=[];fac=[]
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    #print(rgb_small_frame)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)#,number_of_times_to_upsample=1,model='cnn')
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in range(len(face_encodings)):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encodings[face_encoding],tolerance=0.5)
            name = "unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encodings[face_encoding])
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
            
                name = known_face_names[best_match_index]
                
            if name=='unknown' : 
                z.append(face_encodings[face_encoding])
                fac.append(face_locations[face_encoding])            
                    
                    
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        ree = re.findall(r'[a-z]+',name)
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, ree[0], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if(ree[0] in p):
            mylist=[]
            x = datetime.datetime.now()
            mylist.append(x.strftime("%x"))
            mylist.append(x.strftime("%A"))
            mylist.append(x.strftime("%X"))
            a="Your file directory"+ree[0]
            b=os.listdir(a)
            for i in b:
                if i[-1] == 'v' :
                    with open(os.path.join(w+ree[0], ree[0]+'.csv'), "a") as csvfile: 
                        # creating a csv writer object 
                        csvwriter = csv.writer(csvfile) 
                        # writing the data rows 
                        csvwriter.writerow(mylist)
                        csvfile.close()

    for i in range(len(fac)) :
        if face_names[i] == 'unknown' :
            t,r,b,l = fac[i]
            face_image = rgb_small_frame[t:b,l:r]
            pil_image = Image.fromarray(face_image)
            img_enc=face_recognition.face_encodings(face_image)
            pil_image=pil_image.resize((700,700),Image.ANTIALIAS)
            j='guest.jpeg'
            pil_image.save("Your file directory"+j)
            if(img_enc!=[]):                   
                msg = "Do you know The Person ?"
                choices = ["Yes","No"]
                reply = easygui.buttonbox(msg, image=j, choices=choices)
                if reply =='Yes':
                    string=easygui.enterbox('Enter the Name Of Person')
                    if string  :
                        known_face_names.append(string)
                        pil_image=pil_image.resize((4000,4000),Image.ANTIALIAS)
                        if(string in p): 
                            mylist=[]
                            x = datetime.datetime.now()
                            mylist.append(x.strftime("%x"))
                            mylist.append(x.strftime("%A"))
                            mylist.append(x.strftime("%X"))
                            a="Your file directory"+string
                            b=os.listdir(a)
                            q=(len(b)-1)//2
                            img_enc=img_enc[0]
                            encodedfile = np.save(("Your file directory"+string+'/'+string+str(q)+ '.npy'), img_enc[0])
                            pil_image.save("Your file directory"+string+'/'+string+str(q)+'.jpeg')
                            for i in b:
                                if i[-1] == 'v' :
                                    with open(os.path.join(w+string, string+'.csv'), "a") as csvfile: 
                                        # creating a csv writer object 
                                        csvwriter = csv.writer(csvfile) 
                                        # writing the data rows 
                                        csvwriter.writerow(mylist)
                                        csvfile.close()


                        else:
                            os.mkdir("Your file directory"+string)
                            mylist=[]
                            fields = ['Date', 'Weekday', 'Time'] 
                            x = datetime.datetime.now()
                            mylist.append(x.strftime("%x"))
                            mylist.append(x.strftime("%A"))
                            mylist.append(x.strftime("%X"))
                            pil_image.save("Your file directory"+string+'/'+string+'.jpeg') 
                            with open(os.path.join(w+string, string+'.csv'), "w") as f:
                                  csvfile=io.StringIO()
                                  csvwriter=csv.writer(csvfile)
                                  csvwriter.writerow(fields)
                                  csvwriter.writerow(mylist)
                                  for a in csvfile.getvalue():
                                    f.writelines(a)
                                  f.close()
                            encodedfile = np.save(("Your file directory"+string+'/'+string+ ".npy"), img_enc[0])
                        p.append(string)

                        known_face_encodings+=z
            os.remove("Your file directory"+j) 

        else:
            pass

            
    frame = cv2.resize(frame,(1500,800))
                    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
