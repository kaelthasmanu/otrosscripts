from pytube import *
from multiprocessing import Pool
from tkinter import *
from tkinter import ttk

def get_data():
   text= entry.get()
   print(text)



def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = video.filesize
    size = contentsize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), end='')

def downloadVideo(url_video):
    print(video_url)
    my_video = YouTube(video_url,on_progress_callback=progress)

    print("*****************DOWNLOAD VID*************")
    print(my_video.title)

    my_video = my_video.streams.get_highest_resolution()
    path = "E:\cursos"
    my_video.download(path)
    print("VIDEO DOWNLOAD DONNNNE")

'''
playlist = Playlist('https://www.youtube.com/playlist?list=PLyvsggKtwbLX06iMtXnRGX5lyjiiMaT2y')
print('Number of videos in playlist: %s' % len(playlist.video_urls))
for video_url in playlist.video_urls:
    downloadVideo(video_url)
    #with Pool(2) as p:
        #p.map()
'''

root = Tk()
frm = ttk.Frame(root, padding=10)
root.geometry("600x600")
frm.grid()
ttk.Label(frm, text="Introduzca la URL de la lista de video").grid(row=0)
entry = Entry(frm, width= 42)
entry.place(relx= .5, rely= .5, anchor= CENTER)
entry.grid(row=0, column=1)
ttk.Button(frm, text= "Download", command= get_data).place(relx= .93, rely= .16, anchor= CENTER)
txt = Text(root, width=60, height=20).place(relx= .50, rely= .40, anchor= CENTER)
txt.insert(INSERT, "Write Something About Yourself")
txt.pack(expand= 1, fill=BOTH)
#ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=3)
root.mainloop()


'''
def parse_args():
    parser = argparse.ArgumentParser(description='YouTube Video/Audio Downloader')
    parser.add_argument('-u', '--url', help='YouTube URL or YouTube Video ID to download', default=None)
    parser.add_argument('-l', '--list-streams', help='List available streams for this YouTube Video '
                                                     'instead of download. Use -a/--audio-only to list audio streams. '
                                                     'Download specific stream with the '
                                                     'itag ID and -i/--itag argument.',
                        action='store_true', default=False)
    parser.add_argument('-i', '--itag', help='Stream ITAG to download for given YouTube Video/ID. '
                                             'List streams with -l/--list-streams argument. '
                                             'If ITAG is not provided, default stream will be downloaded. '
                                             'Downloading with ITAG ignores -a/--audio-only.', type=int, default=None)
    parser.add_argument('-o', '--output-path', help='Output Directory Path', default=None)
    parser.add_argument('-f', '--filename', help='Override the output filename. Does not override file extension',
                        default=None)
    parser.add_argument('-p', '--proxy', help='Proxy to use. Ex http://xxx.xxx.xxx:8080 '
                                              'NOTE: You need https proxy for https URL!', default=None)
    parser.add_argument('-a', '--audio-only', help='Download Audio Only', action='store_true', default=False)

    parsed_args = parser.parse_args()
    if parsed_args.proxy:
        parsed_args.proxy = {parsed_args.proxy.split(':')[0]: parsed_args.proxy}
    return parsed_args
'''