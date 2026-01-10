import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. أمر الملف الشخصي بالسلاش
    @app_commands.command(name="profile", description="عرض معلومات حسابك")
    async def profile(self, interaction: discord.Interaction):
        user = interaction.user
        embed = discord.Embed(title="👤 ملف المستخدم", color=discord.Color.blue())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="الاسم", value=user.name, inline=True)
        embed.add_field(name="المعرف (ID)", value=user.id, inline=True)
        await interaction.response.send_message(embed=embed)

    # 2. أمر معلومات السيرفر بالسلاش
    @app_commands.command(name="server", description="عرض معلومات السيرفر الحالية")
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"🏰 معلومات {guild.name}", color=discord.Color.green())
        embed.add_field(name="عدد الأعضاء", value=guild.member_count)
        embed.add_field(name="التوثيق", value="موثق" if guild.verified else "غير موثق")
        await interaction.response.send_message(embed=embed)

    # 3. أمر المساعدة بالسلاش
    @app_commands.command(name="help", description="قائمة أوامر البوت")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message("الأوامر المتاحة حالياً:\n- `/profile`: لعرض ملفك\n- `/server`: لمعلومات السيرفر", ephemeral=True)

async def setup(bot):
    await bot.add_cog(General(bot))
