# -*- coding: utf-8 -*-
"""


This is a project initiated and developed by Matteo Montanari
Copyright (C) 2016 Matteo Montanari <matteo.montanari25@gmail.com>

If you want to contribute please contact me at the e-mail address above
-------------------------------------------------------------


"""

import os
import time
import datetime
import imutils
import urllib2
import cv2
import requests
from Tkinter import *
import Tkinter as tk
import tkMessageBox
import PIL.Image as Image
import PIL.ImageTk as  ImageTk



curent_path = os.path.dirname(os.path.abspath(__file__))

list_labels = [#INSERT YOUR LABELS
  ]

#FUNCTIONS FOR INTERROGATION OF THE MODEL

def interview_the_model(path_to_the_file):
    
    global SERVER_ADDRESS

    url = "http://192.168.1.107:5000/upload"
    url = SERVER_ADDRESS + ":5000/upload"
    files = {'image': open(path_to_the_file, 'rb')}
    r = requests.post(url, files=files)
    print(r.status_code)

    return r.status_code

def ask_the_tag():

    global SERVER_ADDRESS

    url = SERVER_ADDRESS + ":5000/getdata"
    print(url)
    
    r = requests.get(url)
    print(r.text)
    return r.text
        

   
class View_Cotroller():

    def __init__(self, Window_MAIN):


    #Camera object - video frames provider
        self.Captured_picture = cv2.VideoCapture(-1)

    # OBJECT of MAIN WINDOW
        self.Window_MAIN = Window_MAIN
        
    # FRAME
        Grid.rowconfigure(self.Window_MAIN, 0, weight=1)
        Grid.columnconfigure(self.Window_MAIN, 0, weight=1)
        self.frame = tk.Frame(self.Window_MAIN)
        self.frame.grid(row=0, column=0, sticky=N+S+E+W)
        
        Grid.rowconfigure(self.frame, 1, weight=1)
        Grid.rowconfigure(self.frame, 2, weight=1)
        Grid.rowconfigure(self.frame, 3, weight=1)
        Grid.rowconfigure(self.frame, 4, weight=1)
        Grid.rowconfigure(self.frame, 5, weight=1)
        Grid.rowconfigure(self.frame, 6, weight=1)
        Grid.columnconfigure(self.frame, 1, weight=1)
        Grid.columnconfigure(self.frame, 2, weight=1)


    # VIDEOlabel
        self.VIDEOlabel = tk.Label(self.frame,  text="Camera Streaming", font="TkHeadingFont 24")
        self.VIDEOlabel.grid(row=0, column=0, sticky=N+S+E+W, padx=5, pady=5)
		
    # Camera Streaming Area
        self.Video_display_Area = tk.Label(self.frame)
        self.Video_display_Area.grid(row=1, column=0, padx=15, pady=15, rowspan=2, sticky=N+W )  
        
    # Reset Camera
        self.Reset_Button = tk.Button(self.frame, command=self.Reset_camera)
        self.Reset_Button.configure(text="Reset Camera", font=("Helvetica",13))
        self.Reset_Button.grid(row=1, column=1, sticky=N+S+W+E, ipadx=15, padx=15, ipady=15, pady=15)
        
    # Start functionality
        self.Recon_functionalities = tk.Button(self.frame,  command=self.both_start_functionality_and_reset_camera)
        self.Recon_functionalities.configure(text="Start Functionality", font=("Helvetica", 13))
        self.Recon_functionalities.grid(row=2, column=1, sticky=N+S+E+W, ipadx=15, padx=15, ipady=15, pady=15)
		
    # Buottom label
        self.Buottomlabel = tk.Label(self.frame,  text="___________________________________________________________________________________________________________________________________________________", font="TkHeadingFont 10")
        self.Buottomlabel.grid(row=6, column=0, columnspan=2, sticky=N+S+E+W, pady=5, ipady=15)


    # COUNTROUN AREA CONSTANT (future variable) for minimum contour area to consider
        self.COUNTROUN_AREA = 200
        self.firstFrame = None
        self.frameDelta = None
        self.thresh = None


    #Control Variables
        self.On_stak_frame = None
        self.Pause_control = 0
        self.functionality_On_or_Off = 0        
        self.model_initialized = False
        self.IMAGE_COUNT = 0
        self.COUNT_FRAME_WAITING = 15
 
    #CONTROL METHODs
    def change_contrlo_value_for_show(self):

        if self.functionality_On_or_Off == 0:

            self.functionality_On_or_Off = 1
            print("changed to functionality ON ")
            self.Recon_functionalities.configure(text="Functionality is On", font=("Helvetica", 13))

        else:

            self.functionality_On_or_Off = 0
            print("changed to functionality OFF ")
            self.Recon_functionalities.configure(text="Start Functionality", font=("Helvetica", 13))


    def both_start_functionality_and_reset_camera(self):
        self.Reset_camera()
        self.change_contrlo_value_for_show()

    def Reset_camera(self):
        self.frameDelta = None
        self.thresh = None
        self.IMAGE_COUNT = 0
        self.firstFrame = None
        self.On_stak_frame = None
        self.Captured_picture = None
        self.Captured_picture = cv2.VideoCapture(-1)
        

    def servo_using(self, name_of_material):
	
	    print(name_of_material)
        


    def presence_counter(self, indicator):
        if indicator:
            self.IMAGE_COUNT = self.IMAGE_COUNT +1

        else:
            self.IMAGE_COUNT = 0




        #VIEW METHODs
    def show_frame(self):

        if self.functionality_On_or_Off == 0:
            self.show_frame_Image()

            if self.IMAGE_COUNT >= self.COUNT_FRAME_WAITING + 1:

                self.IMAGE_COUNT = self.COUNT_FRAME_WAITING


        elif self.functionality_On_or_Off == 1:

            self.show_frame_Image()
            
            if self.IMAGE_COUNT == self.COUNT_FRAME_WAITING:
            
                path_for_the_file = curent_path + '/img.jpg'

                _, self.On_stak_frame = self.Captured_picture.read()

                cv2.imwrite( path_for_the_file , self.On_stak_frame )

                result_of_the_model = interview_the_model(path_for_the_file)

                print(result_of_the_model)

                if result_of_the_model == 200:
                                  
                    image_tag = ask_the_tag()

                    self.servo_using(image_tag)
                    
                    time.sleep(2)
                        
                    self.Reset_camera()
                else:
                    self.Reset_camera()

            elif self.IMAGE_COUNT >= self.COUNT_FRAME_WAITING + 1:

                self.IMAGE_COUNT = 15

            elif self.IMAGE_COUNT < self.COUNT_FRAME_WAITING + 1:
                pass

            else :
                print("Something happened on the way to heaven_1")
        else:
            print("Something happened on the way to heaven_1")


  
    def show_frame_Image(self):    #ESSENTIAL

        # Either keep the pause "picture" or assign a new image to variable named frame
        _, self.On_stak_frame = self.Captured_picture.read()
        #self.On_stak_frame = frame

        # resize the frame, convert it to grayscale, and blur it
        self.On_stak_frame= imutils.resize(self.On_stak_frame, width=800)
        gray = cv2.cvtColor(self.On_stak_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)


        # if the first frame is None, initialize it
        if self.firstFrame is None:
            self.firstFrame = gray

        # resize the frame, convert it to grayscale, and blur it compute the absolute difference between the current frame and first frame
        self.frameDelta = cv2.absdiff(self.firstFrame, gray)
        self.thresh = cv2.threshold(self.frameDelta, 60, 350, cv2.THRESH_BINARY)[1]
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)
        #https://stackoverflow.com/questions/25504964/opencv-python-valueerror-too-many-values-to-unpack
        (cnts, _) = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # the Contours_definer function either choose that the room is UNoccupied
        self.On_stak_frame, contourns_index = self.contourn_definier(cnts, self.On_stak_frame)

        self.presence_counter(contourns_index)

        #print(self.IMAGE_COUNT)

        # Display of the image
        cv2image = cv2.cvtColor(self.On_stak_frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.Video_display_Area.imgtk = imgtk
        self.Video_display_Area.configure(image=imgtk)

        # CallBack itself
        self.Window_MAIN.after(100, self.show_frame)        


    def explicit(self, l):       
        max_val = max(l)
        max_idx = l.index(max_val)
        return max_idx, max_val

    def contourn_definier(self, contourns, frame_to_contourn):  

        # Momentary List
        Momentary_dict_of_contourn = {}

        # loop over the contours
        for index, c in enumerate(contourns):
            count = 0
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.COUNTROUN_AREA:
                continue
            Momentary_dict_of_contourn[cv2.contourArea(c)] = index

        if len(Momentary_dict_of_contourn) == 0:
            return frame_to_contourn, False

        else:
            # list of only values of the contourns' AREA  print len(Momentary_dict_of_contourn)
            list_contourn_Area = Momentary_dict_of_contourn.keys()
            Index_of_the_maximum_area_contourn , Max_Area_Contourn  = self.explicit(list_contourn_Area)

            Index_of_the_chosen_Contourn = Momentary_dict_of_contourn[Max_Area_Contourn]

            # compute the bounding box for the contour, draw it on the frame, and update the text
            (x, y, w, h) = cv2.boundingRect( contourns[Index_of_the_chosen_Contourn])
            cv2.rectangle(frame_to_contourn, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text_index = True
            return frame_to_contourn , text_index



def main():
    filename = "log.txt"
    f = open(filename, "r")
    StoredAddress = f.read() 
    f.close()

    root = Tk().withdraw()  # hiding the main window
    var = tkMessageBox.askyesno("Search for Server option", "Do you want to use a pre-stored server address?\n" + StoredAddress)
	root = None

    def server_address_finder():
        for level2 in xrange(256):
            for level1 in xrange(256):
                try:
                    hostname = "http://192.168." + str(level2) + "." +  str(level1) + ":5000/getid"
                    hostname2 = "http://192.168." + str(level2) + "." +  str(level1)
                    print("reuqesting @: " + hostname)
                    r = requests.get(hostname, timeout=0.01)
                    if r.text == "image_server":
                        return hostname2
                except:
                    pass
                    
                    
    if var == False:
        SERVER_ADDRESS = server_address_finder()
        filename = "log.txt"
        f = open(filename, "w")
        f.write(SERVER_ADDRESS) 
        f.close()
    else:
        SERVER_ADDRESS = StoredAddress
    #Set up GUI Main Window 
    #Makes main window  https://stackoverflow.com/questions/25460418/cannot-associate-image-to-tkinter-label
    window = tk.Toplevel()
    window.wm_title("Personal Recognizer")
    window.config(background="#FFFFFF")



# INITIALIZATION AND START OF THE GLUI (SOFTWARE)
    Show_begin = View_Cotroller(window)
    Show_begin.show_frame() #Display
    window.mainloop()  #Starts GUI
	
if __name__ == "__main__":
    # execute only if run as a script
    main()
    


