# Fix for Windows event loop issue - MUST be at top!
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelPrivate
import logging
import requests
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = 28484876
API_HASH = "baab9e6a37245a4972d7878b636af4e3"
BOT_TOKEN = "8243415590:AAHYXP91-LamZTHOjqrMTuqA4pVcPF24TuQ"

# Channel ID from t.me/c/2986160944/
CHANNEL_ID = int("-100" + "2986160944")  # -1002986160944

# Force subscribe channel
FORCE_SUBSCRIBE_CHANNEL = "@movieversehub_official"
ENABLE_FORCE_SUBSCRIBE = True

# Session file (Windows compatible)
import tempfile
import os

temp_dir = tempfile.gettempdir()
session_path = os.path.join(temp_dir, "movieverse_bot_session")

app = Client(
    session_path,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Firebase Realtime Database URL
FIREBASE_URL = "https://movieverse-hub-default-rtdb.firebaseio.com"

# ✅ CORRECTED: Function to get movie mappings from Firebase (CORRECT NODE!)
def get_movie_mappings():
    """Fetch movie message ID mappings from Firebase movie_mappings node"""
    try:
        # ✅ CORRECT: Read from movie_mappings/ not movies/
        url = f"{FIREBASE_URL}/movie_mappings.json"
        logger.info(f"🔥 Fetching movie mappings from: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            mappings = response.json()
            if mappings:
                logger.info(f"✅ Loaded {len(mappings)} movie mappings from Firebase")
                logger.info(f"📋 Available codes: {list(mappings.keys())[:10]}...")  # Show first 10
                return mappings
            else:
                logger.warning("⚠️ movie_mappings node is empty")
        else:
            logger.error(f"❌ Firebase returned status: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Error loading from Firebase: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Fallback to hardcoded movies if Firebase fails
    logger.warning("⚠️ Using fallback hardcoded movie list")
    return {
        "msg_5": 5,
        "msg_9": 9,
        "msg_11": 11,
        "msg_12": 12,
        "msg_15": 15,
        "msg_17": 17,
    }

# Function to check if user is member of force subscribe channel
async def check_user_membership(client: Client, user_id: int) -> bool:
    """Check if user is a member of the force subscribe channel"""
    if not ENABLE_FORCE_SUBSCRIBE:
        logger.info(f"Force subscribe disabled, allowing user {user_id}")
        return True

    try:
        logger.info(f"Checking membership for user {user_id} in {FORCE_SUBSCRIBE_CHANNEL}")
        member = await client.get_chat_member(FORCE_SUBSCRIBE_CHANNEL, user_id)
        logger.info(f"User {user_id} status: {member.status}")

        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            logger.info(f"✅ User {user_id} IS a member!")
            return True

        logger.info(f"❌ User {user_id} is NOT a member")
        return False
    except UserNotParticipant:
        logger.info(f"❌ User {user_id} has not joined the channel")
        return False
    except (ChatAdminRequired, ChannelPrivate) as e:
        logger.error(f"⚠️ BOT PERMISSION ERROR: {e}")
        return True  # Allow as fallback
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return True  # Allow on error

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    """Handle /start command and deep links"""
    
    logger.info(f"📨 Received /start from user {message.from_user.id}")
    
    if len(message.command) > 1:
        movie_code = message.command[1]
        logger.info(f"🎬 Movie code requested: {movie_code}")
        
        # Refresh movie list from Firebase on each request
        movies = get_movie_mappings()
        
        if movie_code in movies:
            msg_id = movies[movie_code]
            logger.info(f"✅ Found movie code: {movie_code} → Message ID: {msg_id}")
            
            # Check force subscribe
            if ENABLE_FORCE_SUBSCRIBE:
                is_member = await check_user_membership(client, message.from_user.id)
                
                if not is_member:
                    # Show join channel message
                    keyboard = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "📢 Join Channel",
                                url=f"https://t.me/{FORCE_SUBSCRIBE_CHANNEL.replace('@', '')}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "✅ I Joined! Check Again",
                                callback_data=f"check_{movie_code}"
                            )
                        ]
                    ])
                    
                    await message.reply(
                        "🎬 **LumiFlix** 🎬\n"
                        "━━━━━━━━━━━━━━━━━━━\n\n"
                        "🎭 **Welcome to LumiFlix!**\n"
                        "Your ultimate destination for movies! 🍿\n\n"
                        "🔐 **Quick Access Required!**\n"
                        "Join our exclusive channel to unlock:\n"
                        "✨ Unlimited movie downloads\n"
                        "🎥 HD quality content\n"
                        "⚡ Instant delivery\n"
                        "🆕 Latest releases\n\n"
                        f"📢 **Channel:** {FORCE_SUBSCRIBE_CHANNEL}\n\n"
                        "━━━━━━━━━━━━━━━━━━━\n"
                        "**📋 Simple Steps:**\n\n"
                        "1️⃣ Tap 'Join Channel' below\n"
                        "2️⃣ Hit the JOIN button\n"
                        "3️⃣ Return & tap 'I Joined!'\n"
                        "4️⃣ Movie auto-downloads! 🎬\n\n"
                        "━━━━━━━━━━━━━━━━━━━\n\n"
                        "💫 **It takes just 10 seconds!**\n"
                        "🎉 **Enjoy unlimited entertainment!**",
                        reply_markup=keyboard
                    )
                    return
            
            # User is member or force subscribe disabled - send movie
            try:
                logger.info(f"📤 Forwarding message {msg_id} to user {message.from_user.id}")
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=CHANNEL_ID,
                    message_id=msg_id
                )
                logger.info(f"✅ Movie sent successfully!")
                
                await message.reply(
                    "🎬 **Movie Delivered!**\n\n"
                    "✅ Your movie has been sent successfully!\n"
                    "🍿 Enjoy watching!\n\n"
                    "━━━━━━━━━━━━━━━━\n"
                    "💫 **LumiFlix** - Your entertainment destination!"
                )
            except Exception as e:
                logger.error(f"❌ Error forwarding movie: {e}")
                await message.reply(
                    "❌ **Oops! Something went wrong**\n\n"
                    "Unable to send the movie right now.\n"
                    "Please try again later or contact support.\n\n"
                    f"Error: `{str(e)}`"
                )
        else:
            # Movie not found
            logger.warning(f"❌ Movie code '{movie_code}' not found in Firebase")
            logger.info(f"📋 Available codes: {list(movies.keys())}")
            
            await message.reply(
                "❌ **Movie not found!**\n\n"
                f"Code: `{movie_code}`\n\n"
                "Please use the **MovieVerse app** to browse and request available movies.\n\n"
                "📱 Download the app for the best experience!"
            )
    else:
        # No movie code - show welcome message
        await message.reply(
            "🎬 **Welcome to LumiFlix!** 🍿\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "🎭 **Your Entertainment Gateway!**\n\n"
            "This bot delivers movies directly from the LumiFlix app.\n\n"
            "📱 **How to use:**\n"
            "1️⃣ Download the **LumiFlix app**\n"
            "2️⃣ Browse movies\n"
            "3️⃣ Tap 'Download' button\n"
            "4️⃣ Movie arrives here automatically!\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "🌟 **Features:**\n"
            "✨ Instant delivery\n"
            "🎥 HD quality\n"
            "🆕 Latest releases\n"
            "📚 Huge library\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "💫 **Get started now!**\n"
            "Download the LumiFlix app to begin! 🚀"
        )

@app.on_callback_query(filters.regex(r"^check_"))
async def check_callback_handler(client: Client, callback_query: CallbackQuery):
    """Handle 'I Joined! Check Again' button callback"""
    
    movie_code = callback_query.data.replace("check_", "")
    logger.info(f"🔄 User {callback_query.from_user.id} clicked check for movie: {movie_code}")
    
    # Check membership again
    is_member = await check_user_membership(client, callback_query.from_user.id)
    
    if is_member:
        # User is now a member - send movie
        movies = get_movie_mappings()
        
        if movie_code in movies:
            msg_id = movies[movie_code]
            
            try:
                logger.info(f"✅ User verified! Sending message {msg_id}")
                
                await client.copy_message(
                    chat_id=callback_query.message.chat.id,
                    from_chat_id=CHANNEL_ID,
                    message_id=msg_id
                )
                
                await callback_query.answer("✅ Verified! Movie sent!", show_alert=True)
                
                await callback_query.message.reply(
                    "🎬 **Movie Delivered!**\n\n"
                    "✅ Thank you for joining!\n"
                    "🍿 Enjoy your movie!\n\n"
                    "━━━━━━━━━━━━━━━━\n"
                    "💫 **LumiFlix Hub** - Your entertainment destination!"
                )
                
                # Delete the join message
                try:
                    await callback_query.message.delete()
                except:
                    pass
                    
            except Exception as e:
                logger.error(f"❌ Error sending movie: {e}")
                await callback_query.answer("❌ Error sending movie", show_alert=True)
        else:
            await callback_query.answer("❌ Movie not found", show_alert=True)
    else:
        # User still not a member
        await callback_query.answer(
            "❌ You haven't joined the channel yet!\n\n"
            "Please join and try again.",
            show_alert=True
        )

# Run the bot
if __name__ == "__main__":
    logger.info("🚀 Starting LumiFlix Bot...")
    logger.info(f"📡 Force Subscribe: {'ENABLED' if ENABLE_FORCE_SUBSCRIBE else 'DISABLED'}")
    logger.info(f"📢 Channel: {FORCE_SUBSCRIBE_CHANNEL}")
    logger.info(f"🔥 Firebase URL: {FIREBASE_URL}")
    
    # Test Firebase connection on startup
    movies = get_movie_mappings()
    if movies:
        logger.info(f"✅ Firebase connection successful! {len(movies)} movie codes loaded")
        logger.info(f"📋 Sample codes: {list(movies.keys())[:5]}")
    else:
        logger.warning("⚠️ No movie codes loaded from Firebase - check connection!")
    
    app.run()
    logger.info("👋 Bot stopped")
