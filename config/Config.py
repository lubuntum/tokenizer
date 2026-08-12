import json
from pathlib import Path


class Config:
    """Simple configuration manager for user preferences"""

    CONFIG_FILE = Path(__file__).parent / "config.json"

    @classmethod
    def load(cls):
        """Load configuration from file"""
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    @classmethod
    def save(cls, config_data):
        """Save configuration to file"""
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    @classmethod
    def get(cls, key, default=None):
        """Get a config value"""
        config = cls.load()
        return config.get(key, default)

    @classmethod
    def set(cls, key, value):
        """Set a config value"""
        config = cls.load()
        config[key] = value
        cls.save(config)