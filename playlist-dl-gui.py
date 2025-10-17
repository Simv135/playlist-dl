import sys, subprocess, os, time, random, platform, hashlib, threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import urllib.request
from io import StringIO

class PackageInstallerGUI:
    def __init__(self, root, packages):
        self.root = root
        self.root.title("Installing Required Packages")
        self.root.geometry("500x200")
        self.root.resizable(False, False)
        self.packages = packages
        self.current_package = tk.StringVar()
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Installing required packages...", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 20))
        
        ttk.Label(main_frame, textvariable=self.current_package).grid(row=1, column=0, pady=5)
        
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(main_frame, text="Starting installation...")
        self.status_label.grid(row=3, column=0, pady=5)
        
        self.root.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def install_packages(self):
        def run_installation():
            total = len(self.packages)
            for i, package in enumerate(self.packages):
                self.current_package.set(f"Installing: {package}")
                self.progress['value'] = (i / total) * 100
                self.status_label.config(text=f"Installing {package}...")
                
                try:
                    # Try to import first to check if already installed
                    if package == "yt-dlp":
                        __import__("yt_dlp")
                    else:
                        __import__(package)
                    self.status_label.config(text=f"{package} already installed")
                except ImportError:
                    try:
                        # Install the package
                        subprocess.check_call([
                            sys.executable, "-m", "pip", "install", package
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        self.status_label.config(text=f"Successfully installed {package}")
                    except subprocess.CalledProcessError:
                        self.status_label.config(text=f"Failed to install {package}")
                        return False
                
                time.sleep(0.5)
            
            self.progress['value'] = 100
            self.status_label.config(text="All packages installed successfully!")
            time.sleep(1)
            self.root.quit()
            return True
            
        thread = threading.Thread(target=run_installation)
        thread.daemon = True
        thread.start()

# Check and install packages with GUI
required_packages = ["pandas", "yt-dlp", "requests"]
missing_packages = []

for package in required_packages:
    try:
        if package == "yt-dlp":
            __import__("yt_dlp")
        else:
            __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    root = tk.Tk()
    installer = PackageInstallerGUI(root, missing_packages)
    root.after(100, installer.install_packages)
    root.mainloop()
    root.destroy()

# Now import the successfully installed packages
import pandas, requests, yt_dlp

class PlaylistDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playlist Downloader")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        # Variables
        self.file_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.is_downloading = False
        self.download_thread = None
        self.current_progress = 0
        self.total_tracks = 0
        self.processed_tracks = 0
        
        # Set default output path
        self.output_path.set(self.get_music_folder())
        
        # Check for restart after update
        self.check_restart_flag()
        
        self.setup_ui()
        
    def check_restart_flag(self):
        """Check if we just restarted after an update"""
        restart_flag = "update_flag.txt"
        if os.path.exists(restart_flag):
            os.remove(restart_flag)
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Playlist Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # CSV File Selection
        ttk.Label(main_frame, text="CSV File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.file_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=1, column=2, pady=5)
        
        # Output Folder Selection
        ttk.Label(main_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=2, column=2, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.download_button = ttk.Button(button_frame, text="Start Download", 
                                         command=self.toggle_download)
        self.download_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Check for Updates", 
                  command=self.check_updates).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Download Progress", padding="5")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(1, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Progress labels
        self.progress_label = ttk.Label(progress_frame, text="Ready")
        self.progress_label.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        
        self.percentage_label = ttk.Label(progress_frame, text="0%")
        self.percentage_label.grid(row=1, column=2, sticky=tk.E)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to start download")
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Download Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, width=80, height=20, 
                                                 state=tk.DISABLED, wrap=tk.WORD)
        self.log_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored logging
        self.log_area.tag_config("info", foreground="green")
        self.log_area.tag_config("warning", foreground="orange")
        self.log_area.tag_config("error", foreground="red")
        self.log_area.tag_config("progress", foreground="blue")
        
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path.set(folder)
            
    def toggle_download(self):
        if not self.is_downloading:
            self.start_download()
        else:
            self.stop_download()
            
    def start_download(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a CSV file")
            return
            
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("Error", "Selected CSV file does not exist")
            return
            
        self.is_downloading = True
        self.download_button.config(text="Stop Download")
        self.status_label.config(text="Downloading...")
        self.current_progress = 0
        self.processed_tracks = 0
        self.update_progress(0, 0, 0)
        
        # Start download in a separate thread
        self.download_thread = threading.Thread(target=self.download_process)
        self.download_thread.daemon = True
        self.download_thread.start()
        
    def stop_download(self):
        self.is_downloading = False
        self.download_button.config(text="Start Download")
        self.status_label.config(text="Download stopped by user")
        self.log_message("Download stopped by user", "warning")
        
    def download_process(self):
        try:
            self.main(self.file_path.get(), self.output_path.get())
        except Exception as e:
            self.log_message(f"Unexpected error: {e}", "error")
        
        # Reset UI when done
        self.root.after(0, self.download_finished)
        
    def download_finished(self):
        self.is_downloading = False
        self.download_button.config(text="Start Download")
        self.status_label.config(text="Download finished")
        
    def log_message(self, message, msg_type="info"):
        self.root.after(0, self._update_log, message, msg_type)
        
    def _update_log(self, message, msg_type):
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{formatted_message}\n", msg_type)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        
    def update_progress(self, value, current, total):
        self.root.after(0, self._update_progress_ui, value, current, total)
        
    def _update_progress_ui(self, value, current, total):
        self.progress_bar['value'] = value
        self.percentage_label.config(text=f"{value:.1f}%")
        
        if total > 0:
            self.progress_label.config(text=f"Processed: {current}/{total} tracks")
        else:
            self.progress_label.config(text="Processing...")
        
    def clear_log(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)
        
    def check_updates(self):
        self.log_message("Checking for updates...", "info")
        threading.Thread(target=self.update, daemon=True).start()
        
    def update(self):
        url = "https://raw.githubusercontent.com/Simv135/playlist-dl/refs/heads/main/playlist-dl-gui.py"
        file_locale = "playlist-dl-gui.py"
        restart_flag = "update_flag.txt"

        try:
            # Create update dialog
            update_window = tk.Toplevel(self.root)
            update_window.title("Update Check")
            update_window.geometry("400x150")
            update_window.resizable(False, False)
            update_window.transient(self.root)
            update_window.grab_set()
            
            # Center the window
            update_window.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() - update_window.winfo_width()) // 2
            y = self.root.winfo_y() + (self.root.winfo_height() - update_window.winfo_height()) // 2
            update_window.geometry(f"+{x}+{y}")
            
            ttk.Label(update_window, text="Checking for updates...", 
                     font=("Arial", 10, "bold")).pack(pady=10)
            
            progress_bar = ttk.Progressbar(update_window, mode='indeterminate')
            progress_bar.pack(fill=tk.X, padx=20, pady=10)
            progress_bar.start()
            
            status_label = ttk.Label(update_window, text="Connecting to server...")
            status_label.pack(pady=5)
            
            def update_status(text):
                status_label.config(text=text)
                update_window.update()
            
            update_window.update()
            
            # Check current file content
            current_content = ""
            if os.path.exists(file_locale):
                with open(file_locale, 'r', encoding='utf-8') as local_file:
                    current_content = local_file.read()
            
            update_status("Downloading update...")
            
            # Download remote content
            response = requests.get(url)
            response.raise_for_status()
            remote_content = response.text
            
            # Compare content using hash
            current_hash = hashlib.sha256(current_content.encode('utf-8')).hexdigest()
            remote_hash = hashlib.sha256(remote_content.encode('utf-8')).hexdigest()
            
            if current_hash == remote_hash:
                update_status("No updates available.")
                progress_bar.stop()
                self.log_message("No updates available - already up to date.", "info")
                time.sleep(2)
                update_window.destroy()
                return  # Esce senza riavviare
            
            update_status("Update found! Installing...")
            
            # Write the updated file
            with open(file_locale, 'w', encoding='utf-8') as local_file:
                local_file.write(remote_content)

            # Create restart flag
            with open(restart_flag, 'w') as flag_file:
                flag_file.write("restart_after_update")

            update_status("Update completed! Restarting...")
            self.log_message("Update completed. Restarting application...", "info")
            
            time.sleep(2)
            update_window.destroy()
            
            # Restart the application ONLY if there was an actual update
            python = sys.executable
            os.execl(python, python, *sys.argv)

        except requests.RequestException as e:
            self.log_message(f"Error during update: {e}", "error")
            if 'update_window' in locals():
                update_window.destroy()
        except Exception as e:
            self.log_message(f"Error during update: {e}", "error")
            if 'update_window' in locals():
                update_window.destroy()

    def get_music_folder(self):
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
            return music_folder
        else:
            return os.path.expanduser("~")

    def load_csv(self, file_path):
        try:
            data = pandas.read_csv(file_path)
            self.log_message(f"File loaded successfully: {file_path}", "info")
            return data
        except Exception as e:
            self.log_message(f"Error loading the CSV file: {e}", "error")
            raise

    def validate_csv_columns(self, data):
        columns = {col.lower().replace(" ", ""): col for col in data.columns}

        artist_col = columns.get("artistname(s)") or columns.get("artistname") or columns.get("artist")
        track_col = columns.get("trackname") or columns.get("track") or columns.get("song")
        
        if not artist_col or not track_col:
            self.log_message("Missing 'Artist Name' and/or 'Track Name' columns in the CSV file.", "error")
            raise ValueError("Missing necessary columns in the CSV file.")
        
        return artist_col, track_col

    def download_audio(self, video_url, title, artist, output_path):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, f'{artist} - {title}.%(ext)s'),
            'quiet': True,
            'throttled-rate': '500K',
            'sleep-interval': 3,
            'max-sleep-interval': 10,
            'retries': 3,
            'logtostderr': False,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            self.log_message(f"Downloaded: {artist} - {title}", "info")
            return True
        except Exception as e:
            self.log_message(f"Error downloading: {artist} - {title} - {e}", "error")
            return False

    def search_on_youtube(self, artist, title):
        search_query = f"{title} {artist} audio"
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
                if 'entries' in result and result['entries']:
                    return f"https://www.youtube.com/watch?v={result['entries'][0]['id']}"
                else:
                    self.log_message(f"Track not found: {artist} - {title}", "warning")
        except Exception as e:
            self.log_message(f"Error searching: {artist} - {title} - {e}", "error")
        return None

    def main(self, file_path, output_path):
        try:
            data = self.load_csv(file_path)
            artist_col, track_col = self.validate_csv_columns(data)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                self.log_message(f"Folder created: {output_path}", "info")
            
            self.total_tracks = len(data)
            successful_downloads = 0
            
            for i, (_, row) in enumerate(data.iterrows()):
                if not self.is_downloading:
                    break
                    
                artist = str(row[artist_col]).replace('/', '-').replace('\\', '-')
                title = str(row[track_col]).replace('/', '-').replace('\\', '-')
                
                # Check if file already exists (various extensions)
                existing_files = [
                    os.path.join(output_path, f"{artist} - {title}.webm"),
                    os.path.join(output_path, f"{artist} - {title}.mp3"),
                    os.path.join(output_path, f"{artist} - {title}.m4a"),
                ]
                
                if any(os.path.exists(f) for f in existing_files):
                    self.log_message(f"Already exists: {artist} - {title}", "info")
                    self.processed_tracks += 1
                    progress = (self.processed_tracks / self.total_tracks) * 100
                    self.update_progress(progress, self.processed_tracks, self.total_tracks)
                    continue

                self.log_message("-------------------------------", "info")
                self.log_message(f"Searching: {artist} - {title}", "progress")
                
                video_url = self.search_on_youtube(artist, title)#
                
                if video_url:
                    self.log_message(f"Downloading: {artist} - {title}", "progress")
                    if self.download_audio(video_url, title, artist, output_path):
                        successful_downloads += 1
                
                self.processed_tracks += 1
                progress = (self.processed_tracks / self.total_tracks) * 100
                self.update_progress(progress, self.processed_tracks, self.total_tracks)
                
                if self.is_downloading:
                    time.sleep(random.uniform(1, 3))
            
            self.log_message(f"Download completed! Successful: {successful_downloads}/{self.total_tracks}", "info")
                    
        except Exception as e:
            self.log_message(f"Error in main process: {e}", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistDownloaderGUI(root)
    root.mainloop()
