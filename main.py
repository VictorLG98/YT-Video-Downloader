from pytube import YouTube, Playlist
import tkinter
from threading import Thread
from tkinter import ACTIVE, CENTER, DISABLED, messagebox, filedialog
from tkinter import ttk


class YTDownloader():
    
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.title("YT Downloader")
        self.window.config(padx=20, pady=20, background='#105ae3')
        self.window.resizable(False, False)
        
        self.directory = None
        self.len_playlist = None
        
        self.label_Video = tkinter.Label(text="Enter URL", font=('Arial', 15, 'bold'), background="#105ae3",
                                         foreground='#02046e')
        self.label_Video.grid(row=0, column=0, pady=10)
        self.entry_Video = tkinter.Entry(width=50, font=('Helvetica', 13, 'bold'), background='black',
                                         foreground='white', highlightthickness=0, border=0, borderwidth=0)
        self.entry_Video.grid(row=1, column=0)
        self.btn_Video = tkinter.Button(text="Download", command=self.threading, background='#02586e',
                                        font=('Helvetica', 13, 'bold'))
        self.btn_Video.grid(row=2, column=0, pady=10, sticky='EW')
        self.label_Video.grid(row=0, column=0, pady=10)
        
        self.btn_Playlist = tkinter.Button(text="Download Playlist", command=self.threading_Playlist, background='#02586e',
                                        font=('Helvetica', 13, 'bold'))
        self.btn_Playlist.grid(row=3, column=0, pady=10, sticky='EW')
        
        self.spin = ttk.Spinbox(from_=1, to=500, increment=5, justify=CENTER)
        self.spin.grid(row=4, column=0)
        self.spin.set(1)
        
        self.window.mainloop()
        
       
    def threading(self):
        self.deactive_buttons()
        t1 = Thread(target=self.download_video) 
        t1.start()
        
    def threading_Playlist(self):
        self.deactive_buttons()
        t2 = Thread(target=self.download_playlist) 
        t2.start()
     
    def download_video(self):
        video_link = self.entry_Video.get()
        
        if "list=" in video_link:
            messagebox.showwarning(title="Warning!", message="This url refers to a Playlist. Use the other button to download Playlists.")
            self.active_buttons()
        else:
            try:
                yt = YouTube(video_link)
            except:
                messagebox.showerror(title="Invalid YT url", message="You must enter a valid url.")
                self.active_buttons()
            else:
                download = messagebox.askyesno(title="Are you sure you want to download?",
                                            message=f"Title: {yt.title}\nViews: {yt.views}\nAuthor: {yt.author}")                

                self.deactive_buttons()
                if download:
                    choose_directory = messagebox.askyesno(title="Choose directory?", message="Do you want to choose a video path? (Default is current directory)")
                    if choose_directory:
                        path = filedialog.askdirectory()
                        yd = yt.streams.get_highest_resolution()
                        yd.download(path)
                        self.active_buttons()
                        messagebox.showinfo(title="Info", message="Video downloaded succesfully!")
                    else:
                        yd = yt.streams.get_highest_resolution()
                        yd.download()
                        self.active_buttons()
                        messagebox.showinfo(title="Info", message="Video downloaded succesfully!")
                
        
    def download_playlist(self):
        try:
            p = Playlist(self.entry_Video.get())
            self.len_playlist = len(p.videos)
        except:
            messagebox.showerror(title="Invalid YT url", message="You must enter a valid url.")
            self.active_buttons()
        else:
            download_all = messagebox.askyesno(title="Atention!", message=f"There are {self.len_playlist} videos on this playlist. Do you want to download them all or only {self.spin.get()}?")
            choose_directory = messagebox.askyesno(title="Choose directory?", message="Do you want to choose a video path? (Default is current directory)")
            if choose_directory:
                path = filedialog.askdirectory()
            else:
                pass
            
            if download_all:
                for video in p.video_urls:
                    yt = YouTube(video)
                    yd = yt.streams.get_highest_resolution()
                    if choose_directory:
                        yd.download(path)
                    else:
                        yd.download()
                    print(f"Video {yt.title} downloaded succesfully")
                    
                self.active_buttons()
            else:
                how_many = self.spin.get()
                if how_many:
                    how_many = int(how_many)
                    if how_many < 1 or how_many > self.len_playlist:
                        messagebox.showerror(title="Error!", message="You must enter a correct number of videos!")
                        self.active_buttons()
                    else:
                        for video in p.video_urls[:how_many]:
                            yt = YouTube(video)
                            yd = yt.streams.get_highest_resolution()
                            if choose_directory:
                                yd.download(path)
                            else:
                                yd.download()
                            print(f"Video {yt.title} downloaded succesfully")
                        
                        self.active_buttons()
                else:
                    messagebox.showerror(title="Error!", message="You must enter a number!")
                    self.active_buttons()
                    
                    
    def deactive_buttons(self):
        self.btn_Playlist.config(state=DISABLED)
        self.btn_Video.config(state=DISABLED)
        
    def active_buttons(self):
        self.btn_Playlist.config(state=ACTIVE)
        self.btn_Video.config(state=ACTIVE)
        
    

if __name__ == "__main__":
    YTD = YTDownloader()
