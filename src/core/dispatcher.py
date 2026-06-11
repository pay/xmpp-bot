import logging
import re
from typing import Callable, Dict

logger = logging.getLogger(__name__)

class CommandDispatcher:
    """Router untuk perintah bot (prefix !)."""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
    
    def register_command(self, name: str, handler: Callable, help_text: str = ""):
        """
        Daftarkan handler untuk perintah.
        
        Args:
            name: Nama command (tanpa prefix !)
            handler: Fungsi yang menangani command
            help_text: Deskripsi command
        """
        self.commands[name] = {
            'handler': handler,
            'help': help_text
        }
        logger.debug(f"Command registered: !{name}")
    
    def parse_command(self, message: str) -> tuple:
        """
        Parse pesan untuk mendapatkan command dan arguments.
        
        Args:
            message: Pesan pengguna
            
        Returns:
            tuple: (command, args) atau (None, None) jika bukan command
        """
        if not message.startswith('!'):
            return None, None
        
        # Pisahkan command dan args
        parts = message[1:].split(None, 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        return command, args
    
    def dispatch(self, message: str, context: dict) -> str:
        """
        Dispatch pesan ke handler yang sesuai.
        
        Args:
            message: Pesan pengguna
            context: Context (sender_jid, chat_type, dll)
            
        Returns:
            str: Respons dari handler, atau None jika bukan command
        """
        command, args = self.parse_command(message)
        
        if command is None:
            return None
        
        if command not in self.commands:
            return f"Perintah '!{command}' tidak dikenali. Ketik !help untuk daftar perintah."
        
        try:
            handler = self.commands[command]['handler']
            result = handler(args, context)
            return result
        except Exception as e:
            logger.error(f"Error executing command !{command}: {e}")
            return f"Error saat menjalankan perintah !{command}: {str(e)}"
    
    def get_help(self) -> str:
        """Dapatkan bantuan untuk semua perintah."""
        help_text = "=== Daftar Perintah Bot ===\n"
        for cmd, info in sorted(self.commands.items()):
            help_text += f"!{cmd} - {info['help']}\n"
        return help_text.strip()
