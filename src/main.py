import os
import logging
import sys
from src.utils.logger import setup_logging
from src.core.bot import XMPPBot

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Entry point bot XMPP."""
    config_file = os.getenv('CONFIG_FILE', 'config/config.yaml')
    
    logger.info("=" * 70)
    logger.info("BotAsisten - XMPP Bot v1.0.0")
    logger.info("=" * 70)
    
    try:
        bot = XMPPBot(config_file)
        bot.start()
    except KeyboardInterrupt:
        logger.info("\nBot dihentikan oleh pengguna")
        sys.exit(0)
    except FileNotFoundError as e:
        logger.error(f"File tidak ditemukan: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error saat menjalankan bot: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
