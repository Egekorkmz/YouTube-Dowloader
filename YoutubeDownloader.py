import os
import customtkinter
import pytube

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#Main Window
root = customtkinter.CTk()
root.geometry("700x500")
root.title("Youtube Video Downloader")
root.iconbitmap(resource_path("youtube.ico"))
root.resizable(False, False)

##Takes Url address of the video and audio check and Creates a youtube object and returns it
def createYoutubeObj(URL, Audio):
    yt = pytube.YouTube(URL)
    if Audio == 1 :
        Video = yt.streams.filter(only_audio=True)
    else:    
        Video = yt.streams.filter(progressive=True)
    return Video

#finds the url and creates a list of video names to choose from
def findUrl():
    global VideoNames 
    VideoNames = []
    
    global videos 
    videos = createYoutubeObj(entryurl.get(), switchAudio.get())
    
    alertTxt.pack_forget()
    if switchAudio.get() == 1:
        for i in range(len(videos)):
            temp = ""
            temp += "Type: " + videos[i].mime_type +  "   "  + "".join(videos[i].abr) 
            VideoNames.append(temp)
    else:
        for i in range(len(videos)):
            temp = ""
            temp += "Type: " + videos[i].mime_type + "   " + "".join(videos[i].resolution) +" " + "".join(videos[i].codecs)
            VideoNames.append(temp)
    
    options.set(VideoNames[0])
    options.configure(values = VideoNames)
    options.pack(pady = 12 , padx = 10)
    buttondownload.pack(pady = 12, padx = 10)

#downloads the video and change name acording to selection
def downloadvideo():
    video = videos[VideoNames.index(options.get())]
    video.download()

    if switchAudio.get() == 1:
        os.rename(video.default_filename, video.title + ".mp3")
    
    alertTxt.configure(text="Your download is finished. Your file is in the same folder as this program.")
    alertTxt.pack(pady=12, padx=10)
    buttondownload.pack_forget()
    options.pack_forget()
    VideoNames.clear()
    


#GUI
frame = customtkinter.CTkFrame(master = root)
frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

label = customtkinter.CTkLabel(master = frame, text ="Youtube Video Downloader", font =("Roboto", 24), width= 650)
label.pack(pady=12, padx=10)

entryurl = customtkinter.CTkEntry(master=frame, placeholder_text= "Enter Youtube Video Url", width = 550)
entryurl.pack(pady = 12, padx = 10)

buttonfind = customtkinter.CTkButton(master = frame, text= "Find", command= findUrl)
buttonfind.pack(pady = 12, padx = 10)

switchAudio = customtkinter.CTkSwitch(master=frame, text="Only audio", onvalue=1, offvalue=0)
switchAudio.pack(padx=12, pady=10)

options = customtkinter.CTkComboBox(master = frame, width= 450, hover=True, state="readonly")

buttondownload = customtkinter.CTkButton(master = frame, text= "Download", command= downloadvideo)

alertTxt = customtkinter.CTkLabel(master= frame, text="Your download is finished.")

root.mainloop()