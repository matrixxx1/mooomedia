import random
import tkinter
from tkinter.font import Font
import pygame
from guizero import App, ListBox, PushButton, Text, Slider
import os
from glob import iglob
from mutagen.mp3 import MP3

global app
global lbSongList
global textbox
global button
global MUSIC_END
global startpath

pygame.init()
MUSIC_END = pygame.USEREVENT+1

def quit_app():
    app._close_window
    exit()

def get_files():
    startpath=os.getcwd()
    lbSongList.clear()
    file_list = [f for f in iglob(startpath + "/**/*", recursive=True) if os.path.isfile(f)]
    for f in file_list:
        if f.find(".mp3")!=-1:
            addat=0
            if lbSongList.items.__len__()==0:
                addat = 0
            else:
                addat = random.randrange(lbSongList.items.__len__())
            lbSongList.insert(addat,f)     
    pygame.mixer.music.stop()
    
def prev_music():
    rotate_songs(False)
    play_music()

def skip_music():
    rotate_songs(False)
    play_music()

def play_music():
    thissong = lbSongList.items[0]
    Load_SongNow(thissong)    

def play_pausebtn():
    if (btnPlay.text=="Pause"):
        btnPlay.text="Play"
        pygame.mixer.music.pause()        
    else:
        btnPlay.text="Pause"
        pygame.mixer.music.unpause()
        
def Load_SongNow(songFile):
    txtNowPlaying.value=songFile.replace(os.getcwd(),"") + "    "
    pygame.mixer.music.load(songFile)
    pygame.mixer.music.play(0)
    MUSIC_END = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(MUSIC_END)
    song = MP3(songFile)
    txtSongLen.value=round(song.info.length)
            
def stop_music():
    pygame.mixer.music.stop()

def rotate_songs(forward):
    if (forward==True):
        thissong = lbSongList.items[0]
        lbSongList.remove(thissong)
        lbSongList.insert(lbSongList.items.__len__(), thissong)
    else:
        thissong = lbSongList.items[lbSongList.items.__len__()-1]
        lbSongList.remove(thissong)
        lbSongList.insert(0, thissong)

def song_ended():
    rotate_songs(True)    
    play_music()

def getPerc(num_a, num_b):
    return (num_a / num_b) * 100

def slider_changed(slider_value):
    print(slider_value)

def rotateText(startStr):
    return startStr[1:] +  startStr[0:1]  

def refresh_UI():
    app.title="Status: " + str(pygame.mixer.music.get_pos()) + ", Busy: " + str(pygame.mixer.music.get_busy()) + ", File: " + pygame.mixer.music.__file__
    AtNow=pygame.mixer.music.get_pos()/1000
    if (txtSongLen.value!="0"):
        Perc = getPerc(AtNow,float(txtSongLen.value))
        txtCurPos.value=str(round(Perc))+"%, " + str(round(AtNow)) + "s"
        setSlider=round(slider.width * (Perc /100))
        slider.value=round(Perc)
    if (pygame.mixer.music.get_busy()==True):
        btnPlay.text="Pause"
    else:
        btnPlay.text="Play"
    txtNowPlaying.value = rotateText(txtNowPlaying.value)
    for event in pygame.event.get():
        if event.type==pygame.error:
            print("Error")
        if event.type == MUSIC_END:
            song_ended()            
    lbSongList.visible=False

pygame.mixer.init()
app = App(title="Mooo Media Player", layout="grid", width="500", height="150")

txtCurPos = Text(app, text="1", grid=[0,0,3,1],width="fill")
txtSongLen = Text(app, text="1", grid=[4,0,3,1],width="fill")
txtNowPlaying = Text(app, text="Press play to begin", grid=[0,1,6,1],width="fill")
button = PushButton(app,command=get_files,text="Shuffle", grid=[0,3],width="fill")
btnStop = PushButton(app,command=stop_music,text="[ ] Stop", grid=[1,3],width="fill")
btnResume = PushButton(app,command=prev_music,text="<< Prev", grid=[2,3],width="fill")
btnPlay = PushButton(app,command=play_pausebtn,text="Play", grid=[3,3],width="fill")
btnSkip = PushButton(app,command=skip_music,text=">> Skip", grid=[4,3],width="fill")
btnQuit = PushButton(app,command=quit_app,text="Quit", grid=[5,3],width="fill")

slider = Slider(app, command=slider_changed, grid=[0,4,6,1], width=app.width - 10)

lbSongList = ListBox(app, items=[],scrollbar=True,multiselect=False, grid=[0,5,6,1],width="fill")

get_files()
app.repeat(500,refresh_UI)
play_music()
app.display() 
