#Project 6 for Resume, combined proJ 4+5 for camera, face tracking application OpenCV + Tkinter GUI+Pillow
#Inspired by Pysch Imtimacy Lab on Phubbing
#Status: Finish but ongoing improvements. 
#**Improvements to make: Perhaps set a countdown timer for practical reseach. How to make face recognition more accurate to phubbing? 
import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import time

class PhubbingTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Phubbing Tracker")

        # open OpenCV for webcam and face detection
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # tracking variables
        self.phubbing_time = 0
        self.focus_time = 0
        self.start_time = None
        self.is_phubbing = False

        # UI 
        self.status_label = Label(root, text="Status: Not Phubbing", font=("Arial", 18))
        self.status_label.pack(pady=20)
        self.phubbing_label = Label(root, text="Phubbing Time: 0 sec", font=("Arial", 14))
        self.phubbing_label.pack()
        self.focus_label = Label(root, text="Focus Time: 0 sec", font=("Arial", 14))
        self.focus_label.pack()
        self.reset_button = tk.Button(root, text="Reset", command=self.reset, width=15, height=2)
        self.reset_button.pack(pady=10)

        # webcam 
        self.video_label = Label(root)
        self.video_label.pack()

        self.update_video()  #  webcam tracking
        self.update_time()   # time tracking

    def reset(self):
        """Reset timers and status."""
        self.phubbing_time = 0
        self.focus_time = 0
        self.start_time = None
        self.is_phubbing = False
        self.status_label.config(text="Status: Not Phubbing")
        self.phubbing_label.config(text="Phubbing Time: 0 sec")
        self.focus_label.config(text="Focus Time: 0 sec")

    def update_time(self):
        """Update phubbing and focus timers."""
        if self.is_phubbing:
            self.phubbing_time += 1
            self.phubbing_label.config(text=f"Phubbing Time: {self.phubbing_time} sec")
        else:
            self.focus_time += 1
            self.focus_label.config(text=f"Focus Time: {self.focus_time} sec")

        # schedule the time update/second
        self.root.after(1000, self.update_time)

    def update_video(self):
        """Update the webcam feed and determine focus/phubbing status."""
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # face is detected= phubbing, else= focus
            if len(faces) > 0:
                self.is_phubbing = True
                self.status_label.config(text="Status: Phubbing")
            else:
                self.is_phubbing = False
                self.status_label.config(text="Status: Focused")

            # convert to RGB and display in Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

        # video tracking update
        self.root.after(10, self.update_video)

    def __del__(self):
        """Release the webcam resource."""
        if self.cap.isOpened():
            self.cap.release()

#run program app
if __name__ == "__main__":
    root = tk.Tk()
    app = PhubbingTracker(root)
    root.mainloop()
