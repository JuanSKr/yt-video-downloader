import pytube
from moviepy.editor import AudioFileClip
import os


class Downloader:
    def __init__(self):
        super().__init__()

    def download_video(self, url_video, destination):
        """
        Downloads a YouTube video at the highest available resolution.

        :param url_video: The URL of the YouTube video to download.
        :param destination: The path where the video will be downloaded.

        This method takes a YouTube video URL and a destination path as parameters.
        It creates a YouTube object using the provided URL, gets the stream with the highest resolution,
        and downloads the video to the provided destination.
        """
        self.yt = pytube.YouTube(url_video)
        self.video = self.yt.streams.get_highest_resolution()
        self.video.download(destination)

    def download_mp3(self, url_video, destination):
        """
        Downloads the audio from a YouTube video and converts it to MP3.

        :param url_video: The URL of the YouTube video to download audio from.
        :param destination: The path where the audio will be downloaded and the MP3 file will be saved.

        This method takes a YouTube video URL and a destination path as parameters.
        It creates a YouTube object using the provided URL, gets the audio-only stream,
        and downloads the audio to the provided destination.
        It then converts the downloaded audio to MP3 format, saves it to the same destination,
        and deletes the original downloaded file.
        """
        self.yt = pytube.YouTube(url_video)
        self.audio = self.yt.streams.get_audio_only()
        audio_path = self.audio.download(destination)
        new_path = audio_path.replace(".mp4", ".mp3")
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(new_path)
        audio_clip.close()


        os.remove(audio_path)

    def download_wav(self, url_video, destination):
        """
        Downloads the audio from a YouTube video and converts it to WAV.

        :param url_video: The URL of the YouTube video to download audio from.
        :param destination: The path where the audio will be downloaded and the WAV file will be saved.

        This method takes a YouTube video URL and a destination path as parameters.
        It creates a YouTube object using the provided URL, gets the audio-only stream,
        and downloads the audio to the provided destination.
        It then converts the downloaded audio to WAV format, saves it to the same destination,
        and deletes the original downloaded file.
        """
        self.yt = pytube.YouTube(url_video)
        self.audio = self.yt.streams.get_audio_only()
        audio_path = self.audio.download(destination)
        new_path = audio_path.replace(".mp4", ".wav")
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(new_path, codec='pcm_s16le')
        audio_clip.close()
        os.remove(audio_path)
