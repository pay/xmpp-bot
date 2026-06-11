import logging
import openai
from src.ai.base_ai import BaseAIHandler

logger = logging.getLogger(__name__)

class OpenAIHandler(BaseAIHandler):
    """Handler untuk OpenAI API (ChatGPT) - Compatible dengan openai==0.28.0"""
    
    def __init__(self, config: dict):
        """
        Inisialisasi OpenAI handler.
        
        Args:
            config: Konfigurasi AI dari config.yaml
        """
        super().__init__(config)
        
        openai_config = config.get('openai', {})
        api_key = openai_config.get('api_key')
        
        if not api_key or api_key.startswith('sk-example'):
            logger.warning("OpenAI API key tidak dikonfigurasi dengan benar!")
            self.client = None
            return
        
        try:
            # Set API key untuk openai 0.28.0
            openai.api_key = api_key
            self.model = openai_config.get('model', 'gpt-3.5-turbo')
            self.temperature = openai_config.get('temperature', 0.7)
            self.max_tokens = openai_config.get('max_tokens', 500)
            self.client = True  # Dummy client untuk indicate initialized
            logger.info(f"OpenAI handler initialized dengan model: {self.model}")
        except Exception as e:
            logger.error(f"Error inisialisasi OpenAI: {e}")
            self.client = None
    
    def generate_response(self, prompt: str, context: dict = None) -> str:
        """
        Generate respons menggunakan OpenAI API.
        
        Args:
            prompt: Pertanyaan/prompt dari pengguna
            context: Context tambahan
            
        Returns:
            str: Respons dari GPT atau error message
        """
        if self.client is None:
            return "⚠️ OpenAI belum dikonfigurasi. Hubungi admin untuk setup API key."
        
        try:
            logger.debug(f"Mengirim request ke OpenAI: {prompt[:50]}...")
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            result = response['choices'][0]['message']['content'].strip()
            logger.info(f"OpenAI response: {result[:80]}...")
            return result
            
        except openai.error.AuthenticationError as e:
            logger.error(f"OpenAI authentication error: {e}")
            return "❌ API key OpenAI tidak valid. Periksa config Anda."
        except openai.error.APIConnectionError as e:
            logger.error(f"OpenAI connection error: {e}")
            return "❌ Error koneksi ke OpenAI. Coba lagi nanti."
        except openai.error.Timeout as e:
            logger.error(f"OpenAI timeout: {e}")
            return "⏱️ OpenAI timeout. Coba lagi nanti."
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI rate limit: {e}")
            return "⏱️ Rate limit OpenAI. Coba lagi nanti."
        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI: {e}", exc_info=True)
            error_msg = str(e)[:100]
            return f"❌ Error: {error_msg}"
