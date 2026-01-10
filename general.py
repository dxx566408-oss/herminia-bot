import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="عرض صورة الحساب")
    @app_commands.describe(user="اختر الشخص (اختياري)")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        embed = discord.Embed(title=f"🖼️ صورة: {target.display_name}", color=discord.Color.blue())
        embed.set_image(url=target.display_avatar.url)
        embed.set_footer(
            text=f"طلب بواسطة: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="profile", description="عرض الملف الشخصي")
    @app_commands.describe(user="اختر الشخص (اختياري)")
    async def profile(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        embed = discord.Embed(title=f"👤 ملف: {target.display_name}", color=discord.Color.blue())
        embed.set_image(url=target.display_avatar.url)
        embed.set_footer(
            text=f"طلب بواسطة: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
