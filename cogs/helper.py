from discord.ext import commands
from utils.database import get_db_connection

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Helper Cog is Active")

    @commands.command()
    async def explain(self, ctx):
        buildstring = "Hej, jag är Scooterbot! Jag är en chattrobot som bor här i huset. Jag hjälper dig"
        buildstring = buildstring + "\nhålla koll på dina poäng som du kan använda till att exempelvis få scooterminuter, "
        buildstring = buildstring + "\neller lösa in mot andra belöningar. Tips är att kolla med kommandot !rewards för mer info "

        await ctx.send(buildstring)
        
   
async def setup(bot):
    await bot.add_cog(Helper(bot))