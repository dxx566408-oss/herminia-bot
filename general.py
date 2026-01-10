import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # أمر البروفايل الذكي
    @app_commands.command(name="profile", description="عرض الملف الشخصي لك أو لشخص آخر")
    @app_commands.describe(member="اختر العضو الذي تريد رؤية ملفه (اختياري)")
    async def profile(self, interaction: discord.Interaction, member: discord.Member = None):
        # المنطق الذي طلبته: إذا لم يختر عضواً، استخدم صاحب الأمر نفسه
        user = member or interaction.user
        
        embed = discord.Embed(
            title=f"👤 ملف: {user.display_name}",
            color=discord.Color.blue()
        )
        
        # عرض صورة الشخص (صورتك أو صورة الممنشن)
        embed.set_image(url=user.display_avatar.url)
        
        # إضافة معلومات إضافية اختيارية
        embed.add_field(name="الاسم الكامل", value=user.name, inline=True)
        embed.add_field(name="المعرف (ID)", value=f"`{user.id}`", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
