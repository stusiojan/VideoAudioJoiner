import os 
import subprocess 
from pathlib import Path 
import logging 
 
logging.basicConfig(filename='conversion_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s') 
 
def join_audio_video(): 
    base_dir = Path("CONTENTS_imprezy") 
    video_dir = base_dir / "VIDEO" 
    audio_dir = base_dir / "AUDIO" 
    output_dir = base_dir / "MP4" 
 
    output_dir.mkdir(exist_ok=True) 
 
    for video_file in video_dir.glob("*.MXF"): 
        video_name = video_file.stem 
        output_file = output_dir / f"{video_name}.mp4" 
 
        audio_files = sorted(audio_dir.glob(f"{video_name}[0-9][0-9].MXF")) 
 
        if not audio_files: 
            logging.warning(f"No audio files found for {video_name}") 
            continue 
 
        cmd = [ 
            "ffmpeg", 
            "-i", str(video_file) 
        ] 
 
        for audio_file in audio_files: 
            cmd.extend(["-i", str(audio_file)]) 
 
        cmd.extend([ 
            "-map", "0:v" 
        ]) 
 
        for i in range(len(audio_files)): 
            cmd.extend(["-map", f"{i+1}:a"]) 
 
        cmd.extend([ 
            "-c:v", "libx264", 
            "-preset", "medium", 
            "-crf", "23", 
            "-c:a", "aac", 
            "-b:a", "128k", 
            "-y", 
            str(output_file) 
        ]) 
 
        try: 
            print(f"Processing {video_name}...") 
            result = subprocess.run(cmd, check=True, capture_output=True, text=True) 
            logging.info(f"Successfully processed {video_name}") 
            print(f"Completed {video_name}") 
        except subprocess.CalledProcessError as e: 
            logging.error(f"Error processing {video_name}: {e}") 
            logging.error(f"ffmpeg stdout: {e.stdout}") 
            logging.error(f"ffmpeg stderr: {e.stderr}") 
            print(f"Error processing {video_name}. Check log for details.") 
        except Exception as e: 
            logging.error(f"Unexpected error processing {video_name}: {e}") 
            print(f"Unexpected error processing {video_name}. Check log for details.") 
 
def check_ffmpeg_version(): 
    try: 
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True) 
        print(f"ffmpeg version: {result.stdout.split()[2]}") 
    except subprocess.CalledProcessError as e: 
        print(f"Error checking ffmpeg version: {e}") 

if __name__ == "__main__":
    check_ffmpeg_version()
    join_audio_video() 
