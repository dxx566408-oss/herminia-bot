import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # أمر الأفاتار (عرض صورة الحساب)
    @app_commands.command(name="avatar", description="عرض صورة الحساب الخاصة بك أو لشخص آخر")
    @app_commands.describe(user="اختر الشخص الذي تريد رؤية صورته")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        # إذا لم يختر الشخص مستخدم، تظهر صورته هو
        target = user or interaction.user
        
        embed = discord.Embed(
            title=f"🖼️ صورة {target.display_name}",
            color=discord.Color.random() # يختار لون عشوائي في كل مرة
        )
        
        # عرض الصورة بجودتها الكاملة
        embed.set_image(url=target.display_avatar.url)
        
        # زر لتحميل الصورة (اختياري)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
