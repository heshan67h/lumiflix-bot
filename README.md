# MovieVerse Telegram Bot

Telegram bot for MovieVerse app - forwards movies from your private channel to users on demand.

## Features
- Deep link support for in-app download buttons
- Automatic movie forwarding from private channel
- User-friendly error messages
- Supports multiple movies

## Deployment

### Files needed:
- `movieverse_bot.py` - Main bot script
- `requirements.txt` - Python dependencies
- `Procfile` - Tells hosting service how to run bot
- `runtime.txt` - Python version specification

### Deploy to Railway.app (FREE):
1. Create account at railway.app
2. New Project → Deploy from GitHub
3. Connect your repo or upload files
4. Bot automatically starts!
5. Check logs to verify it's running

### Deploy to Render.com (FREE):
1. Create account at render.com
2. New → Background Worker
3. Connect GitHub or upload
4. Build command: `pip install -r requirements.txt`
5. Start command: `python movieverse_bot.py`
6. Deploy!

## Configuration

Bot credentials are in the code:
- API_ID: 28484876
- API_HASH: baab9e6a37245a4972d7878b636af4e3
- BOT_TOKEN: 8243415590:AAHYXP91-LamZTHOjqrMTuqA4pVcPF24TuQ
- CHANNEL_ID: -1002986160944

Movies database (add your movies):
```python
MOVIES = {
    "msg_5": 5,
    "msg_9": 9,
    "msg_11": 11,
    "msg_12": 12,
    "msg_15": 15,
    "msg_17": 17,
}
```

## Bot Commands

- `/start` - Welcome message
- `/start msg_XX` - Request specific movie (XX = message ID)
- `/help` - Help information
- `/movies` - List available movies

## Deep Links

Format: `t.me/movieverse_storage_bot?start=msg_XX`

Example:
- `t.me/movieverse_storage_bot?start=msg_12` - Request movie with message ID 12

Use these links in your MovieVerse admin panel!

## Support

For issues or questions, contact the MovieVerse team.
