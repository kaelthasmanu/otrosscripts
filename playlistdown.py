from pytube import Playlist
from pytube import *

urls = []
playlist = Playlist('https://www.youtube.com/playlist?list=PLyvsggKtwbLX06iMtXnRGX5lyjiiMaT2y')
print('Number of videos in playlist: %s' % len(playlist.video_urls))
for video_url in playlist.video_urls:
    print(video_url)
    urls.append(video_url)
    for url in urls:
        my_video = YouTube(url)

        print("*****************DOWNLOAD VID*************")
        print(my_video.title)

        my_video = my_video.streams.get_highest_resolution()
        path = "E:\cursos"
        my_video.download(path)
        print("VIDEO DOWNLOAD DONNNNE")
        
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