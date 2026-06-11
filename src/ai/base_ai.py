from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseAIHandler(ABC):
    """Base class untuk AI handlers."""
    
    def __init__(self, config: dict):
        """
        Inisialisasi AI handler.
        
        Args:
            config: Konfigurasi AI dari config.yaml
        """
        self.config = config
        self.system_prompt = config.get('system_prompt', '')
    
    @abstractmethod
    def generate_response(self, prompt: str, context: dict = None) -> str:
        """
        Generate respons AI untuk prompt.
        
        Args:
            prompt: Pertanyaan/prompt dari pengguna
            context: Context tambahan (sender_name, chat_type, dll)
            
        Returns:
            str: Respons dari AI
        """
        pass
    
    def format_prompt(self, prompt: str, context: dict = None) -> str:
        """
        Format prompt dengan context.
        
        Args:
            prompt: Prompt awal
            context: Context pengguna
            
        Returns:
            str: Prompt yang sudah diformat
        """
        if context is None:
            return prompt
        
        sender_name = context.get('sender_name', 'User')
        chat_type = context.get('chat_type', 'private')
        
        formatted = f"[{chat_type.upper()}] {sender_name}: {prompt}"
        return formatted
