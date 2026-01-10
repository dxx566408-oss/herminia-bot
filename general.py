import discord
from discord.ext import commands
import time

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # أمر لمعرفة سرعة اتصال البوت (Ping)
    @commands.command(name="بنق")
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send("جاري الفحص... ⏳")
        end_time = time.time()
        
        # حساب سرعة الاستجابة بالملي ثانية
        ping_ms = round((end_time - start_time) * 1000)
        await message.edit(content=f"🚀 سرعة الاستجابة: {ping_ms}ms\n📡 الحالة: متصل ومستقر")

    # أمر لعرض معلومات السيرفر
    @commands.command(name="سيرفر")
    async def server_info(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"معلومات {guild.name}", color=discord.Color.blue())
        embed.add_field(name="عدد الأعضاء", value=guild.member_count, inline=True)
        embed.add_field(name="صاحب السيرفر", value=guild.owner, inline=True)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
