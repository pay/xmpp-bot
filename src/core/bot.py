import logging
from src.utils.config_loader import ConfigLoader
from src.core.connection import XMPPConnection
from src.core.dispatcher import CommandDispatcher
from src.handlers.message import MessageHandler
from src.handlers.groupchat import GroupChatHandler
from src.ai.ai_manager import AIManager

logger = logging.getLogger(__name__)

class XMPPBot:
    """Bot XMPP utama - orchestrator untuk semua komponen."""
    
    def __init__(self, config_file: str = "config/config.yaml"):
        """
        Inisialisasi bot.
        
        Args:
            config_file: Path ke file konfigurasi YAML
        """
        self.config = ConfigLoader(config_file)
        
        # Inisialisasi koneksi XMPP
        self.connection = XMPPConnection(
            jid=self.config.get_bot_jid(),
            password=self.config.get_bot_password(),
            host=self.config.get_server_host(),
            port=self.config.get_server_port(),
            use_tls=self.config.get_use_tls()
        )
        
        self.client = self.connection.get_client()
        self.dispatcher = CommandDispatcher()
        
        # Inisialisasi AI
        self.ai_manager = AIManager(self.config.get_ai_config())
        
        # Register handlers
        self.message_handler = MessageHandler(self.dispatcher, self.ai_manager)
        self.groupchat_handler = GroupChatHandler(self.dispatcher, self.ai_manager)
        
        self._setup_handlers()
        self._register_commands()
        self._setup_muc()
        self._join_rooms()
    
    def _setup_handlers(self):
        """Setup event handlers untuk pesan."""
        self.client.add_event_handler("message", self._on_message)
        self.client.add_event_handler("groupchat_message", self._on_groupchat_message)
    
    def _setup_muc(self):
        """Setup Multi-User Chat (MUC) plugin."""
        try:
            if 'xep_0045' not in self.client.plugin:
                self.client.register_plugin('xep_0045')  # MUC
            logger.info("MUC plugin siap")
        except Exception as e:
            logger.error(f"Error setup MUC: {e}")
    
    def _on_message(self, msg):
        """
        Event handler untuk pesan pribadi.
        
        Args:
            msg: Pesan dari slixmpp
        """
        if msg['type'] in ('chat', 'normal'):
            self.message_handler.handle(msg, self.client)
    
    def _on_groupchat_message(self, msg):
        """
        Event handler untuk pesan grup.
        
        Args:
            msg: Pesan dari slixmpp
        """
        if msg['type'] == 'groupchat':
            self.groupchat_handler.handle(msg, self.client)
    
    def _register_commands(self):
        """Daftarkan built-in commands."""
        self.dispatcher.register_command(
            "help",
            self._cmd_help,
            "Tampilkan bantuan perintah"
        )
        self.dispatcher.register_command(
            "info",
            self._cmd_info,
            "Tampilkan informasi bot"
        )
        self.dispatcher.register_command(
            "echo",
            self._cmd_echo,
            "Ulangi pesan (echo <pesan>)"
        )
        self.dispatcher.register_command(
            "ping",
            self._cmd_ping,
            "Cek status bot"
        )
        self.dispatcher.register_command(
            "ai",
            self._cmd_ai,
            "Query AI (ai <pertanyaan>)"
        )
    
    def _cmd_help(self, args: str, context: dict) -> str:
        """Command: !help - Tampilkan bantuan."""
        return self.dispatcher.get_help()
    
    def _cmd_info(self, args: str, context: dict) -> str:
        """Command: !info - Informasi bot."""
        return f"Saya adalah {self.config.get_bot_nick()}, asisten bot XMPP yang siap membantu Anda. Ketik !help untuk melihat daftar perintah lengkap."
    
    def _cmd_echo(self, args: str, context: dict) -> str:
        """Command: !echo <pesan> - Ulangi pesan."""
        if not args:
            return "Gunakan: !echo <pesan>"
        return f"Echo: {args}"
    
    def _cmd_ping(self, args: str, context: dict) -> str:
        """Command: !ping - Cek status bot."""
        return "Pong! Bot masih online dan siap melayani. 🤖"
    
    def _cmd_ai(self, args: str, context: dict) -> str:
        """Command: !ai <pertanyaan> - Query AI."""
        if not self.ai_manager.is_enabled():
            return "⚠️ AI feature tidak tersedia. Hubungi admin."
        
        if not args:
            return "Gunakan: !ai <pertanyaan>"
        
        return self.ai_manager.generate_response(args, context)
    
    def _join_rooms(self):
        """Bergabung dengan MUC rooms yang dikonfigurasi."""
        muc = self.client['xep_0045']
        rooms = self.config.get_muc_rooms()
        
        for room_info in rooms:
            room_jid = room_info.get('jid')
            nick = room_info.get('nick', self.config.get_bot_nick())
            try:
                muc.join_muc(room_jid, nick)
                logger.info(f"Bot bergabung dengan room: {room_jid} (nick: {nick})")
            except Exception as e:
                logger.error(f"Gagal bergabung room {room_jid}: {e}")
    
    def start(self):
        """Mulai bot (event loop berjalan indefinitely)."""
        logger.info("=" * 60)
        logger.info(f"Bot XMPP '{self.config.get_bot_nick()}' dimulai...")
        logger.info(f"JID: {self.config.get_bot_jid()}")
        logger.info(f"Server: {self.config.get_server_host()}:{self.config.get_server_port()}")
        if self.ai_manager.is_enabled():
            logger.info(f"AI Feature: ENABLED ({self.ai_manager.provider})")
        else:
            logger.info("AI Feature: DISABLED")
        logger.info("=" * 60)
        
        if self.connection.connect():
            self.connection.process(block=True)
        else:
            logger.error("Gagal menghubungkan bot ke server XMPP")
    
    def stop(self):
        """Hentikan bot."""
        logger.info("Menghentikan bot...")
        self.connection.disconnect()
