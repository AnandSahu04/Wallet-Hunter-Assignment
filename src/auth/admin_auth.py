from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from ..db.models import User

def admin_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        user = context.bot_data.get('db').query(User).filter(User.user_id == user_id).first()
        
        if not user or not user.is_admin:
            await update.message.reply_text("This command is only available to admins.")
            return
        
        return await func(self, update, context, *args, **kwargs)
    return wrapper