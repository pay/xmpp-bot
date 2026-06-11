import logging

logger = logging.getLogger(__name__)

class MessageHandler:
    """Handler untuk pesan pribadi (private chat)."""
    
    def __init__(self, dispatcher):
        """
        Inisialisasi message handler.
        
        Args:
            dispatcher: CommandDispatcher instance
        """
        self.dispatcher = dispatcher
    
    def handle(self, msg, client):
        """
        Proses pesan pribadi.
        
        Args:
            msg: Pesan dari slixmpp
            client: XMPP client instance
        """
        sender_jid = str(msg['from'])
        sender_name = msg['from'].bare.split('@')[0]
        text = msg['body'].strip()
        
        context = {
            'sender_jid': sender_jid,
            'sender_name': sender_name,
            'chat_type': 'private',
            'client': client
        }
        
        logger.info(f"[PRIVATE] {sender_name}: {text}")
        
        # Cek apakah pesan adalah command
        response = self.dispatcher.dispatch(text, context)
        
        # Jika bukan command, treat sebagai percakapan biasa
        if response is None:
            response = self._handle_casual_message(text, context)
        
        # Kirim respons
        if response:
            msg.reply(response).send()
            logger.info(f"[REPLY to {sender_name}] {response[:80]}...")
    
    def _handle_casual_message(self, text: str, context: dict) -> str:
        """
        Handle percakapan biasa (non-command).
        
        Args:
            text: Pesan dari pengguna
            context: Context pesan
            
        Returns:
            str: Respons yang tepat
        """
        text_lower = text.lower()
        sender_name = context['sender_name']
        
        # Greeting
        if any(word in text_lower for word in ['halo', 'hai', 'hello', 'hi', 'assalamu', 'pagi', 'sore', 'malam']):
            return f"Halo {sender_name}! Ada yang bisa saya bantu? 😊"
        
        # Asking how are you
        if any(word in text_lower for word in ['apa kabar', 'gimana kabar', 'how are you', 'kabar mu', 'kabar kamu']):
            return f"Kabar saya baik, terima kasih! Bagaimana dengan Anda, {sender_name}?"
        
        # Thanks
        if any(word in text_lower for word in ['terima kasih', 'terimakasih', 'thank', 'thanks', 'tq', 'makasih']):
            return "Sama-sama! Senang membantu Anda. 😊"
        
        # Asking for help
        if any(word in text_lower for word in ['bantuan', 'help', 'tolong', 'caranya', 'bagaimana']):
            return f"Silakan katakan apa yang Anda butuhkan, {sender_name}. Atau ketik !help untuk melihat perintah saya."
        
        # Default response
        return f"Saya menerima pesan Anda, {sender_name}. Ketik !help jika butuh bantuan atau perintah tertentu."
