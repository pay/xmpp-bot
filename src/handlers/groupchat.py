import logging

logger = logging.getLogger(__name__)

class GroupChatHandler:
    """Handler untuk pesan grup (MUC - Multi-User Chat)."""
    
    def __init__(self, dispatcher):
        """
        Inisialisasi groupchat handler.
        
        Args:
            dispatcher: CommandDispatcher instance
        """
        self.dispatcher = dispatcher
    
    def handle(self, msg, client):
        """
        Proses pesan grup.
        
        Args:
            msg: Pesan dari slixmpp
            client: XMPP client instance
        """
        sender_jid = str(msg['from'])
        room_jid = msg['from'].bare
        sender_name = msg['from'].resource  # Nick di room
        text = msg['body'].strip()
        
        # Ignore pesan dari bot sendiri
        if sender_name == client.nick:
            return
        
        context = {
            'sender_jid': sender_jid,
            'sender_name': sender_name,
            'chat_type': 'groupchat',
            'room_jid': room_jid,
            'your_nick': client.nick,
            'client': client
        }
        
        logger.info(f"[GROUP {room_jid}] {sender_name}: {text}")
        
        # Tentukan apakah bot harus membalas
        should_reply = self._should_reply(text, client.nick)
        
        if not should_reply:
            logger.debug(f"Pesan dari {sender_name} diabaikan (tidak relevan)")
            return
        
        # Cek apakah pesan adalah command
        response = self.dispatcher.dispatch(text, context)
        
        # Jika bukan command, treat sebagai percakapan casual
        if response is None and should_reply:
            response = self._handle_casual_message(text, context)
        
        # Kirim respons ke grup
        if response:
            msg.reply(response).send()
            logger.info(f"[GROUP REPLY to {sender_name}] {response[:80]}...")
    
    def _should_reply(self, text: str, bot_nick: str) -> bool:
        """
        Tentukan apakah bot harus membalas pesan.
        
        Args:
            text: Pesan
            bot_nick: Nick bot di room
            
        Returns:
            bool: True jika bot harus membalas
        """
        text_lower = text.lower()
        bot_nick_lower = bot_nick.lower()
        
        # Balas jika ada command (prefix !)
        if text.startswith('!'):
            return True
        
        # Balas jika nama bot disebutkan
        if bot_nick_lower in text_lower:
            return True
        
        if 'botasisten' in text_lower:
            return True
        
        # Balas jika ada kata kunci help/bantuan
        if any(word in text_lower for word in ['help', 'bantuan', 'perintah', 'bot']):
            return True
        
        return False
    
    def _handle_casual_message(self, text: str, context: dict) -> str:
        """
        Handle percakapan casual di grup.
        
        Args:
            text: Pesan pengguna
            context: Context pesan
            
        Returns:
            str: Respons atau None jika tidak perlu balas
        """
        text_lower = text.lower()
        sender_name = context['sender_name']
        
        # Greeting
        if any(word in text_lower for word in ['halo', 'hai', 'hello', 'hi']):
            return f"Halo {sender_name}! 👋"
        
        # Asking for help
        if any(word in text_lower for word in ['help', 'bantuan', 'tolong', 'perintah']):
            return f"{sender_name}, silakan ketik !help untuk melihat daftar perintah saya. 😊"
        
        # Default: no response
        return None
