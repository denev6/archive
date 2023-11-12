# How To

1. List up URLSs in `*.txt` seperated in "\n".
2. Run `downloader.py` with options.

`$ python downloader.py TXT EXTENSION -q QUALITY`  

## Example

_url.txt_  
```
https://youtu.be/000
https://youtu.be/111
```

_Command_  
```bash
$ python downloader.py url.txt mp3  
$ python downloader.py url.txt mp4 -q low  
$ python downloader.py url.txt mp4 -q high
```  

# Test

```bash
$ sh test.sh
```

# Open Source

```bash
$ pip install pytube
$ pip install pydub
$ pip install ffmpeg
```
