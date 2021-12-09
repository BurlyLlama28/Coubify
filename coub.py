import requests, urllib.request, os


class Coub():
    def __init__(self):
        self.error = "Oops, we have error"

    def download_video(self, url, path):
        url = url.replace("https://coub.com/view/",
                          "http://coub.com/api/v2/coubs/")

        # get api-url
        data = requests.get(url).json()
        video_link = data["file_versions"]["html5"]["video"]["higher"]["url"]
        title = data["id"]

        # download video
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        video = opener.open(video_link)

        # save file
        try:
            os.mkdir(path)
        except:
            pass
        with open(f"{path}{title}.mp4", 'wb') as file:
            file.write(b'\x00\x00' + video.read()[2:])


if __name__ == "__main__":
    coub = Coub()
    coub.download_video("https://coub.com/view/2xkael", "./coubs/")