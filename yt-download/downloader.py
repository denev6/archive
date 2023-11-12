"""Download mp3 or mp4 from Youtube.

Command
  $ python downloader.py TXT EXTENSION -q QUALITY
"""

import argparse
import os
from pytube import YouTube
from pydub import AudioSegment


def save(url, file_path, format, quality=None, log=True):
    try:
        yt = YouTube(str(url))

        if format == "mp3":
            file = _get_mp3(yt)
        else:
            file = _get_mp4(yt, quality)

        out_file = file.download(output_path=file_path)

    except Exception as exp:
        print(f"Expection: {exp}")
        print("-" * 10)
        return None

    base, _ = os.path.splitext(out_file)
    new_file = "".join([base, f".{format}"])

    try:
        os.rename(out_file, new_file)
    except FileExistsError:
        new_file = "".join([base, "(1)", f".{format}"])
        os.rename(out_file, new_file)

    if log is True:
        print(f" {new_file}")

    return new_file


def _get_mp3(yt):
    audio = yt.streams.filter(only_audio=True).first()
    return audio


def _get_mp4(yt, quality):
    video_stream = yt.streams.filter(progressive=True).order_by("resolution").desc()
    if quality == "low":
        video = video_stream.last()
    else:
        # video = video_stream.first()
        video = video_stream[0]
    return video


def get_urls(file_name):
    file_path = os.path.join(CWD, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        urls = set(f.readlines())
        urls = map(lambda t: str(t).strip(), urls)
        urls = filter(
            lambda t: str(t).startswith("https://youtu.be/")
            or str(t).startswith("https://www.youtube.com/watch?v="),
            urls,
        )
        return urls


def get_q_arg(q_arg):
    if q_arg:
        q_arg = str(q_arg).strip().lower()
        if q_arg in ["high", "low"]:
            return q_arg
        else:
            print("Abnormal Video Quality Argument.")
    else:
        print("Video Quality Argument Not found.")
    exit()


def update_bitrate(file_path, bitrate="320k"):
    try:
        sound = AudioSegment.from_file(file_path)
        sound.export(file_path, format="mp3", bitrate=bitrate)
    except Exception as exp:
        print(f"Fail to update {file_path} bitrate to {bitrate}bps.")
        print(exp)


if __name__ == "__main__":
    CWD = os.getcwd()
    PATH = os.path.join(CWD, "downloaded")
    os.makedirs(PATH, exist_ok=True)

    parser = argparse.ArgumentParser(description="File Extension: mp3 or mp4")
    parser.add_argument("urls", help="*.txt includes URLs")
    parser.add_argument("extension", help="file extension")
    parser.add_argument("-q", help="Video quality: high or low")

    args = parser.parse_args()
    url_txt = str(args.urls).strip()
    ext = str(args.extension).strip().lower()

    print("Checking URLs...\n")
    URLs = get_urls(url_txt)

    print("Downloading...\n")
    if ext == "mp3":
        for url in URLs:
            file_path = save(url, PATH, "mp3")
            update_bitrate(file_path)
    elif ext == "mp4":
        quality = get_q_arg(args.q)
        for url in URLs:
            save(url, PATH, "mp4", quality)
    else:
        print("Abnormal Extension Argument.")

    print("Done!")
