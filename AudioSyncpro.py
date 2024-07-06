
# Copyright (C) [2023] by Stream Sonic tools
# All Rights Reserved to Stream Sonic tools
#
# This software is the property of Stream Sonic tools and is protected by copyright law.
# Unauthorized reproduction or distribution of this software, or any portion of it,
# may result in severe civil and criminal penalties, and will be prosecuted to the
# maximum extent possible under the law.
#Reach out to info@streamsonic.ca if you have any questions.

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os
from shutil import which
from concurrent.futures import ProcessPoolExecutor
import sys

def find_ffmpeg():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the FFmpeg executable
    # Adjust the executable name if necessary (e.g., for different operating systems)
    ffmpeg_executable_path = os.path.join(script_dir, 'FFmpeg\\bin\\ffmpeg.exe')

    if os.path.isfile(ffmpeg_executable_path):
        return ffmpeg_executable_path

    # FFmpeg not found in the script directory
    messagebox.showerror("Error", "FFmpeg executable not found in the script directory.")
    return None

# Function to replace audio in MP4 file
def replace_audio(video_path, audio_path, output_path, ffmpeg_path):
    cmd = [
        ffmpeg_path,
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-y',
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to process multiple videos
def process_videos(directory, audio_path, ffmpeg_path):
    if not audio_path or not directory:
        messagebox.showerror("Error", "Please select the audio file and directory.")
        messagebox.showerror("Copyrights", "This software is the property of Stream Sonic tools. All Rights Reserved to Stream Sonic tools.")
        return

    with ProcessPoolExecutor() as executor:
        for file_name in os.listdir(directory):
            if file_name.endswith(".mp4") and file_name != os.path.basename(audio_path):
                video_path = os.path.join(directory, file_name)
                output_path = os.path.join(directory, f"new_{file_name}")
                executor.submit(replace_audio, video_path, audio_path, output_path, ffmpeg_path)
    messagebox.showinfo("Success", "All videos have been processed.")
    messagebox.showinfo("Copyrights", "This software is the property of Stream Sonic tools. All Rights Reserved to Stream Sonic tools.")
# Main UI function
def main_ui():
    root = tk.Tk()
    root.title("Audio Sync Pro")

    # Variables to store user selections
    audio_file_var = tk.StringVar(root)
    directory_var = tk.StringVar(root)

    # Functions to select audio file and directory
    def select_audio_file():
        audio_file_var.set(filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")]))
        
    def select_directory():
        directory_var.set(filedialog.askdirectory())
        
    # Widgets for UI
    tk.Button(root, text="Select MP4 with Audio", command=select_audio_file).pack()
    tk.Button(root, text="Select Directory with MP4s", command=select_directory).pack()
    
    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path is None:
        root.destroy()
        return

    def on_process_videos():
        process_videos(directory_var.get(), audio_file_var.get(), ffmpeg_path)

    tk.Button(root, text="Process Videos", command=on_process_videos).pack()

    root.mainloop()

if __name__ == "__main__":
    main_ui()
