import logging
from src.ai.openai_handler import OpenAIHandler
from src.ai.base_ai import BaseAIHandler

logger = logging.getLogger(__name__)

class AIManager:
    """Manager untuk menghandle berbagai AI providers."""
    
    def __init__(self, config: dict):
        """
        Inisialisasi AI manager.
        
        Args:
            config: Konfigurasi AI dari config.yaml
        """
        self.config = config
        self.enabled = config.get('enabled', False)
        self.provider = config.get('provider', 'openai')
        self.handler: BaseAIHandler = None
        
        if self.enabled:
            self._init_provider()
        else:
            logger.info("AI feature disabled")
    
    def _init_provider(self):
        """Inisialisasi provider yang dikonfigurasi."""
        try:
            if self.provider == 'openai':
                self.handler = OpenAIHandler(self.config)
                logger.info("OpenAI handler loaded")
            else:
                logger.warning(f"Unknown AI provider: {self.provider}")
        except Exception as e:
            logger.error(f"Error initializing AI provider: {e}")
            self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check apakah AI enabled."""
        return self.enabled and self.handler is not None
    
    def generate_response(self, prompt: str, context: dict = None) -> str:
        """
        Generate respons AI.
        
        Args:
            prompt: Pertanyaan
            context: Context pengguna
            
        Returns:
            str: Respons dari AI
        """
        if not self.is_enabled():
            return None
        
        try:
            return self.handler.generate_response(prompt, context)
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return f"❌ Error: {str(e)[:100]}"
