import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace with the HTTP API token you got from @BotFather
BOT_TOKEN = '8997186272:ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'-w'
bot = telebot.TeleBot(BOT_TOKEN)

# In-memory database to store player profiles and their active cards
# In production, you'll want to transition this to a database like SQLite or MongoDB
players_db = {}

def generate_bingo_card():
    """Generates a standard 5x5 Bingo matrix."""
    # Bingo columns: B (1-15), I (16-30), N (31-45), G (46-60), O (61-75)
    ranges = [
        (1, 15),   # B
        (16, 30),  # I
        (31, 45),  # N
        (46, 60),  # G
        (61, 75)   # O
    ]
    
    card = []
    for start, end in ranges:
        column = random.sample(range(start, end + 1), 5)
        card.append(column)
        
    # Transpose columns to rows to make it a standard grid
    rows = list(map(list, zip(*card)))
    
    # The center tile (Row 2, Column 2) is historically a "FREE" slot
    rows[2][2] = "❌" 
    return rows

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Player"
    
    # Register the user if they are new, giving them a 5-coin starting balance
    if user_id not in players_db:
        players_db[user_id] = {
            "username": username,
            "balance": 5,
            "current_card": None
        }
        welcome_text = f"Welcome to MK Online Bingo, {username}! 🎮\n\nWe've credited your wallet with a starting bonus of 5 coins. 💰"
    else:
        welcome_text = f"Welcome back to MK Online Bingo, {username}! 🎰\nYour current balance: {players_db[user_id]['balance']} coins."

    # Main Menu Navigation Buttons
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📄 Generate New Card", callback_data="generate_card"))
    markup.row(InlineKeyboardButton("💰 Check Balance", callback_data="check_balance"))
    
    bot.send_message(message.chat_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_menu_clicks(call):
    user_id = call.from_user.id
    
    if user_id not in players_db:
        bot.answer_callback_query(call.id, "Please type /start to initialize your profile.")
        return

    if call.data == "check_balance":
        balance = players_db[user_id]["balance"]
        bot.answer_callback_query(call.id, f"Your balance is: {balance} coins 🪙", show_alert=True)
        
    elif call.data == "generate_card":
        # Generate a fresh card matrix and save it to the player's session
        new_card = generate_bingo_card()
        players_db[user_id]["current_card"] = new_card
        
        # Displaying the card layout in text format
        card_display = "🎲 **YOUR BINGO CARD** 🎲\n`---------------------`\n` B   I   N   G   O `\n`---------------------`\n"
        for row in new_card:
            row_text = " ".join(f"{str(num).center(3)}" for num in row)
            card_display += f"`{row_text}`\n"
        card_display += "`---------------------`"
        
        bot.edit_message_text(card_display, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")

if __name__ == '__main__':
    print("Bot is up and running...")
    bot.infinity_polling()
