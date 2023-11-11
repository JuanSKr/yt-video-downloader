import pytube


class Downloader:
    def __init__(self):
        super().__init__()

    def download_video(self, url_video, destino):
        self.yt = pytube.YouTube(url_video)
        self.video = self.yt.streams.get_by_resolution(resolution='720p')
        self.video.download(destino)
        print("Download completed")


if __name__ == '__main__':
    url_video = input("Enter the URL of the video: ")
    destino = input("Enter the path where you want to save the video: ")
    downloader = Downloader()
    downloader.download_video(url_video, destino)
