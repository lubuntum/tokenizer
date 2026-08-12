import json
import customtkinter as ctk
from pathlib import Path


class UITheme:
    """Theme manager that loads themes from JSON files"""

    _instance = None
    _theme_data = {}

    def __new__(cls, theme_name="default_theme"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, theme_name="default_theme"):
        if not getattr(self, '_initialized', False):
            self._initialized = True
            self.load_theme(theme_name)

    def load_theme(self, theme_name):
        """Load theme from JSON file"""
        theme_path = Path(__file__).parent.parent / "themes" / f"{theme_name}.json"

        if theme_path.exists():
            try:
                with open(theme_path, 'r') as f:
                    self._theme_data = json.load(f)
                print(f"Loaded theme: {theme_name}")
            except Exception as e:
                print(f"Error loading theme {theme_name}: {e}")
                self._theme_data = {}
        else:
            print(f"Theme file not found: {theme_path}")
            self._theme_data = {}

    def switch_theme(self, theme_name):
        """Switch to a different theme"""
        self.load_theme(theme_name)

    def get_available_themes(self):
        """Get list of available themes"""
        themes_dir = Path(__file__).parent.parent / "themes"
        if themes_dir.exists():
            themes = [f.stem for f in themes_dir.glob("*.json")]
            if themes:
                return themes
        return ["default_theme"]

    # This should be an instance method, not a class method
    def get(self, *keys, default=None):
        """Get nested theme value"""
        data = self._theme_data

        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default

        return data

    # Convenience properties
    @property
    def window_bg(self):
        return self.get("window", "background")

    @property
    def window_size(self):
        return self.get("window", "size")

    @property
    def main_frame_bg(self):
        return self.get("main_frame", "background")

    @property
    def main_frame_corner(self):
        return self.get("main_frame", "corner_radius")

    @property
    def title_color(self):
        return self.get("title", "color")

    @property
    def title_size(self):
        return self.get("title", "size")

    @property
    def entry_bg(self):
        return self.get("entry", "background")

    @property
    def entry_border(self):
        return self.get("entry", "border")

    # Font helpers
    def title_font(self):
        return ctk.CTkFont(
            size=self.get("title", "size", default=28),
            weight=self.get("title", "weight", default="bold")
        )

    def subtitle_font(self):
        return ctk.CTkFont(size=self.get("subtitle", "size", default=14))

    def label_font(self):
        return ctk.CTkFont(
            size=self.get("labels", "size", default=13),
            weight=self.get("labels", "weight", default="bold")
        )

    def entry_font(self):
        return ctk.CTkFont(size=self.get("entry", "font_size", default=13))

    def button_font(self):
        return ctk.CTkFont(
            size=self.get("buttons", "font_size", default=15),
            weight=self.get("buttons", "weight", default="bold")
        )

    def card_label_font(self):
        return ctk.CTkFont(
            size=self.get("cards", "label_size", default=12),
            weight="bold"
        )

    def card_value_font(self):
        return ctk.CTkFont(
            size=self.get("cards", "value_size", default=14),
            weight="bold"
        )

    def stat_value_font(self):
        return ctk.CTkFont(
            size=self.get("stat_cards", "value_size", default=24),
            weight="bold"
        )

    def stat_label_font(self):
        return ctk.CTkFont(size=self.get("stat_cards", "label_size", default=11))