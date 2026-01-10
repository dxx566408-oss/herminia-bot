import discord
from discord.ext import commands
from discord import app_commands # مكتبة أوامر السلاش

class ProfileView(discord.ui.View): # كلاس خاص بالأزرار
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="صورة الحساب", style=discord.ButtonStyle.primary, emoji="🖼️")
    async def avatar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(interaction.user.display_avatar.url, ephemeral=True)

    @discord.ui.button(label="تاريخ الانضمام", style=discord.ButtonStyle.success, emoji="📅")
    async def join_date_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        date = interaction.user.joined_at.strftime("%Y-%m-%d")
        await interaction.response.send_message(f"لقد انضممت للسيرفر في: {date}", ephemeral=True)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # تعريف أمر السلاش /profile
    @app_commands.command(name="profile", description="عرض ملفك الشخصي مع أزرار التحكم")
    async def profile(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"الملف الشخصي لـ {interaction.user.name}",
            description="اختر أحد الأزرار أدناه للحصول على معلومات إضافية:",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        # إرسال الرسالة مع الأزرار
        await interaction.response.send_message(embed=embed, view=ProfileView())

async def setup(bot):
    await bot.add_cog(General(bot))
