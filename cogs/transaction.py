from discord.ext import commands
from utils.database import get_db_connection
from datetime import datetime


class Transactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Transactions Cog is Active")
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Marks a task as completed. Usage: !didit <task_id>",
                          aliases=['di']  # This must be a list or tuple of strings    
                      )
    async def didit(self, ctx, task_id: int):
        try:
            conn = get_db_connection()
            c = conn.cursor()
            # Get task details
            c.execute('SELECT task_name, points, requires_verification FROM tasks WHERE id = ?', (task_id,))
            task = c.fetchone()
            #print(str(task))    
            if not task:
                await ctx.send(f"Task ID {task_id} not found.")
                conn.close()
                return

            task_name, points, requires_verification = task
            print(task_name)
            print(str(points))

        except Exception as e:
            print(f"(e1) An error occurred when trying to get task details: {e} \n")
            await ctx.send(f"An error occurred (e1): {e}")

        try:    
            # Get user details
            c.execute('SELECT id FROM users WHERE discord_id = ?', (str(ctx.author.id),))
            user = c.fetchone()
            

            if not user:
                # If user does not exist, create a new entry
                c.execute('INSERT INTO users (discord_id, user_name, role) VALUES (?, ?, ?)',
                      (str(ctx.author.id), str(ctx.author), 'user'))
                conn.commit()
                c.execute('SELECT id FROM users WHERE discord_id = ?', (str(ctx.author.id),))
                user = c.fetchone()

            user_id = user[0]
        except Exception as e:
            print(f"(e2)An error occurred when trying to get user details: {e}")
            await ctx.send(f"An error occurred (e2): {e}")
        
        # Insert transaction
        try:

            print("Requires verification: " + str(requires_verification))
            transaction_pending = requires_verification
            c.execute('INSERT INTO transactions (user_id, change, transaction_reason, transaction_pending, transaction_datetime) VALUES (?, ?, ?, ?, ?)',
                      (user_id, points, f'Completed task {task_name}', transaction_pending, datetime.now()))
            conn.commit()
        except Exception as e:
            print(f"(e3)An error occurred: {e}")
            await ctx.send(f"An error occurred (e3): {e}")

        #finally:
        #    conn.close()

        # Calculate total points
        c.execute('SELECT SUM(change) FROM transactions WHERE user_id = ? AND transaction_pending = 0', (user_id,))
        total_points = c.fetchone()[0] or 0

        # Send response
        print("Getting ready for transaction statement")
        if transaction_pending:
            await ctx.send(f'{ctx.author.name} now has {total_points} points. The latest transaction requested is "{task_name}" (Task ID: {task_id}) and it\'s not added to your statement as it is waiting for verification.')
        else:
            await ctx.send(f'{ctx.author.name} now has {total_points} points. The latest transaction requested is "{task_name}" (Task ID: {task_id}) and it\'s added to your statement.')

        conn.close()

    @commands.command(help="Shows all your transactions with a summary of your points. Usage: !mypoints",
                          aliases=['mp']  # This must be a list or tuple of strings    
                      )
    async def mypoints(self, ctx):
        conn = get_db_connection()
        c = conn.cursor()

        try:
            # Get user details
            #print("Fetching user details...")
            c.execute('SELECT id FROM users WHERE discord_id = ?', (str(ctx.author.id),))
            user = c.fetchone()
            #print(f"User: {user}")

            if not user:
                await ctx.send("You have no transactions recorded.")
                return

            user_id = user[0]

            # Get all transactions for the user
            #print("Fetching transactions...")
            c.execute('SELECT transaction_datetime, change, transaction_reason, transaction_pending FROM transactions WHERE user_id = ?', (user_id,))
            transactions = c.fetchall()
            #print(f"Transactions: {transactions}")

            if not transactions:
                await ctx.send("You have no transactions recorded.")
                return

            # Calculate points
            #print("Calculating points...")
            c.execute('SELECT SUM(change) FROM transactions WHERE user_id = ? AND transaction_pending = 0', (user_id,))
            usable_points = c.fetchone()[0] or 0

            c.execute('SELECT SUM(change) FROM transactions WHERE user_id = ? AND transaction_pending = 1', (user_id,))
            pending_points = c.fetchone()[0] or 0

            total_points = usable_points + pending_points

            # Format the response
            response = f"Transaction history for {ctx.author.name}:\n"
            response += "```\n"
            response += "{:<22} {:<8} {:<40} {:<10}\n".format("Date/Time", "Change", "Reason", "Pending")
            response += "-" * 80 + "\n"
            for trans in transactions:
                date_time, change, reason, pending = trans
                #datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
                #response += "{:<20} {:<10} {:<30} {:<10}\n".format(date_time, change, reason, "Yes" if pending else "No")
                response += "{:<22} {:<8.1f} {:<40} {:<10}\n".format(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"), change, reason, "Yes" if pending else "No")

            response += "-" * 80 + "\n"
            response += f"Usable points: {usable_points:.1f}\n"
            response += f"Pending points: {pending_points:.1f}\n"
            response += f"Total points: {total_points:.1f}\n"
            response += "```"

            await ctx.send(response)
        except Exception as e:
            print(f"(e4) An error occurred when getting your point status: {e}")
            await ctx.send(f"An error occurred (e4) point status: {e}")
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Transactions(bot))