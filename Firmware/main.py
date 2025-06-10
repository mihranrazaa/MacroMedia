import board
import time
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
import adafruit_ssd1306


class MacroMediaMinimal(KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (board.A0, board.A1, board.A2, board.A3)
        self.row_pins = (board.TX, board.RX)  
        self.diode_orientation = DiodeOrientation.COL2ROW

        self.extensions.append(MediaKeys())

        # Encoder for volume control
        encoder = EncoderHandler()
        encoder.pins = ((board.SCL, board.SDA, board.D3, False),)
        encoder.map = [((KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.AUDIO_MUTE),)]
        self.modules.append(encoder)

        # OLED setup
        self.setup_display()
        self.boot_time = time.monotonic()

        self.keymap = [
            [
                KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK,
                KC.MEDIA_PREV_TRACK, KC.MEDIA_STOP,
                KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN,
                KC.AUDIO_MUTE, KC.BRIGHTNESS_UP,
            ]
        ]

    def setup_display(self):
        """Initialize OLED display"""
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)
            self.display.fill(0)
            self.display.show()
            self.show_boot_screen()
        except:
            self.display = None

    def show_boot_screen(self):
        """Show MacroMedia for 3 seconds"""
        if not self.display:
            return
        try:
            self.display.fill(0)
            # Simple text display - "MacroMedia"
            text = "MacroMedia"
            x_pos = 20  # Approximate center
            y_pos = 12

            for i, char in enumerate(text):
                char_x = x_pos + (i * 8)
                if char_x < 120:
                    for dy in range(8):
                        for dx in range(6):
                            if char_x + dx < 128 and y_pos + dy < 32:
                                if (dx == 1 or dx == 4) and (dy > 1 and dy < 7):
                                    self.display.pixel(char_x + dx, y_pos + dy, 1)
                                elif dy == 2 or dy == 6:
                                    if dx > 0 and dx < 5:
                                        self.display.pixel(char_x + dx, y_pos + dy, 1)

            self.display.show()
        except:
            pass

    def show_default_screen(self):
        """Show default screen"""
        if not self.display:
            return
        try:
            self.display.fill(0)
            text = "Ready"
            x_pos = 45
            y_pos = 12

            for i, char in enumerate(text):
                char_x = x_pos + (i * 8)
                if char_x < 120:
                    for dy in range(8):
                        for dx in range(6):
                            if char_x + dx < 128 and y_pos + dy < 32:
                                if (dx == 1 or dx == 4) and (dy > 1 and dy < 7):
                                    self.display.pixel(char_x + dx, y_pos + dy, 1)

            self.display.show()
        except:
            pass

    def before_matrix_scan(self):
        """Update display before each scan"""
        super().before_matrix_scan()

        # Show boot screen for 3 seconds, then default
        if time.monotonic() - self.boot_time > 3.0:
            if hasattr(self, '_default_shown'):
                return
            self.show_default_screen()
            self._default_shown = True


# Initialize and run
keyboard = MacroMediaMinimal()
keyboard.go()
