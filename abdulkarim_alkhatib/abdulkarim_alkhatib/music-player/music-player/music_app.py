import pygame.mixer as mixer
from tkinter import *
from tkinter import filedialog
import audio_metadata
from PIL import ImageTk, Image
from io import BytesIO
import os
import time

# Function to play the selected songs from the list or directory.
def play_song(song_name: StringVar, song_list: Listbox, status: StringVar):
    # Set the name of the current played song on the window.
    name = song_list.get(ACTIVE)
    if len(name) > 40:
        name = (name[:35] + '.mp3')
    song_name.set(name)

    # Load the selected song and start the mixer/play the song.
    mixer.music.load(song_list.get(ACTIVE))
    mixer.music.play()

    # Extract the total song duration from the metadata of the song.
    global duration, metadata
    metadata=audio_metadata.load(song_list.get(ACTIVE))
    song_len = metadata.streaminfo['duration']
    duration = time.strftime('%M:%S', time.gmtime(song_len))

    # Call the play_time function when the song is played.
    play_time()

    # Set the status of the player to Playing.
    status.set("Song Playing..")

    # Active the disabled resume button.
    if resume_btn['state'] == DISABLED:
        resume_btn['state'] = NORMAL

    # Show the cover photo of the song.
    # get_song_img()

# Function to stop the current song and set the status of the player to 'stop'.
def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Song Stopped!!")

    # Disable the resume button when the song is stoped.
    resume_btn['state'] = DISABLED

# Function to pause the current song and set the status of the player to 'pause'.  
def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Song Paused!")

# Function to resume the paused song and set the status of the player to 'resume'.
def resume_song(status: StringVar):
    mixer.music.unpause()
    if status.get() == "<Not Available>":
        status.set("Please Select a song!")
    else:
        status.set("Song Playing..")

# Function to load all the songs from the specified directory. 
def load(listbox):
    # Request the user to input the path of the directory and os will change to that directory.
    os.chdir(filedialog.askdirectory(title="Open a song Directory"))
    
    # List all the songs present in the specified directory.
    tracks = os.listdir()

    # Takes all the songs from the directory and store in listbox.
    for track in tracks:
        listbox.insert(END, track)

# Function to change the sound volume.
def volume(x):
    value = volume_slider.get()
    mixer.music.set_volume(value/100)

def play_time():
    # Fetch the song's current time position,
    current_time = mixer.music.get_pos() / 1000

    # Convert the time into minute and second format.
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    # show the time on the duration frame and reset the timer when the song is stopped.
    song_duration = duration
   

def get_song_img():
    # get all metadata of song.mp3
    artwork = metadata.pictures[0].data
    stream = BytesIO(artwork)
    
    img = Image.open(stream)
    img_size = img.resize((50, 50))
    new_img = ImageTk.PhotoImage(img_size)

    image_label = Label(root, image=new_img)
    image_label.place(x=150, y=190)

# Starting the mixer.
mixer.init()

# Initializing the parent window of the GUI and set the resolution and the title of the GUI.
root = Tk()
root.geometry('700x400')
root.title('مشغل mp3')

# It helps to stop the change of the window size.
root.resizable(False, False)

# Creating the frames of the music player

button_frame = LabelFrame(root, text="الأوامر",  width=700, height=160)
button_frame.place(y=0)

listbox_frame = LabelFrame(root, text='Playlist', bg="red", height=160, width=700)
listbox_frame.place(x=0, y=160)




# StringVar is used to manipulate text in entry, labels.
current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

# Playlist Listbox.
playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='Gold', height=160, width=690)



playlist.pack( padx=5, pady=5)




# Buttons in the main screen.
pause_btn = Button(button_frame, text="إيقاف مؤقت", bg='red', font=('Georgia', 13), width=7, command=lambda: pause_song(song_status))
pause_btn.place(x=15, y=20)

stop_btn = Button(button_frame, text="إيقاف", bg='red', font=("Georgia", 13), width=7, command=lambda: stop_song(song_status))
stop_btn.place(x=105, y=20)

play_btn = Button(button_frame, text="تشغيل",  bg='red', font=("Georgia", 13), width=7, command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=20)

resume_btn = Button(button_frame, text='متابعة',  bg='red', font=("Georgia", 13), width=7, command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=20)

dir_btn = Button(button_frame, text="إستيراد", bg='red', font=("Georgia", 13), width=7, command=lambda: load(playlist))
dir_btn.place(x=380, y=20)

# Control the volume of the song.


# Finalize and start the main loop of the GUI.
root.update()
root.mainloop()