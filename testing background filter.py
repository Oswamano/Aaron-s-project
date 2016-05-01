import numpy as np
import cv2
import os
import smtplib, os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys
import time

def GetImage():
 # read is the easiest way to get a full image out of a VideoCapture object.
   retval, im = cap.read()
   return im
   
filepath = "C:/Users/aaron/Projects/python/doorman/"
index = 0;
#constants:
COMMASPACE = ', '
gmail_user = "6780frontdoor@gmail.com"
gmail_pwd = "amp.Amp827"

#variables:
msgText = "You have a visitor!"
#recipients = ['7164356580@mms.att.net'] # my cell phone number
recipients = ['ENTER YOUR EMAIL OR PHONE EMAIL HERE'] # my cell phone number

time.sleep(5)
print "starting motion detection"
cap = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG()

while(True):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)  
    currentImage1 = GetImage()
    cv2.imwrite(filepath + 'frame.png', currentImage1)

    if np.average(fgmask)>.5:
    # Attempting to send the image
        currentImage = GetImage();
        #if(motion detected)
        cv2.imwrite(filepath + 'lastImage.jpg', currentImage)
        print "intruder found!"
        # Attempting to send the image
        time.sleep(.2)
        currentImage2 = GetImage();
        time.sleep(.2)
        currentImage3 = GetImage();
        time.sleep(.2)
        currentImage4 = GetImage();
        time.sleep(.2)
        currentImage5 = GetImage();
        img1avg = np.average(fgbg.apply(currentImage1)) 
        img2avg = np.average(fgbg.apply(currentImage2)) 
        img3avg = np.average(fgbg.apply(currentImage3)) 
        img4avg = np.average(fgbg.apply(currentImage4)) 
        img5avg = np.average(fgbg.apply(currentImage5)) 
        
        cv2.imwrite(filepath + str(index) + 'lastImage1.jpg', fgbg.apply(currentImage1))
        cv2.imwrite(filepath + str(index) + 'lastImage2.jpg', fgbg.apply(currentImage2))
        cv2.imwrite(filepath + str(index) + 'lastImage3.jpg', fgbg.apply(currentImage3))
        cv2.imwrite(filepath + str(index) + 'lastImage4.jpg', fgbg.apply(currentImage4))
        cv2.imwrite(filepath + str(index) + 'lastImage5.jpg', fgbg.apply(currentImage5))
        index = index + 1
        if(img1avg >= max(img2avg, img3avg, img4avg,img5avg)):
            cv2.imwrite(filepath + 'lastImage.jpg', currentImage1)
        elif(img2avg >= max(img1avg, img3avg, img4avg,img5avg)):
            cv2.imwrite(filepath + 'lastImage.jpg', currentImage2)
        elif(img3avg >= max(img1avg, img2avg, img4avg,img5avg)):
            cv2.imwrite(filepath + 'lastImage.jpg', currentImage3)
        elif(img4avg >= max(img1avg, img2avg, img3avg,img5avg)):
            cv2.imwrite(filepath + 'lastImage.jpg', currentImage4)
        else:
            cv2.imwrite(filepath + 'lastImage.jpg', currentImage5)
        try:
            # Message composition
            msg = MIMEMultipart()
            msg['From'] = 'Your front door'
            msg['To'] = COMMASPACE.join(recipients)
            msg['Subject'] = ("Test")
            msg.attach(MIMEText(msgText))
    
            # Finding the picture in the directory and adding it to the message
            fp = open(filepath + 'lastImage.jpg', 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)
            server = smtplib.SMTP("smtp.gmail.com:587") #selecting the gmail server
            server.ehlo()
            server.starttls() #starting the gmail connection
            server.login(gmail_user, gmail_pwd) #logging into gmail
            server.sendmail(gmail_user, recipients, msg.as_string()) #sending the email
            server.quit()
            print "successfully sent"
            time.sleep(.5)
        except:
            print "failed to send"
            cap.release()
            break;
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break