import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # هذا الأمر سيظهر تماماً كما في صورتك مع خيار "user"
    @app_commands.command(name="profile", description="عرض الملف الشخصي")
    @app_commands.describe(user="اختر الشخص الذي تريد عرض ملفه") # الوصف الذي يظهر للمستخدم
    async def profile(self, interaction: discord.Interaction, user: discord.Member = None):
        # إذا لم يتم اختيار مستخدم، يعرض بروفايل الشخص الذي كتب الأمر
        target = user or interaction.user
        
        embed = discord.Embed(
            title=f"👤 ملف {target.display_name}",
            color=discord.Color.blue()
        )
        
        # وضع الصورة كبيرة كما اتفقنا
        embed.set_image(url=target.display_avatar.url)
        
        # إضافة التاريخ والمعلومات الأساسية
        embed.add_field(name="الاسم", value=target.name, inline=True)
        embed.add_field(name="انضم للديسكورد", value=target.created_at.strftime("%Y-%m-%d"), inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
