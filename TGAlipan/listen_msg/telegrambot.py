from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# 你的Telegram机器人Token
TOKEN = "7331438236:AAEkhCXcehRkSQeH94IgHKIh-QYmJd0hFLE"

# /start命令的处理函数
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! I am your bot. How can I help you?')

# 回声处理函数，回复收到的每一条文本消息
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

# 主函数，初始化并启动机器人
def main():
    # 创建Application对象，并传入机器人Token
    application = ApplicationBuilder().token(TOKEN).build()

    # 添加命令处理程序
    application.add_handler(CommandHandler('start', start))

    # 添加消息处理程序
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 启动轮询
    application.run_polling()

if __name__ == '__main__':
    main()
