import discord

from discord.ext import tasks

from discord.ui import Button, View

intents = discord.Intents.default()

intents.guilds = True

intents.members = True

intents.messages = True

intents.message_content = True

bot = discord.Bot(intents=intents)

GUILD_ID = 1396269262599094393

CATEGORY_ID = 1398693106689380493

TARGET_CHANNEL_ID = 1397436260997402776
RAINBOW_COLORS = [
    "#B40202", "#AF0000", "#AA0000", "#A50000", "#A00000",

    "#9B0000", "#960000", "#910000", "#8C0000", "#870000",

    "#820000", "#7D0000", "#780000", "#730000", "#6E0000",

    "#690000", "#640000", "#5F0000", "#5A0000", "#550000",

    "#500000", "#4B0000", "#460000", "#410000", "#3C0000",

    "#370000", "#320000", "#2D0000", "#280000", "#230000",

    "#1E0000", "#190000", "#140000", "#0F0000", "#0A0000"

]

active_tickets = {}

embed_message = None

color_index = 0

stored_view = None  # view që do ta ruajmë për më vonë

def hex_to_color(hex_str):

    hex_str = hex_str.lstrip('#')

    return discord.Color(int(hex_str, 16))

@bot.event

async def on_ready():

    print(f"✅ Bot u kyç si: {bot.user}")

    await send_rainbow_embed()

    change_color.start()

async def send_rainbow_embed():

    global embed_message, stored_view

    channel = bot.get_channel(TARGET_CHANNEL_ID)

    if not channel:

        print("⛔ Kanali nuk u gjet")

        return

    embed = discord.Embed(

        title=" <:emoji_1:1398708022439706664> TrimoO - Support System",

        description=(

            "Hapni një ticket për:\n"

            "• Raportime 📌\n"

            "• Pyetje ❓\n"

            "• Ndihmë teknike 🛠️\n\n"

            "🎫 **Klikoni butonin më poshtë për të hapur një ticket!**\n\n"

            "**📋 Si funksionon**\n"

            "• Klikoni \"Krijo Ticket\"\n"

            "• Do të krijohet një kanal privat\n"

            "• Shpjegoni problemin tuaj\n"

            "• Stafi do t'ju ndihmojë"

        ),

        color=hex_to_color(RAINBOW_COLORS[0])

    )

    # Krijo butonin dhe vendos callback

    button = Button(label="🎫 Krijo Ticket", style=discord.ButtonStyle.secondary)

    async def button_callback(interaction: discord.Interaction):

        user = interaction.user

        if user.id in active_tickets:

            existing_channel = bot.get_channel(active_tickets[user.id])

            if existing_channel:

                await interaction.response.send_message(

                    f"⛔ Ju tashmë keni një ticket: {existing_channel.mention}", ephemeral=True

                )

                return

            else:

                del active_tickets[user.id]

        guild = interaction.guild

        category = discord.utils.get(guild.categories, id=CATEGORY_ID)

        overwrites = {

            guild.default_role: discord.PermissionOverwrite(view_channel=False),

            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),

            guild.me: discord.PermissionOverwrite(view_channel=True)

        }

        ticket_channel = await guild.create_text_channel(

            name=f"ticket-{user.name}",

            overwrites=overwrites,

            category=category

        )

        active_tickets[user.id] = ticket_channel.id

        # Butoni për mbyllje

        close_btn = Button(label="🔒 Mbyll Ticket", style=discord.ButtonStyle.secondary)

        async def close_callback(close_inter):

            if close_inter.user != user:

                await close_inter.response.send_message("⛔ Vetëm ti mund ta mbyllësh këtë ticket.", ephemeral=True)

                return

            await ticket_channel.delete()

            del active_tickets[user.id]

        view_close = View()

        close_btn.callback = close_callback

        view_close.add_item(close_btn)

        await ticket_channel.send(

            content=f"{user.mention} 📩 Faleminderit që hapët një ticket!\nStafi do t'ju ndihmojë së shpejti.",

            view=view_close

        )

        await interaction.response.send_message(f"✅ Ticket u krijua: {ticket_channel.mention}", ephemeral=True)

    # Vendos butonin në view

    view = View()

    button.callback = button_callback

    view.add_item(button)

    stored_view = view  # ruaj view për me e përdor në ndryshim ngjyrash

    embed_message = await channel.send(embed=embed, view=view)

@tasks.loop(seconds=3)

async def change_color():

    global color_index, embed_message, stored_view

    if embed_message:

        try:

            hex_color = RAINBOW_COLORS[color_index]

            color = hex_to_color(hex_color)

            embed = embed_message.embeds[0]

            new_embed = discord.Embed(

                title=embed.title,

                description=embed.description,

                color=color

            )

            await embed_message.edit(embed=new_embed, view=stored_view)

            color_index = (color_index + 1) % len(RAINBOW_COLORS)

        except Exception as e:

            print("❌ Error në change_color:", e)

bot.run("MTM5ODgwODM4MDgzOTE3MDA1OA.GovTtk.MIH2NYAtBLiySe7bUK2P_7IkMwKDyeZnQgahZk")