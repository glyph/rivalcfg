from .. import usbhid


_BATTERY_CHARGING_FLAG = 0b10000000


profile = {
    "name": "SteelSeries Prime Wireless",
    "models": [
        {
            "name": "SteelSeries Prime Wireless (wired mode)",
            "vendor_id": 0x1038,
            "product_id": 0x1842,
            "endpoint": 3,
        },
    ],
    "settings": {
        "sensitivity": {
            "label": "Sensibility presets",
            "description": "Set sensitivity preset (DPI)",
            "cli": ["-s", "--sensitivity"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2D],
            "value_type": "multidpi_range",
            "input_range": [100, 18000, 100],
            "output_range": [0x00, 0xD6, 1.2],
            "dpi_length_byte": 1,
            "first_preset": 0,
            "count_mode": "number",
            "max_preset_count": 5,
            "default": "400, 800, 1200, 2400, 3200",
        },
        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2B],
            "value_type": "choice",
            "choices": {
                125: 0x03,
                250: 0x02,
                500: 0x01,
                1000: 0x00,
            },
            "default": 1000,
        },
        "color": {
            "label": "LED color",
            "description": "Set the mouse LED color",
            "cli": ["-c", "--color"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x21, 0x01, 0x00],
            "value_type": "rgbcolor",
            "default": "red",
        },
        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x2A],
            "value_type": "buttons",
            # fmt: off
            "buttons": {
                "Button1":    {"id": 0x01, "offset": 0x00, "default": "button1"},
                "Button2":    {"id": 0x02, "offset": 0x05, "default": "button2"},
                "Button3":    {"id": 0x03, "offset": 0x0A, "default": "button3"},
                "Button4":    {"id": 0x04, "offset": 0x0F, "default": "button4"},
                "Button5":    {"id": 0x05, "offset": 0x14, "default": "button5"},
                "Button6":    {"id": 0x06, "offset": 0x19, "default": "dpi"},
                "ScrollUp"  : {"id": 0x31, "offset": 0x1E, "default": "scrollup"},
                "ScrollDown": {"id": 0x32, "offset": 0x23, "default": "scrolldown"},
            },
            "button_field_length": 5,
            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30,
            "button_scroll_up":   None,
            "button_scroll_down": None,
            # fmt: on
            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=dpi; scrollup=scrollup; scrolldown=scrolldown; layout=qwerty)",
        },
        "sleep_timer": {
            "label": "Sleep timer",
            "description": "Set the IDLE time before the mouse goes to sleep mode (minutes, 0 = disable)",
            "cli": ["-t", "--sleep-timer"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x29],
            "value_type": "range",
            "input_range": [0, 20, 1],
            "output_range": [0x000000, 0x124F80, 60000],
            "range_length_byte": 3,
            "default": 5,
        },
        "dim_timer": {
            "label": "Dim timer",
            "description": "Set the IDLE time before the mouse light is dimmed (seconds, 0 = disable)",
            "cli": ["-T", "--dim-timer"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x23, 0x0F, 0x01, 0x00, 0x00],
            "value_type": "range",
            "input_range": [0, 1200, 1],
            "output_range": [0x000000, 0x124F80, 1000],
            "range_length_byte": 3,
            "default": 30,
        },
        "default_lighting": {
            "label": "Default lighting",
            "description": "Set default lighting at mouse startup",
            "cli": ["-d", "--default-lighting"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x27],
            "value_type": "choice",
            "choices": {
                "off": 0x00,
                "rainbow": 0x01,
            },
            "default": "rainbow",
        },
    },
    "battery_level": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x92],
        "response_length": 2,
        "is_charging": lambda data: bool(data[1] & _BATTERY_CHARGING_FLAG),
        "level": lambda data: ((data[1] & ~_BATTERY_CHARGING_FLAG) - 1) * 5,
    },
    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x11, 0x00],
    },
}
