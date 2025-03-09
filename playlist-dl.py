import sys, subprocess, os, time, random, argparse, platform
packages = ["pandas", "yt-dlp", "colorama"]

while True:
    try:
        import pandas
        import yt_dlp
        from colorama import init, Fore, Style
        init(autoreset=True)
        break
    except ImportError as e:
        missing_package = str(e).split("'")[1]
        print(f"Missing package: {missing_package}. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", missing_package])

def print_info(message):
    print(Fore.GREEN + message)

def print_warning(message):
    print(Fore.YELLOW + message)

def print_error(message):
    print(Fore.RED + message)

def print_progress(message):
    print(Fore.CYAN + message)

def load_csv(file_path):
    try:
        data = pandas.read_csv(file_path)
        print_info(f"CSV file loaded successfully: {file_path}")
        return data
    except Exception as e:
        print_error(f"Error loading the CSV file: {e}")
        raise

def validate_csv_columns(data):
    columns = {col.lower(): col for col in data.columns}
    artist_col = columns.get("artist name(s)") or columns.get("artist name")
    track_col = columns.get("track name")
    
    if not artist_col or not track_col:
        print_error("Missing 'Artist Name' and 'Track Name' columns in the CSV file.")
        raise ValueError("Missing necessary columns in the CSV file.")
    
    return artist_col, track_col

def download_audio(video_url, title, artist, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, f'{artist} - {title}.webm'),
        'quiet': True,
        'throttled-rate': '500K',
        'sleep-interval': 3,
        'max-sleep-interval': 10,
        'retries': 3,
        'logtostderr': False,
        'progress_hooks': [],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print_info("Track downloaded successfully!")
        return True
    except Exception as e:
        print_error("Error downloading the track!")
        return False

def search_on_youtube(artist, title):
    search_query = f"{title} {artist}"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if 'entries' in result and result['entries']:
                return f"https://www.youtube.com/watch?v={result['entries'][0]['id']}"
            else:
                print_warning(f"Track {artist} - {title} not found.")
    except Exception as e:
        print_error(f"Error during track search: {e}")
    return None

def get_music_folder():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get("USERPROFILE", ""), "Music")
    elif system == "Linux":
        xdg_dirs_file = os.path.expanduser("~/.config/user-dirs.dirs")
        music_folder = os.path.join(os.path.expanduser("~"), "Music")
        if os.path.exists(xdg_dirs_file):
            with open(xdg_dirs_file, "r", encoding="utf-8") as f:
                for line in f:
                    if "XDG_MUSIC_DIR" in line:
                        return line.split("=")[1].strip().strip('"').replace("$HOME", os.path.expanduser("~"))
    else:
        raise Exception(f"Operating system {system} not supported")

def main(file_path, output_path):
    try:
        data = load_csv(file_path)
        artist_col, track_col = validate_csv_columns(data)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print_info(f"Folder {output_path} created.")
        
        for _, row in data.iterrows():
            artist = row[artist_col].replace('/', '-').replace('\\', '-')
            title = row[track_col].replace('/', '-').replace('\\', '-')
            
            file_path = os.path.join(output_path, f"{artist} - {title}.webm")
            if os.path.exists(file_path):
                continue

            print_info("-------------------------------")
            video_url = search_on_youtube(artist, title)
            
            if video_url:
                print_progress(f"Downloading: {artist} - {title}")
                download_audio(video_url, title, artist, output_path)
            
            time.sleep(random.uniform(2, 5))
    except KeyboardInterrupt:
        print_warning("\nDownload interrupted by the user.")
    except Exception as e:
        print_error(f"Error in the download process: {e}")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Download music from a playlist')
        parser.add_argument('file_path', type=str, help='Path to the CSV file with tracks to download')
        parser.add_argument('--output_path', type=str, help='Folder to save the tracks')
        args = parser.parse_args()

        file_path = args.file_path
        output_path = args.output_path if args.output_path else get_music_folder()
        main(file_path, output_path)
    except KeyboardInterrupt:
        print_info("\nDownload interrupted by the user.")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
