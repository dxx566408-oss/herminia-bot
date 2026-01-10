@app_commands.command(name="avatar", description="عرض صورة الحساب الخاصة بك أو لشخص آخر")
@app_commands.describe(user="اختر الشخص الذي تريد رؤية صورته")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        # تحديد الشخص المستهدف (صاحب الصورة)
        target = user or interaction.user
        
        # إنشاء البطاقة (Embed)
        embed = discord.Embed(
            title=f"🖼️ صورة: {target.display_name}",
            color=discord.Color.blue()
        )
        
        # عرض الصورة الكبيرة
        embed.set_image(url=target.display_avatar.url)
        
        # --- هذا هو السطر الذي يضيف "طلب بواسطة" في الأسفل ---
        embed.set_footer(
            text=f"طلب بواسطة: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url # يضع صورتك الصغيرة بجانب النص
        )
        
        await interaction.response.send_message(embed=embed)
