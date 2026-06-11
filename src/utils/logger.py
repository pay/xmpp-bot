import logging
import logging.config
import yaml
from pathlib import Path

def setup_logging(config_file: str = "config/logging.yaml"):
    """Setup logging dari file konfigurasi YAML."""
    config_path = Path(config_file)
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Buat direktori logs jika belum ada
        Path('logs').mkdir(exist_ok=True)
        
        logging.config.dictConfig(config)
    else:
        # Fallback ke setup sederhana
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    return logging.getLogger(__name__)
