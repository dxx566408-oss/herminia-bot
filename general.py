@app_commands.command(name="avatar", description="عرض صورة الحساب الخاصة بك أو لشخص آخر")
    @app_commands.describe(user="اختر الشخص الذي تريد رؤية صورته")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        # الشخص المراد عرض صورته
        target = user or interaction.user
        
        # إنشاء البطاقة
        embed = discord.Embed(
            title=f"🖼️ صورة: {target.display_name}",
            color=discord.Color.blue()
        )
        
        # وضع الصورة الكبيرة
        embed.set_image(url=target.display_avatar.url)
        
        # إضافة اسم الشخص الذي طلب الأمر في الأسفل بخط صغير
        embed.set_footer(
            text=f"طلب بواسطة: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )
        
        await interaction.response.send_message(embed=embed)
