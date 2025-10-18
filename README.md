# [playlist-dl](https://raw.githubusercontent.com/Simv135/playlist-dl/refs/heads/main/playlist-dl.py)
This program reads a .csv file containing a list of songs and automatically downloads them. Simply provide the .csv file with titles and artists, and the software retrieves the corresponding tracks. Ideal for creating offline music libraries in just a few clicks.

![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/Simv135/playlist-dl/latest/total)

## 📌 Requirements
- Python 3.x

For Windows:

https://www.python.org/downloads/windows/

For Linux:
```bash
sudo apt install python3-pip -y && sudo apt update
```

## 📦 Installation

For the **GUI version** simply download the ["playlist-dl-gui.py"](https://github.com/Simv135/playlist-dl/releases/tag/auto-updated) file and open it with Python

For the **Console version** open the terminal or command prompt and use:
```bash
curl -o playlist-dl.py https://raw.githubusercontent.com/Simv135/playlist-dl/refs/heads/main/playlist-dl.py
```

## 📄 CSV File Format
The '.csv' file must contain at least two columns:
- **"Artist Name"** → Name of the artist or band
- **"Track Name"** → Song Title

### Example of '.csv' file

| Artist Name  | Track Name |
| ------------- | ------------- |
| Coldplay  | Yellow  |
| Eminem  | Lose Yourself  |
| Daft Punk  | One More Time  |

```csv
Artist Name,Track Name
Coldplay,Yellow
Eminem,Lose Yourself
Daft Punk,One More Time
```

## ▶️ Usage (Console version)
Open the terminal or command prompt and use:

For Windows:
```bash
python playlist-dl.py "/my_path/my_playlist.csv"
```
For Linux:
```bash
python3 playlist-dl.py "/my_path/my_playlist.csv"
```

If you want to specify a destination folder for your audio files:

For Windows:
```bash
python playlist-dl.py "/my_path/my_playlist.csv" --output_path "/my_path/Music"
```
For Linux:
```bash
python3 playlist-dl.py "/my_path/my_playlist.csv" --output_path "/my_path/Music"
```

## 🚨 Uninstallation

For the **GUI version** delete the file "playlist-dl-gui.py", open the terminal or command prompt and use:
```bash
pip uninstall pandas yt-dlp requests -y
```

For the **Console version** open the terminal or command prompt and use:

For Windows:
```bash
del playlist-dl.py && pip uninstall pandas yt-dlp colorama requests -y
```
For Linux:
```bash
rm playlist-dl.py && pip uninstall pandas yt-dlp colorama requests -y
```
