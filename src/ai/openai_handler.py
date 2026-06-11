import logging
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError
from src.ai.base_ai import BaseAIHandler

logger = logging.getLogger(__name__)

class OpenAIHandler(BaseAIHandler):
    """Handler untuk OpenAI API (ChatGPT)."""
    
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
            self.client = OpenAI(api_key=api_key)
            self.model = openai_config.get('model', 'gpt-4o-mini')
            self.temperature = openai_config.get('temperature', 0.7)
            self.max_tokens = openai_config.get('max_tokens', 500)
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
            # Format prompt dengan system instruction
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            logger.debug(f"Mengirim request ke OpenAI: {prompt[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=0.9,
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"OpenAI response: {result[:80]}...")
            return result
            
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error: {e}")
            return "❌ Error koneksi ke OpenAI. Coba lagi nanti."
        except APITimeoutError as e:
            logger.error(f"OpenAI timeout: {e}")
            return "⏱️ OpenAI timeout. Coba lagi nanti."
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return f"❌ Error: {str(e)[:100]}"
        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI: {e}", exc_info=True)
            return f"❌ Error tidak terduga: {str(e)[:100]}"
