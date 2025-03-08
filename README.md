# playlist-dl
This program reads a .csv file containing a list of songs and automatically downloads them. Simply provide the .csv file with titles and artists, and the software retrieves the corresponding tracks. Ideal for creating offline music libraries in just a few clicks.

## 📌 Installation
- Requirements: Python 3.x

Open the terminal or command prompt and use:
```bash
curl -o playlist-dl.py https://gist.githubusercontent.com/Simv135/391ce0c1bed736d6b7c56853b05bf3b3/raw/44ea5df20d3edab6d4c63b0e92415b93558f2508/playlist-dl.py
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
rm playlist-dl.py && pip uninstall pandas yt-dlp colorama
```
