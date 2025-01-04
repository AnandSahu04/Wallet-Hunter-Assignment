from telegram import Update
from telegram.ext import ContextTypes
from ..db.models import Task, User, TaskStatus
from ..services.task_service import TaskService
from ..auth.admin_auth import admin_required

class TaskBotHandlers:
    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    @admin_required
    async def create_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Format: /create_task @username task description
            args = context.args
            if len(args) < 2:
                await update.message.reply_text("Usage: /create_task @username task description")
                return

            username = args[0].replace("@", "")
            task_description = " ".join(args[1:])
            
            task = await self.task_service.create_task(username, task_description)
            await update.message.reply_text(f"Task created successfully! Task ID: {task.task_id}")
            
        except Exception as e:
            await update.message.reply_text(f"Error creating task: {str(e)}")

    async def list_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user_id = update.effective_user.id
            tasks = await self.task_service.get_user_tasks(user_id)
            
            if not tasks:
                await update.message.reply_text("You have no tasks assigned.")
                return

            response = "Your tasks:\n\n"
            for task in tasks:
                response += f"ID: {task.task_id}\nDescription: {task.task_description}\nStatus: {task.status.value}\n\n"
            
            await update.message.reply_text(response)
            
        except Exception as e:
            await update.message.reply_text(f"Error listing tasks: {str(e)}")

    async def update_task_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Format: /update_status task_id new_status
            args = context.args
            if len(args) != 2:
                await update.message.reply_text("Usage: /update_status task_id status")
                return

            task_id = int(args[0])
            new_status = args[1].upper()
            user_id = update.effective_user.id
            
            await self.task_service.update_task_status(task_id, user_id, TaskStatus[new_status])
            await update.message.reply_text("Task status updated successfully!")
            
        except Exception as e:
            await update.message.reply_text(f"Error updating task status: {str(e)}")