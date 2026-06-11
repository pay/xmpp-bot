import logging
try:
    from openai import OpenAI, APIError, APIConnectionError, APITimeoutError
except ImportError:
    # Fallback untuk versi openai yang lebih lama
    try:
        import openai as openai_module
        from openai.error import APIError, APIConnectionError, APITimeoutError
        OpenAI = openai_module.ChatCompletion
    except ImportError:
        OpenAI = None
        APIError = Exception
        APIConnectionError = Exception
        APITimeoutError = Exception

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
            self.use_new_api = False
            return
        
        try:
            # Try new API (>=1.3.0)
            from openai import OpenAI as OpenAIClient
            self.client = OpenAIClient(api_key=api_key)
            self.use_new_api = True
            self.model = openai_config.get('model', 'gpt-4o-mini')
            self.temperature = openai_config.get('temperature', 0.7)
            self.max_tokens = openai_config.get('max_tokens', 500)
            logger.info(f"OpenAI handler initialized (new API) dengan model: {self.model}")
        except ImportError:
            # Fall back ke old API
            try:
                import openai
                openai.api_key = api_key
                self.use_new_api = False
                self.model = openai_config.get('model', 'gpt-4o-mini')
                self.temperature = openai_config.get('temperature', 0.7)
                self.max_tokens = openai_config.get('max_tokens', 500)
                logger.info(f"OpenAI handler initialized (old API) dengan model: {self.model}")
                self.client = True  # Dummy client untuk cek is_enabled
            except Exception as e:
                logger.error(f"Error inisialisasi OpenAI: {e}")
                self.client = None
                self.use_new_api = False
        except Exception as e:
            logger.error(f"Error inisialisasi OpenAI: {e}")
            self.client = None
            self.use_new_api = False
    
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
            
            if self.use_new_api:
                # New API (>=1.3.0)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                result = response.choices[0].message.content.strip()
            else:
                # Old API
                import openai
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
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            error_msg = str(e)[:100]
            
            if 'timeout' in str(e).lower():
                return "⏱️ OpenAI timeout. Coba lagi nanti."
            elif 'connection' in str(e).lower():
                return "❌ Error koneksi ke OpenAI. Coba lagi nanti."
            elif 'api' in str(e).lower() or 'unauthorized' in str(e).lower():
                return "❌ Error API OpenAI. Periksa API key Anda."
            else:
                return f"❌ Error: {error_msg}"
