from telegram import Bot,InlineKeyboardButton,InlineKeyboardMarkup
import config
bot = Bot(token=config.TOKEN)
        #bot.send_message(chat_id=path, text="Deposited "+str(int(request.json["amount"]/1000))+"sats!")
keyboard = [
        [
            InlineKeyboardButton("Get Code", callback_data="check_sms"),
        ]
        ]
reply_markup = InlineKeyboardMarkup(keyboard)
bot.edit_message_text(inline_message_id="", text= "Send verification code to this phone number: +" , reply_markup=reply_markup)
