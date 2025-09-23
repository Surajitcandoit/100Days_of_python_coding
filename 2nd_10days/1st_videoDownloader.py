import yt_dlp

url = "https://youtube.com/shorts/i-dpilfoRRw?si=K0ezHfyuSgcy1-Jm"
ydl_opts = {'outtmpl': 'video.%(ext)s', 'format': 'bestvideo+bestaudio/best'}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
