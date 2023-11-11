import pytube
from moviepy.editor import AudioFileClip
import os


class Downloader:
    def __init__(self):
        super().__init__()

    def download_video(self, url_video, destino):
        self.yt = pytube.YouTube(url_video)
        self.video = self.yt.streams.get_highest_resolution()
        self.video.download(destino)

    def download_audio(self, url_video, destino):
        self.yt = pytube.YouTube(url_video)
        self.audio = self.yt.streams.get_audio_only()
        audio_path = self.audio.download(destino)
        new_path = audio_path.replace(".mp4", ".mp3")
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(new_path)
        audio_clip.close()
        os.remove(audio_path)
