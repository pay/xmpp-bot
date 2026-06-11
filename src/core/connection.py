import logging
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

logger = logging.getLogger(__name__)

class XMPPConnection:
    """Mengelola koneksi ke server XMPP."""
    
    def __init__(self, jid: str, password: str, host: str = None, port: int = 5222,
                 use_tls: bool = True, use_ssl: bool = False):
        """
        Inisialisasi koneksi XMPP.
        
        Args:
            jid: JID bot (user@domain.com)
            password: Password untuk autentikasi
            host: Host server XMPP (opsional, bisa di-parse dari JID)
            port: Port server XMPP
            use_tls: Gunakan TLS
            use_ssl: Gunakan SSL
        """
        self.jid = jid
        self.password = password
        self.host = host if host else jid.split('@')[1]
        self.port = port
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        
        self.client = ClientXMPP(jid, password)
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup event handlers dasar."""
        self.client.add_event_handler("session_start", self._on_session_start)
        self.client.add_event_handler("disconnected", self._on_disconnected)
    
    def _on_session_start(self, event):
        """Event saat sesi XMPP dimulai."""
        logger.info(f"Bot {self.jid} berhasil terhubung dan session dimulai")
        self.client.send_presence()
        self.client.get_roster()
    
    def _on_disconnected(self, event):
        """Event saat bot terputus dari server."""
        logger.warning("Bot terputus dari server XMPP")
    
    def connect(self) -> bool:
        """
        Hubungkan ke server XMPP.
        
        Returns:
            bool: True jika koneksi berhasil, False jika gagal
        """
        try:
            logger.info(f"Menghubung ke {self.host}:{self.port}")
            if self.client.connect((self.host, self.port), use_tls=self.use_tls, 
                                   use_ssl=self.use_ssl):
                logger.info("Koneksi XMPP berhasil")
                return True
            else:
                logger.error("Gagal terhubung ke server XMPP")
                return False
        except Exception as e:
            logger.error(f"Error saat menghubung: {e}")
            return False
    
    def disconnect(self):
        """Putuskan koneksi dari server."""
        try:
            self.client.disconnect()
            logger.info("Bot terputus")
        except Exception as e:
            logger.error(f"Error saat disconnect: {e}")
    
    def process(self, block: bool = False, timeout: int = None):
        """
        Proses XMPP event loop.
        
        Args:
            block: Jika True, event loop berjalan indefinitely
            timeout: Timeout dalam detik
        """
        try:
            self.client.process(block=block, timeout=timeout)
        except KeyboardInterrupt:
            logger.info("Bot dihentikan oleh user")
            self.disconnect()
        except Exception as e:
            logger.error(f"Error dalam process loop: {e}")
    
    def get_client(self):
        """Return client object untuk konfigurasi lebih lanjut."""
        return self.client
