import yt_dlp
from pydub import AudioSegment ##for chunking
import os

DOWNLOAD_DIRECTORY="downloads"
os.makedirs(DOWNLOAD_DIRECTORY,exist_ok=True)

## generate using ai
##for youtube
def download_youtube_audio(url:str)->str:
    output_path = os.path.join(DOWNLOAD_DIRECTORY, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


##convert wav file to desired form that is convert to mono make freq 16 hz as it is suitable for whisper ai
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz ##sets channel converts to monoaudio
    audio.export(output_path, format="wav")
    return output_path


##converting audio to chunks so that each chunk is of 10min so that whisper ai can process chunks
def chunk_audio(wav_path:str,chunk_minutes:int=10) -> list:
    ##returns list of chunked path saved in downloads itself

    audio=AudioSegment.from_wav(wav_path) ##loading audio file

    chunk_ms= chunk_minutes*60*1000 ##milli seconds

    chunks=[]

    for i,start in enumerate(range(0,len(audio),chunk_ms)):
        chunk=audio[start: start+chunk_ms] ##go from start to chunkms size
        chunk_path=f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path,format="wav") ## to save the audio file
        chunks.append(chunk_path)

    return chunks


## to just trigger all above functions
def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks

# output=download_youtube_audio("https://www.youtube.com/watch?v=k2P_pHQDlp0&t=8s")
# print(convert_to_wav(output))