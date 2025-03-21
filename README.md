# [playlist-dl](https://raw.githubusercontent.com/Simv135/playlist-dl/refs/heads/main/playlist-dl.py)
This program reads a .csv file containing a list of songs and automatically downloads them. Simply provide the .csv file with titles and artists, and the software retrieves the corresponding tracks. Ideal for creating offline music libraries in just a few clicks.

## 📌 Installation
- Requirements: Python 3.x

Open the terminal or command prompt and use:
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

## ▶️ Usage
Open the terminal or command prompt and use:
```bash
python3 playlist-dl.py "/my_path/my_playlist.csv"
```

If you want to specify a destination folder for your audio files:
```bash
python3 playlist-dl.py "/my_path/my_playlist.csv" --output_path "/my_path/Music"
```

## 🚨 Uninstallation
```bash
rm playlist-dl.py && pip uninstall pandas yt-dlp colorama requests
```
