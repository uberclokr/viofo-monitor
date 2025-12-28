import time
import threading

import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.toast import toast
from kivy.core.window import Window

try:
    from kivy.core.window import Window
    # Set default aspect ratio 16:9 (e.g. 1280x720)
    Window.size = (1280, 720)
except:
    pass

# Check for ffpyplayer
try:
    from ffpyplayer.player import MediaPlayer
except ImportError:
    MediaPlayer = None
    print("ffpyplayer not found. Video will not play.")

class ViofoVideoWidget(Widget):
    source = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = None
        self.trigger_update = Clock.create_trigger(self.update_frame, 0)
        self.is_playing = False

    def play(self, url):
        if not MediaPlayer:
            return
        if self.player:
            self.player.close_player()
        
        self.source = url
        # Options to help with RTSP stream startup
        opts = {
            'packet-buffering': False, # Low latency
            'fflags': 'nobuffer', # Reduce legacy buffering
            'analyzeduration': 200000, # 0.2s to find stream info
            'probesize': 32768, # 32KB
            'rtsp_transport': 'tcp', # Force TCP for reliability
            'framedrop': True,
            'sync': 'ext' # Sync to external clock
        }
        self.player = MediaPlayer(self.source, ff_opts=opts)
        self.is_playing = True
        self.trigger_update()

    def stop(self):
        if self.player:
            self.player.close_player()
            self.player = None
        self.is_playing = False

    def update_frame(self, dt):
        if not self.player or not self.is_playing:
            return

        frame, val = self.player.get_frame()
        if val == 'eof':
            # Auto-reconnect if EOF (common in RTSP)
            # self.play(self.source) # Simple retry logic?
            pass
        elif val == 'paused':
            pass
        elif frame:
            img, t = frame
            # Convert to Kivy Texture
            texture = Texture.create(size=img.get_size(), colorfmt='rgb')
            texture.blit_buffer(img.to_bytearray()[0], colorfmt='rgb', bufferfmt='ubyte')
            texture.flip_vertical()
            
            self.canvas.before.clear()
            with self.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(1, 1, 1, 1)
                Rectangle(pos=self.pos, size=self.size, texture=texture)

        if self.is_playing:
            self.trigger_update()

class MainScreen(Screen):
    pass

class ViofoMonitorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        Builder.load_file("viofo.kv")
        return MainScreen()

    # User requested ONLY this specific stream URL
    stream_urls = ["rtsp://192.168.1.254"]
    target_ip = "192.168.1.254"
    dialog = None
    menu = None
    current_stream_index = NumericProperty(-1)

    # Viofo Commands Mapping
    COMMANDS = {
        "Record Toggle": 2001,
        "Take Photo": 1001,
        "Cycle View (PIP)": 3028,
        "Firmware Version": 3012,
        "Reboot Camera": 9095,
    }

    def on_start(self):
        # Skip probing, direct start
        print(f"Direct start on {self.stream_urls[0]}")
        Clock.schedule_once(lambda dt: self.start_stream_index(0))

    def open_menu(self, caller):
        menu_items = []
        for name, cmd_id in self.COMMANDS.items():
            menu_items.append(
                {
                    "text": name,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=name, y=cmd_id: self.menu_callback(x, y),
                }
            )
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text, cmd_id):
        self.menu.dismiss()
        is_dangerous = "Dangerous" in text or "Format" in text or "Delete" in text
        
        if is_dangerous:
            self.show_confirmation_dialog(text, cmd_id)
        elif cmd_id == 3012: # Firmware Version
            self.send_command(cmd_id, callback=self.show_response_dialog)
        else:
            self.send_command(cmd_id)

    def show_confirmation_dialog(self, text, cmd_id):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Confirm Action",
                text=f"Are you sure you want to execute '{text}'? This may be destructive.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="CONFIRM",
                        md_bg_color=(1, 0, 0, 1), # Red
                        on_release=lambda x: self.confirm_action(cmd_id)
                    ),
                ],
            )
        self.dialog.text = f"Are you sure you want to execute '{text}'?"
        # Hacky way to update button callbacks if reused, usually better to recreate
        # simpler: Recreate dialog each time for safety or bind correct partial
        self.dialog.buttons[1].bind(on_release=lambda x: self.confirm_action(cmd_id))
        self.dialog.open()

    def confirm_action(self, cmd_id):
        self.dialog.dismiss()
        self.send_command(cmd_id)

    def show_response_dialog(self, text):
        Clock.schedule_once(lambda dt: self._show_info_dialog(text))

    def _show_info_dialog(self, text):
        # XML Cleanup (simple heuristic)
        # Often returns <Function>...<String>Version</String>...</Function>
        # We can try to extract <String> content or just show all
        clean_text = text
        if "<String>" in text and "</String>" in text:
            import re
            m = re.search(r"<String>(.*?)</String>", text)
            if m:
                clean_text = m.group(1)
        
        self.info_dialog = MDDialog(
            title="Command Response",
            text=clean_text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.info_dialog.dismiss())]
        )
        self.info_dialog.open()

    def send_command(self, cmd_id, param=None, callback=None):
        url = f"http://{self.target_ip}/?custom=1&cmd={cmd_id}"
        if param is not None:
             url += f"&par={param}"
        
        print(f"Executing: {url}")
        threading.Thread(target=self._send_http_req, args=(url, callback), daemon=True).start()

    def _send_http_req(self, url, callback=None):
        try:
            r = requests.get(url, timeout=2)
            msg = f"CMD Sent. Code: {r.status_code}"
            print(msg)
            if callback:
                 callback(r.text)
        except Exception as e:
            print(f"CMD Failed: {e}")

    def start_stream_index(self, index):
        if not self.stream_urls:
            return

        # Always usage index 0 since we only have one URL
        url = self.stream_urls[0]
        
        screen = self.root
        video = screen.ids.video_main
        print(f"Starting Stream: {url}")
        # label.text = f"Stream: {url}"
        video.play(url)

    def switch_camera(self, target_index):
        # Stop current stream to allow camera to switch modes if needed
        self.root.ids.video_main.stop()
        
        cmd_id = 3028 # PIP_STYLE
        
        # par=0 (Front), par=1 (Inside), par=2 (Rear)
        threading.Thread(target=self._send_switch_command_and_restart, args=(cmd_id, target_index), daemon=True).start()
        
        # Update local index
        self.current_stream_index = target_index

    def _send_switch_command_and_restart(self, cmd_id, param):
        print(f"Switching Camera... CMD={cmd_id} PAR={param}")
        self.send_command(cmd_id, param)
            
        # Wait a moment for camera to process
        time.sleep(1.5) # Increased wait for mode switch
        
        # Restart stream
        Clock.schedule_once(lambda dt: self.start_stream_index(0))

if __name__ == "__main__":
    ViofoMonitorApp().run()
