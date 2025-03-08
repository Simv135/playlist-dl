# playlist-dl
This program reads a .csv file containing a list of songs and automatically downloads them. Simply provide the .csv file with titles and artists, and the software retrieves the corresponding tracks. Ideal for creating offline music libraries in just a few clicks.

## 📌 Requirements


## 📌 Installation
- Requirements: Python 3.x

Open the terminal or command prompt and use:
```bash
curl -o playlist-dl.py https://gist.githubusercontent.com/Simv135/bd2ab20b1ea59c817c266536f547e8d2/raw/15fc63887cdf70b3de99460dc60ed8ba89b33af3/playlist-dl
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
python playlist-dl.py my_playlist.csv
```

If you want to specify a destination folder for your audio files:
```bash
python playlist-dl.py my_playlist.csv --output_path "/Users/Username/Music"
```

## 🚨 Uninstallation
```bash
rm playlist-dl.py && pip uninstall pandas yt-dlp colorama
```
