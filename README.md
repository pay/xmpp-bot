# BotAsisten - XMPP Bot 🤖

Bot XMPP yang cerdas, ramah, dan profesional untuk komunikasi pribadi dan grup.

## ✨ Fitur

- ✅ Koneksi ke server XMPP dengan slixmpp
- ✅ Chat pribadi (private) dan grup (MUC)
- ✅ Sistem command dengan prefix `!`
- ✅ Handler modular untuk berbagai tipe pesan
- ✅ Logging terstruktur dan extensible
- ✅ Konfigurasi via YAML
- ✅ Respons casual yang ramah
- ✅ Mudah menambah command baru

## 📋 Prasyarat

- **Python 3.8+**
- Server XMPP yang aktif (ejabberd, Prosody, atau OpenFire)

## 🚀 Instalasi & Setup

### 1. Clone Repository
```bash
git clone https://github.com/pay/xmpp-bot.git
cd xmpp-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Bot

Edit `config/config.yaml`:
```yaml
bot:
  jid: "botasisten@example.com"      # Ganti dengan JID bot Anda
  password: "your_password"           # Ganti dengan password
  nick: "BotAsisten"

server:
  host: "example.com"                 # Ganti dengan host XMPP
  port: 5222
  use_tls: true

muc:
  rooms:
    - jid: "tim_proyek@conference.example.com"
      nick: "BotAsisten"
    - jid: "general@conference.example.com"
      nick: "BotAsisten"
```

### 4. Jalankan Bot
```bash
python -m src.main
```

Anda akan melihat log seperti:
```
======================================================================
BotAsisten - XMPP Bot v1.0.0
======================================================================
2024-01-15 10:30:45 - bot - INFO - Konfigurasi dimuat dari config/config.yaml
2024-01-15 10:30:45 - bot - INFO - Menghubung ke example.com:5222
2024-01-15 10:30:46 - bot - INFO - Koneksi XMPP berhasil
2024-01-15 10:30:47 - bot - INFO - Bot BotAsisten berhasil terhubung dan session dimulai
```

## 💬 Perintah Bot

| Perintah | Deskripsi |
|----------|----------|
| `!help` | Tampilkan daftar bantuan |
| `!info` | Informasi tentang bot |
| `!echo <pesan>` | Ulangi pesan |
| `!ping` | Cek status bot (online/offline) |

## 💻 Chat Casual

Bot juga bisa merespons percakapan biasa:

**Private Chat:**
```
User: Halo bot!
Bot:  Halo {nama}! Ada yang bisa saya bantu? 😊
```

**Group Chat:**
```
User: BotAsisten, tolong bantu!
Bot:  {nama}, silakan ketik !help untuk melihat daftar perintah saya. 😊
```

## 📁 Struktur Project

```
xmpp-bot/
├── config/
│   ├── config.yaml          # Konfigurasi utama (EDIT INI!)
│   └── logging.yaml         # Setup logging
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── bot.py           # Bot orchestrator
│   │   ├── connection.py    # Koneksi XMPP
│   │   └── dispatcher.py    # Router command
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── message.py       # Handler chat pribadi
│   │   └── groupchat.py     # Handler MUC
│   └── utils/
│       ├── __init__.py
│       ├── config_loader.py # Parser konfigurasi
│       └── logger.py        # Setup logging
├── tests/                   # Unit & integration tests
├── logs/                    # Log files (auto-created)
├── requirements.txt         # Python dependencies
├── README.md                # Dokumentasi
└── .gitignore              # Git ignore patterns
```

## 🔧 Development - Menambah Command Baru

Buka `src/core/bot.py` dan tambahkan di method `_register_commands()`:

```python
def _register_commands(self):
    # ... existing commands ...
    self.dispatcher.register_command(
        "mycommand",
        self._cmd_mycommand,
        "Deskripsi perintah saya"
    )

def _cmd_mycommand(self, args: str, context: dict) -> str:
    """Command: !mycommand <args>"""
    sender_name = context['sender_name']
    chat_type = context['chat_type']
    
    if not args:
        return "Gunakan: !mycommand <argument>"
    
    return f"Hasil perintah Anda: {args}"
```

Sekarang command `!mycommand` sudah bisa digunakan!

## 🔒 Keamanan

- Jangan commit `config/config.yaml` dengan password ke repository
- Gunakan environment variable untuk sensitive data:
  ```bash
  export XMPP_PASSWORD="your_secure_password"
  ```
  Kemudian edit config loader untuk membaca dari env

## 📝 Logging

Log tersimpan di `logs/bot.log` dan juga ditampilkan di console. Level dapat diatur di `config/logging.yaml`.

## 🐛 Troubleshooting

**Bot tidak bisa connect**
- Pastikan JID, password, host, dan port benar di `config/config.yaml`
- Cek apakah server XMPP running
- Periksa firewall

**Logging tidak berfungsi**
- Pastikan folder `logs/` ada dan writable
- Periksa file `config/logging.yaml`

## 📚 Resources

- [slixmpp Documentation](https://slixmpp.readthedocs.io/)
- [XMPP Standards](https://xmpp.org/)
- [Ejabberd XMPP Server](https://www.ejabberd.im/)

## 📄 License

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

## 👨‍💻 Author

Created with ❤️ untuk komunitas XMPP Indonesia

---

**Questions?** Tanya di channel XMPP atau buat issue di repository!
