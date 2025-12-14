import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
bot = commands.Bot(command_prefix='$', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
        print(f'Logged in as {bot.user}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="convert-weight", description="Convert kg to lb and lb to kg")
@app_commands.describe(
    number="The number to convert",
    unit="Unit to convert from"
)
@app_commands.choices(unit=[
    app_commands.Choice(name="Kilograms (kg)", value="kg"),
    app_commands.Choice(name="Pounds (lb)", value="lb")
])
async def convert_weight(interaction: discord.Interaction, number: float, unit: str):
    if unit.lower() == "lb":
        await interaction.response.send_message(f"{number}lb is {number * 0.453592:.2f}kg")
    elif unit.lower() == "kg":
        await interaction.response.send_message(f"{number}kg is {number / 0.453592:.2f}lb")

@bot.tree.command(name="convert-height", description="Convert ft to m and m to ft")
@app_commands.describe(
    number="The length to convert",
    unit="Unit to convert from"
)
@app_commands.choices(unit=[
    app_commands.Choice(name="Feet (ft)", value="ft"),
    app_commands.Choice(name="Meter (m)", value="m")
])
async def convert_height(interaction: discord.Interaction, unit :str,  number: str):
    if unit == "m":
        meters = float(number)
        total_feet = meters * 3.28084
        feet = int(total_feet)
        inches = (total_feet - feet) * 12
        await interaction.response.send_message(f"{number}m = {total_feet:.2f}ft = {feet}'{inches:.2f}ft")
    elif unit == "ft":
        parts = number.replace("'", " ").replace('"', '').split()
        ft = int(parts[0])  # Convert to int
        inch = int(parts[1]) if len(parts) > 1 else 0
        
        total_feet = ft + (inch / 12)
        meters = total_feet * 0.3048
        await interaction.response.send_message(f"{"'".join(parts)}ft is {meters:.2f}m")

@bot.tree.command(name="1rm-calculator", description="1 rep max calculator!")
@app_commands.describe(
    weight="The weight (doesnt matter what metric)",
    reps="Amount of reps"
)
async def one_rm(interaction : discord.Interaction, weight: float, reps: int):
    await interaction.response.send_message(f"Estimated one-rep max: {weight * (1 + 0.0333 * reps):.2f}kg/lb")

@bot.tree.command(name="suggestion", description="Submit a suggestion to improve the server")
@app_commands.describe(suggestion_text="Your suggestion")
async def suggestion(interaction: discord.Interaction, suggestion_text: str):
    os.makedirs('suggestions', exist_ok=True)
    with open(f"suggestions/{interaction.user.name}.txt", "a") as f:
        f.write(f"{suggestion_text}\n\n")
    await interaction.response.send_message("Saved suggestion", ephemeral=True)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandInvokeError):
        await interaction.response.send_message(
            f"An error occurred: {str(error)}", 
            ephemeral=True
        )
        print(f"Error: {error}")
    else:
        await interaction.response.send_message(
            f"Something went wrong!", 
            ephemeral=True
        )

bot.run(TOKEN)
