# -----------------------------------------------------------------------------
# Project Name: Form Trainer
# File: form_trainer.py
# BSD 3-Clause License
# 
# Copyright (c) 2024, Mateus Paiva Fogaca
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
 
import cv2
import mediapipe as mp
import argparse
import os
from tqdm import tqdm
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import threading
from PIL import Image, ImageTk
from settings import global_settings

def process_video_file(root):
    # Initialize MediaPipe pose detection
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode        = global_settings.pose_static_image_mode(),
        model_complexity         = global_settings.pose_model_complexity(),       
        min_detection_confidence = global_settings.pose_min_detection_confidence(),
        min_tracking_confidence  = global_settings.pose_min_tracking_confidence() 
    )

    mp_drawing = mp.solutions.drawing_utils

    input_file = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.MOV;*.mkv"), ("All files", "*.*")]
    )
    if not input_file:
        return

    output_file = filedialog.asksaveasfilename(
        title="Create output file",
        defaultextension=".mp4",
        filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.MOV;*.mkv"), ("All files", "*.*")]
    )
    if not output_file:
        return

    # Open the video file
    cap = cv2.VideoCapture(input_file)

    if not cap.isOpened():
        print(f"Error: Unable to open video file {input_file}")
        return

    # Get video properties
    frame_count  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps          = int(cap.get(cv2.CAP_PROP_FPS))

    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    with tqdm(total=frame_count, desc="Processing Video", unit="frame") as pbar:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB (MediaPipe requires RGB input)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform pose detection
            result = pose.process(frame_rgb)

            # Draw landmarks and connections on the frame
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Write the processed frame to the output video
            out.write(frame)
            pbar.update(1)

    # Release resources
    cap.release()
    out.release()
    pose.close()

    print(f"Processed video saved as {output_file}")

def process_camera(canvas, apply_filter, cam_id, stop_event):
      # Initialize MediaPipe Pose and Drawing utilities
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Set up the Pose model
    pose = mp_pose.Pose(
        static_image_mode        = global_settings.pose_static_image_mode(),
        model_complexity         = global_settings.pose_model_complexity(),       
        min_detection_confidence = global_settings.pose_min_detection_confidence(),
        min_tracking_confidence  = global_settings.pose_min_tracking_confidence()
    )

    cap = cv2.VideoCapture(cam_id)  # Change the ID for other cameras (e.g., 1, 2)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB for tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (canvas_width, canvas_height))

        result = pose.process(frame)

        if apply_filter == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.Canny(frame, threshold1=75, threshold2=150)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk  # Keep a reference to avoid garbage collection
        canvas.update()
        

def get_available_cameras():
    cam_ids = []
    for i in range(4):  # only allow four inputs
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cam_ids.append(i)
            cap.release()
    return cam_ids

def start_cameras(root):
    cam_ids = get_available_cameras()
    tk.messagebox.showinfo("Info", f"{len(cam_ids)} camera(s) were found")

    second_window = tk.Toplevel(root)
    second_window.title(f"Camera (model complexity: {global_settings.pose_model_complexity()})")

    canvas = tk.Canvas(second_window, width=640, height=480)
    canvas.grid(row=0, column=0)

    stop_event = threading.Event()
    thread = threading.Thread(target=process_camera, args=(canvas, False, cam_ids[0], stop_event))
    thread.daemon = True
    thread.start()

    close_button = tk.Button(second_window, text="Close", command=second_window.destroy)
    close_button.grid(row=1, column=0, columnspan=2)

def add_model_complexity_opt(root, target_row):
    label = tk.Label(root, text="Select model complexity:")
    label.grid(row=target_row, column=0, padx=10, pady=10)

    complexity_scale = tk.Scale(root, from_=0, to=2, orient=tk.HORIZONTAL, 
                                command=lambda v: global_settings.set_pose_model_complexity(int(v)))
    complexity_scale.grid(row=target_row, column=1, padx=10, pady=10)
    complexity_scale.set(1)

def add_min_detection_confidence_opt(root, target_row):
    label = tk.Label(root, text="Select min detection confidence:")
    label.grid(row=target_row, column=0, padx=10, pady=10)

    confidence_scale = tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
    confidence_scale.set(0.5)  # Set the default value
    confidence_scale.grid(row=target_row, column=1, padx=10, pady=10)

def add_apply_button(root, target_row):
    submit_button = tk.Button(root, text="Apply setup")
    submit_button.grid(row=target_row, column=0, columnspan=2, pady=10)

def add_start_cameras_button(root, target_row):
    submit_button = tk.Button(root, text="Start cameras", command=lambda: start_cameras(root))
    submit_button.grid(row=target_row, column=0, columnspan=2, pady=10)

def add_process_video_button(root, target_row):
    submit_button = tk.Button(root, text="Process video file", command=lambda: process_video_file(root))
    submit_button.grid(row=target_row, column=0, columnspan=2, pady=10)

def start_gui():
    root = tk.Tk()
    root.title("FormTrainer (prototype)")

    add_model_complexity_opt(root, 0)
    add_min_detection_confidence_opt(root, 1)
    add_start_cameras_button(root, 2)
    add_process_video_button(root, 3)

    root.mainloop()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_gui();
    quit()