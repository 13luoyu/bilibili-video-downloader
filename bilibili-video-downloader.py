import requests
from moviepy.editor import *
from bs4 import BeautifulSoup
import re
import os


def get_data_and_merge(title, video_url, audio_url):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44",
        "Referer":"https://www.bilibili.com/video/BV1uQ4y1k7G4?p=2&vd_source=e451850282ff73c07332cc6cd961137e"
    }
    response_video = requests.get(video_url, headers=header)
    response_audio = requests.get(audio_url, headers=header)
    data_video = response_video.content
    data_audio = response_audio.content

    with open('video.mp4', 'wb') as f:
        f.write(data_video)
    with open('audio.mp3', 'wb') as f:
        f.write(data_audio)

    video = VideoFileClip("video.mp4")
    audio = AudioFileClip("audio.mp3")
    video = video.set_audio(audio)
    video.write_videofile(title + ".mp4")
    os.remove("video.mp4")
    os.remove("audio.mp3")


def get_name_and_audio_video_url(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44",
        "Reference":"https://www.baidu.com/link?url=Hfx-FhfdpjzGHgKNLj0cwNUklbA4YxnB4saeepCciOUprUvbxaFK0qu2hqhAaOKjxROa-otozIClS1dHnOhMK_&wd=&eqid=c3f30fba00024b910000000362b174ca",

    }
    response = requests.get(url, headers=headers)
    html = response.text
    page = BeautifulSoup(html, features="html.parser")
    title_tag = page.find_all("title")[0]
    title = title_tag.text
    title = title.replace("_哔哩哔哩_bilibili", "")

    tags = page.find_all("script")
    a_v = ""
    for tag in tags:
        if "window.__playinfo" in tag.text:
            a_v = tag.text
            break
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)",', a_v)[0]
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)",', a_v)[0]

    return title, video_url, audio_url

def run():
    url = input("请输入哔哩哔哩视频地址：")
    title, video, audio = get_name_and_audio_video_url(url)
    get_data_and_merge(title, video, audio)

run()