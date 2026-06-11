import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Loader untuk konfigurasi bot dari file YAML."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = {}
        self.load()
    
    def load(self):
        """Muat konfigurasi dari file YAML."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"Konfigurasi dimuat dari {self.config_path}")
        except FileNotFoundError:
            logger.error(f"File konfigurasi tidak ditemukan: {self.config_path}")
            self.config = {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML: {e}")
            self.config = {}
    
    def get(self, key: str, default=None):
        """Ambil nilai konfigurasi dengan nested key support (dot notation)."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def get_bot_jid(self) -> str:
        """Ambil JID bot."""
        return self.get('bot.jid', 'bot@example.com')
    
    def get_bot_password(self) -> str:
        """Ambil password bot."""
        return self.get('bot.password', '')
    
    def get_bot_nick(self) -> str:
        """Ambil nickname bot."""
        return self.get('bot.nick', 'BotAsisten')
    
    def get_server_host(self) -> str:
        """Ambil host server XMPP."""
        return self.get('server.host', 'example.com')
    
    def get_server_port(self) -> int:
        """Ambil port server XMPP."""
        return self.get('server.port', 5222)
    
    def get_use_tls(self) -> bool:
        """Ambil setting TLS."""
        return self.get('server.use_tls', True)
    
    def get_muc_rooms(self) -> list:
        """Ambil daftar MUC rooms."""
        return self.get('muc.rooms', [])
    
    def get_enabled_plugins(self) -> list:
        """Ambil daftar plugin yang diaktifkan."""
        return self.get('plugins.enabled', [])
    
    def get_ai_config(self) -> dict:
        """Ambil konfigurasi AI."""
        return self.get('ai', {})
