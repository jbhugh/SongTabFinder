import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
import numpy as np
from scipy.io.wavfile import write
import json
from acrcloud.recognizer import ACRCloudRecognizer
import requests
from bs4 import BeautifulSoup
import platform
import os
import threading
import time

# Platform-specific imports
if platform.system() == "Windows":
    import sounddevice as sd
elif platform.system() == "Linux" and "ANDROID_ARGUMENT" in os.environ:
    from jnius import autoclass
    AudioRecord = autoclass('android.media.AudioRecord')
    MediaRecorder = autoclass('android.media.MediaRecorder$AudioSource')
    AudioFormat = autoclass('android.media.AudioFormat')

class SongTabFinder(BoxLayout):
    status_text = StringProperty("Ready to record")
    songsterr_link = StringProperty("")
    ug_link = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recording = False
        self.audio_data = []
        self.recorder = None  # For Android

    def record_audio(self, duration=5, sample_rate=44100):
        self.audio_data = []  # Reset audio data
        if platform.system() == "Windows":
            try:
                audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
                sd.wait()
                return audio.flatten()
            except Exception:
                return None
        elif platform.system() == "Linux" and "ANDROID_ARGUMENT" in os.environ:
            try:
                # Android audio setup
                channel_config = AudioFormat.CHANNEL_IN_MONO
                audio_format = AudioFormat.ENCODING_PCM_16BIT
                buffer_size = AudioRecord.getMinBufferSize(sample_rate, channel_config, audio_format)
                self.recorder = AudioRecord(
                    MediaRecorder.MIC,
                    sample_rate,
                    channel_config,
                    audio_format,
                    buffer_size
                )
                self.recording = True
                self.recorder.startRecording()
                start_time = time.time()
                while time.time() - start_time < duration and self.recording:
                    audio_buffer = bytearray(buffer_size)
                    bytes_read = self.recorder.read(audio_buffer, 0, buffer_size)
                    if bytes_read > 0:
                        # Convert bytes to float32 for consistency with sounddevice
                        int16_data = np.frombuffer(audio_buffer[:bytes_read], dtype=np.int16)
                        float32_data = int16_data.astype(np.float32) / 32768.0
                        self.audio_data.extend(float32_data)
                    time.sleep(0.01)
                self.recorder.stop()
                self.recorder.release()
                self.recording = False
                return np.array(self.audio_data)
            except Exception as e:
                print(f"Android recording error: {e}")
                self.recording = False
                if self.recorder:
                    self.recorder.release()
                return None

    def save_audio(self, audio, sample_rate=44100):
        if audio is not None:
            write('temp_recording.wav', sample_rate, audio)
            return 'temp_recording.wav'
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
            parsed_result = json.loads(result)
            if parsed_result.get('status', {}).get('code') == 0:
                return parsed_result
            return None
        except Exception:
            return None

    def get_tabs(self, song_title, artist):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        ug_url = None
        songsterr_url = None

        try:
            query = f"{song_title} {artist}".replace(" ", "+")
            ug_url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={query}"
            if self.ids.tab_source.text == "UG":
                webbrowser.open(ug_url)
        except Exception:
            pass

        try:
            query = f"{song_title} {artist}".replace(" ", "+")
            url = f"https://www.songsterr.com/?pattern={query}"
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            tab_links = soup.select('a[href*="/a/wsa/"]')
            for link in tab_links:
                link_text = link.get_text().lower()
                link_href = link['href'].lower()
                if (song_title.lower() in link_text or artist.lower() in link_text or
                    song_title.lower() in link_href or artist.lower() in link_href):
                    songsterr_url = "https://www.songsterr.com" + link['href']
                    if self.ids.tab_source.text == "Songsterr":
                        webbrowser.open(songsterr_url)
                    break
            else:
                songsterr_url = "No Songsterr tabs found."
        except Exception:
            songsterr_url = "No tabs available."

        return songsterr_url, ug_url

    def start_recording(self, instance):
        self.status_text = "Recording..."
        Clock.schedule_once(self._record_and_identify, 0)

    def _record_and_identify(self, dt):
        audio = self.record_audio()
        if audio is not None:
            audio_file = self.save_audio(audio)
            if audio_file:
                self.status_text = "Identifying..."
                song_info = self.identify_song(audio_file)
                if song_info and song_info.get('status', {}).get('code') == 0:
                    title = song_info['metadata']['music'][0]['title']
                    artist = song_info['metadata']['music'][0]['artists'][0]['name']
                    self.status_text = f"{title} by {artist}"
                    songsterr_url, ug_url = self.get_tabs(title, artist)
                    self.songsterr_link = songsterr_url
                    self.ug_link = ug_url
                else:
                    self.status_text = "Couldn’t identify song"
                    self.clear_links()
            else:
                self.status_text = "Failed to save audio"
                self.clear_links()
        else:
            self.status_text = "Recording failed"
            self.clear_links()

    def clear_results(self, instance):
        self.status_text = "Ready to record"
        self.clear_links()

    def clear_links(self):
        self.songsterr_link = ""
        self.ug_link = ""

    def open_songsterr_url(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.songsterr_link.startswith("http"):
            webbrowser.open(self.songsterr_link)

    def open_ug_url(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.ug_link.startswith("http"):
            webbrowser.open(self.ug_url)

    def open_donate(self, instance):
        webbrowser.open("https://www.paypal.me/jbfiresteels")

class SongTabFinderApp(App):
    def build(self):
        return SongTabFinder()

if __name__ == '__main__':
    SongTabFinderApp().run()
