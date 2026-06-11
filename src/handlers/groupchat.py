import logging
import re

logger = logging.getLogger(__name__)

class GroupChatHandler:
    """Handler untuk pesan grup (MUC - Multi-User Chat)."""
    
    def __init__(self, dispatcher, ai_manager=None):
        """
        Inisialisasi groupchat handler.
        
        Args:
            dispatcher: CommandDispatcher instance
            ai_manager: AIManager instance (opsional)
        """
        self.dispatcher = dispatcher
        self.ai_manager = ai_manager
    
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
        should_reply, mention_type = self._should_reply(text, client.nick)
        
        if not should_reply:
            logger.debug(f"Pesan dari {sender_name} diabaikan (tidak relevan)")
            return
        
        # Handle mention untuk AI
        if mention_type == 'ai' and self.ai_manager and self.ai_manager.is_enabled():
            prompt = self._extract_prompt_from_mention(text, client.nick)
            if prompt:
                response = self.ai_manager.generate_response(prompt, context)
                if response:
                    msg.reply(response).send()
                    logger.info(f"[GROUP AI REPLY to {sender_name}] {response[:80]}...")
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
    
    def _should_reply(self, text: str, bot_nick: str) -> tuple:
        """
        Tentukan apakah bot harus membalas pesan dan tipe mention.
        
        Args:
            text: Pesan
            bot_nick: Nick bot di room
            
        Returns:
            tuple: (should_reply: bool, mention_type: str) -> 'ai', 'normal', atau None
        """
        text_lower = text.lower()
        bot_nick_lower = bot_nick.lower()
        
        # Balas jika ada command (prefix !)
        if text.startswith('!'):
            return True, 'command'
        
        # Balas jika nama bot disebutkan dengan @ (AI mention)
        if f"@{bot_nick_lower}" in text_lower or f"@{bot_nick}" in text:
            return True, 'ai'
        
        # Balas jika nama bot disebutkan tanpa @ (normal mention)
        if bot_nick_lower in text_lower:
            return True, 'normal'
        
        if 'botasisten' in text_lower:
            return True, 'normal'
        
        # Balas jika ada kata kunci help/bantuan
        if any(word in text_lower for word in ['help', 'bantuan', 'perintah', 'bot']):
            return True, 'normal'
        
        return False, None
    
    def _extract_prompt_from_mention(self, text: str, bot_nick: str) -> str:
        """
        Extract prompt dari mention @botname.
        
        Args:
            text: Pesan dengan mention
            bot_nick: Nick bot
            
        Returns:
            str: Prompt tanpa mention prefix
        """
        # Pattern: @botname prompt
        pattern = rf"@{re.escape(bot_nick)}\s+(.+)"
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        return text.strip()
    
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
            ai_hint = ""
            if self.ai_manager and self.ai_manager.is_enabled():
                ai_hint = " Atau sebutkan @BotAsisten untuk AI response."
            return f"{sender_name}, silakan ketik !help untuk melihat daftar perintah saya.{ai_hint} 😊"
        
        # Default: no response
        return None
