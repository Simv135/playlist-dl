# playlist-dl
This program reads a .csv file containing a list of songs and automatically downloads them. Simply provide the .csv file with titles and artists, and the software retrieves the corresponding tracks. Ideal for creating offline music libraries in just a few clicks.

## 📌 Requirements - **Python 3.x**
- Required packages: 'pandas', 'yt-dlp', 'colorama'

If not installed, the program will install them automatically.

## 📄 CSV File Format
The '.csv' file must contain at least two columns:
- **"Artist Name"** → Name of the artist or band
- **"Track Name"** → Song Title

### 📌 Example of 'playlist.csv'
'''csv
Artist Name,Track Name Coldplay,
Yellow Eminem,Lose Yourself
Daft Punk,One More Time
'''

## ▶️ Usage Open the terminal or command prompt and use:
'''
bash Python playlist-dl.py playlist.csv
'''

If you want to specify a destination folder for your audio files:
'''
bash python playlist-dl.py playlist.csv --output_path "/Users/Username/Music"
'''

Enjoy your offline music! 🎵🚀
