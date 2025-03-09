<<<<<<< HEAD
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, ObjectProperty
from kivy.animation import Animation
=======
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
from kivy.clock import Clock
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import json
from acrcloud.recognizer import ACRCloudRecognizer
import requests
from bs4 import BeautifulSoup
<<<<<<< HEAD
import webbrowser
import os
=======
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)

class SongTabFinder(BoxLayout):
    status_text = StringProperty("Ready to record")
    songsterr_link = StringProperty("")
    ug_link = StringProperty("")
<<<<<<< HEAD
    record_button = ObjectProperty(None)  # Reference to the button

    def __init__(self, **kwargs):
        super(SongTabFinder, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.status_label = Label(text=self.status_text, font_size=20, size_hint_y=None, height=50)
        self.add_widget(self.status_label)

        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.record_button = Button(text="Record", on_press=self.start_recording)
        self.clear_button = Button(text="Clear", on_press=self.clear_results)
        button_layout.add_widget(self.record_button)
        button_layout.add_widget(self.clear_button)
        self.add_widget(button_layout)

        spinner_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        spinner_label = Label(text="Auto-open:", size_hint_x=None, width=100)
        self.tab_source = Spinner(
            text="Off",
            values=("Off", "Songsterr", "UG"),
            size_hint_x=None,
            width=150
        )
        spinner_layout.add_widget(spinner_label)
        spinner_layout.add_widget(self.tab_source)
        self.add_widget(spinner_layout)

        # Thinking animation label
        self.thinking_label = Label(
            text="", font_size=40, size_hint_y=None, height=50, color=(0, 0.7, 0.9, 1)
        )
        self.add_widget(self.thinking_label)

        tabs_layout = BoxLayout(orientation='vertical', spacing=5)
        self.songsterr_label = Label(
            text="Songsterr: " + self.songsterr_link,
            font_size=16,
            color=(0, 0.7, 0.9, 1) if self.songsterr_link.startswith("http") else (1, 1, 1, 1)
        )
        self.ug_label = Label(
            text="UG: " + self.ug_link,
            font_size=16,
            color=(0, 0.7, 0.9, 1) if self.ug_link.startswith("http") else (1, 1, 1, 1)
        )
        tabs_layout.add_widget(self.songsterr_label)
        tabs_layout.add_widget(self.ug_label)
        self.add_widget(tabs_layout)

        self.songsterr_label.bind(on_touch_down=self.open_songsterr_url)
        self.ug_label.bind(on_touch_down=self.open_ug_url)

        # Animation setup
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']  # Spinning chars
        self.spinner_event = None
=======
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)

    def record_audio(self, duration=5, sample_rate=44100):
        try:
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()
            return audio.flatten()
        except Exception as e:
<<<<<<< HEAD
            print(f"Error recording audio: {e}")
=======
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
            return None

    def save_audio(self, audio, sample_rate=44100):
        if audio is not None:
<<<<<<< HEAD
            temp_dir = os.path.join(os.path.expanduser("~"), "SongTabFinder")
            os.makedirs(temp_dir, exist_ok=True)
            audio_file = os.path.join(temp_dir, "temp_recording.wav")
            write(audio_file, sample_rate, audio)
            return audio_file
=======
            write('temp_recording.wav', sample_rate, audio)
            return 'temp_recording.wav'
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
        return None

    def identify_song(self, audio_file):
        config = {
            'host': 'identify-us-west-2.acrcloud.com',
            'access_key': '3ebe28971e7fd6561cc91d9c10a67283',
            'access_secret': '4mtioPufwFF90vUv4R5HpF5ZS3GphuEdKNBX2A45',
            'timeout': 10
        }
        try:
            recognizer = ACRCloudRecognizer(config)
            result = recognizer.recognize_by_file(audio_file, 0)
<<<<<<< HEAD
            print(f"ACRCloud Raw Response: {result}")
=======
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
            parsed_result = json.loads(result)
            if parsed_result.get('status', {}).get('code') == 0:
                title = parsed_result['metadata']['music'][0]['title']
                artist = parsed_result['metadata']['music'][0]['artists'][0]['name']
<<<<<<< HEAD
                print(f"ACRCloud Identified: {title} by {artist}")
                return parsed_result
            else:
                print("ACRCloud failed to identify song")
                return None
        except Exception as e:
            print(f"Error identifying song: {e}")
=======
                return parsed_result
            return None
        except Exception:
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
            return None

    def get_tabs(self, song_title, artist):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
<<<<<<< HEAD
        print(f"Fetching tabs for: {song_title} by {artist}")
=======
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
        ug_url = None
        songsterr_url = None

        try:
            query = f"{song_title} {artist}".replace(" ", "+")
            ug_url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={query}"
<<<<<<< HEAD
            print(f"UG search page: {ug_url}")
            if self.tab_source.text == "UG":
                self.open_url(ug_url)
                print("UG search page opened!")
        except Exception as e:
            print(f"UG Error: {e}")
=======
            if self.ids.tab_source.text == "UG":
                webbrowser.open(ug_url)
        except Exception:
            pass
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)

        try:
            query = f"{song_title} {artist}".replace(" ", "+")
            url = f"https://www.songsterr.com/?pattern={query}"
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            tab_links = soup.select('a[href*="/a/wsa/"]')
            for link in tab_links:
                link_text = link.get_text().lower()
                link_href = link['href'].lower()
<<<<<<< HEAD
                title_match = song_title.lower() in link_text or song_title.lower() in link_href
                artist_match = artist.lower() in link_text or artist.lower() in link_href
                if title_match and artist_match:
                    songsterr_url = "https://www.songsterr.com" + link['href']
                    print(f"Songsterr Found: {songsterr_url}")
                    if self.tab_source.text == "Songsterr":
                        self.open_url(songsterr_url)
                        print("Songsterr tab opened!")
                    break
            else:
                print("No matching Songsterr tabs found for this artist and title")
                songsterr_url = "No Songsterr tabs found for this artist."
        except Exception as e:
            print(f"Songsterr Error: {e}")
=======
                if (song_title.lower() in link_text or artist.lower() in link_text or
                    song_title.lower() in link_href or artist.lower() in link_href):
                    songsterr_url = "https://www.songsterr.com" + link['href']
                    if self.ids.tab_source.text == "Songsterr":
                        webbrowser.open(songsterr_url)
                    break
            else:
                songsterr_url = "No Songsterr tabs found."
        except Exception:
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
            songsterr_url = "No tabs available."

        return songsterr_url, ug_url

<<<<<<< HEAD
    def start_spinner(self):
        self.record_button.disabled = True  # "Stays down" effect
        self.record_button.text = "Recording..."
        self.spinner_idx = 0
        self.spinner_event = Clock.schedule_interval(self.update_spinner, 0.1)

    def update_spinner(self, dt):
        self.thinking_label.text = self.spinner_chars[self.spinner_idx]
        self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)

    def stop_spinner(self):
        if self.spinner_event:
            self.spinner_event.cancel()
            self.spinner_event = None
        self.thinking_label.text = ""
        self.record_button.disabled = False
        self.record_button.text = "Record"

    def start_recording(self, instance):
        self.start_spinner()  # Show feedback
        Clock.schedule_once(self._record_and_process, 0.1)  # Async to let UI update

    def _record_and_process(self, dt):
=======
    def start_recording(self, instance):
        self.status_text = "Recording..."
        Clock.schedule_once(self._record_and_identify, 0)

    def _record_and_identify(self, dt):
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
        audio = self.record_audio()
        if audio is not None:
            audio_file = self.save_audio(audio)
            if audio_file:
<<<<<<< HEAD
=======
                self.status_text = "Identifying..."
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
                song_info = self.identify_song(audio_file)
                if song_info and song_info.get('status', {}).get('code') == 0:
                    title = song_info['metadata']['music'][0]['title']
                    artist = song_info['metadata']['music'][0]['artists'][0]['name']
                    self.status_text = f"{title} by {artist}"
                    songsterr_url, ug_url = self.get_tabs(title, artist)
                    self.songsterr_link = songsterr_url
                    self.ug_link = ug_url
<<<<<<< HEAD
                    self.update_link_colors()
=======
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
                else:
                    self.status_text = "Couldn’t identify song"
                    self.clear_links()
            else:
                self.status_text = "Failed to save audio"
                self.clear_links()
        else:
            self.status_text = "Recording failed"
            self.clear_links()
<<<<<<< HEAD
        self.status_label.text = self.status_text
        self.stop_spinner()  # Reset UI

    def clear_results(self, instance):
        self.status_text = "Ready to record"
        self.status_label.text = self.status_text
=======

    def clear_results(self, instance):
        self.status_text = "Ready to record"
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)
        self.clear_links()

    def clear_links(self):
        self.songsterr_link = ""
        self.ug_link = ""
<<<<<<< HEAD
        self.songsterr_label.text = "Songsterr: " + self.songsterr_link
        self.ug_label.text = "UG: " + self.ug_link
        self.songsterr_label.color = (1, 1, 1, 1)
        self.ug_label.color = (1, 1, 1, 1)

    def update_link_colors(self):
        self.songsterr_label.text = "Songsterr: " + self.songsterr_link
        self.ug_label.text = "UG: " + self.ug_link
        self.songsterr_label.color = (0, 0.7, 0.9, 1) if self.songsterr_link.startswith("http") else (1, 1, 1, 1)
        self.ug_label.color = (0, 0.7, 0.9, 1) if self.ug_link.startswith("http") else (1, 1, 1, 1)

    def open_url(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening URL: {e}")

    def open_songsterr_url(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.songsterr_link.startswith("http"):
            self.open_url(self.songsterr_link)

    def open_ug_url(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.ug_link.startswith("http"):
            self.open_url(self.ug_link)
=======

    def open_songsterr_url(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.songsterr_link.startswith("http"):
            webbrowser.open(self.songsterr_link)

    def open_ug_url(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.ug_link.startswith("http"):
            webbrowser.open(self.ug_link)

    def open_donate(self, instance):
        webbrowser.open("https://www.paypal.me/jbfiresteels")
>>>>>>> 6b40076 (Initial commit: SongTabFinder with clean code, wrapped links, Donate at bottom)

class SongTabFinderApp(App):
    def build(self):
        return SongTabFinder()

if __name__ == '__main__':
    SongTabFinderApp().run()