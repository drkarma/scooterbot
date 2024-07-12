from discord.ext import commands
from utils.database import get_db_connection

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Rewards Cog is Active")

   
    @commands.command(
        help="Use this command to add a new reward attr1 <name of reward> attr2 <description> attr3 <points> attr4 <is it a minuterate - True/False>"
    )
   
    async def add_reward(self, ctx, reward_name: str, reward_description: str , cost: float, reward_rate: bool):
        #print ("Hej \n\n")
        reward_author = str(ctx.author)
        # conn = get_db_connection()
        # c = conn.cursor()
        # c.execute('INSERT INTO tasks (task_name, task_description, points, requires_verification) VALUES (?, ?, ?, ?)',
        #     (task_name, task_description, points, requires_verification))
        # conn.commit()
        # conn.close()
        # await ctx.send(f'Task {task_name} added with {points} points.')
        
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO rewards (reward_name, reward_description, reward_contributor, cost, reward_rate) VALUES (?, ?, ?, ?, ?)',
                      (reward_name, reward_description, reward_author, cost, reward_rate))
            conn.commit()
            conn.close()
            if reward_rate:
                await ctx.send(f'Reward Rate (cost per minute) {reward_name} added with {cost} cost. by {reward_author}')
            else:
                await ctx.send(f'Reward {reward_name} added with {cost} cost. by {reward_author}')

        else:
            await ctx.send('You do not have permission to add rewards.')
    @commands.command(
        help="Deletes a reward. Usage: !delete_reward <task_id>"
    )

    async def delete_reward(self, ctx, ent_id: int):
        """
        Deletes a reward.

        Arguments:
        task_id -- The ID of the task to delete.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('DELETE FROM rewards WHERE id = ?', (ent_id,))
            if c.rowcount == 0:
                await ctx.send(f"Reward ID {ent_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Reward ID {ent_id} has been deleted.')
            conn.close()
        else:
            await ctx.send('You do not have permission to delete rewards.')
    
    @commands.command(
        help="Updates an existing rewards. Usage: !update_reward <ent_id> <name> <cost> <reward_Rate True/False>"
    )
    
    async def update_reward(self, ctx, ent_id: int, name: str, cost: float, reward_rate: bool):
        """
        Updates an existing reward.

        Arguments:
        ent_id -- The ID of the reward to update.
        name -- The new name of the reward.
        cost -- The new cost for the reward.
        reward_rate -- True if reward is a cost per minute.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE rewards SET reward_name = ?, cost = ?, reward_Rate = ? WHERE id = ?',
                      (name, cost, reward_rate, ent_id))
            if c.rowcount == 0:
                await ctx.send(f"Reward ID {ent_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Reward ID {ent_id} updated to {name} with {cost} points and reward_rate: {reward_rate}.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update rewards.')

    @commands.command(
        help="Lists all available rewards."
    )
    async def list_rewards(self, ctx):
        """
        Lists all rewards.
        """
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, reward_name, reward_description, cost, reward_rate FROM rewards')
        rewards = c.fetchall()
        conn.close()

        if rewards:
            response = "```\n"
            response += "{:<4} {:<20} {:<30} {:<10} {:<10}\n".format("ID", "Name", "Description", "cost", "cost/minute")
            response += "-" * 75 + "\n"
            for reward in rewards:
               # response += "{:<5} {:<20} {:<30} {:<10} {:<10}\n".format(reward[0], reward[1], reward[2], reward[3], reward[4])
                response += "{:<4} {:<20} {:<30} {:<10} ".format(reward[0], reward[1], reward[2], reward[3])
                if reward[4]:
                    response += "{:<6}\n".format("Yes")
                else:
                    response += "{:<6}\n".format("No")


            response += "```"
            await ctx.send(response)
        else:
            await ctx.send("No rewards found.")

        # if rewards:
        #     rewards_list = "\n".join([f"ID: {reward[0]}, Name: {reward[1]}, Description: {reward[2]}, Points: {reward[3]}, Cost is rate per minute?: {reward[4]}" for reward in rewards])
        #     await ctx.send(f"Rewards:\n{rewards_list}")
        # else:
        #     await ctx.send("No rewards found.")

    @commands.command(
        help="Updates the description of an existing task. Usage: !update_rewarddesc <ent_id> <new_description>"
    )
    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def update_rewarddesc(self, ctx, ent_id: int, *, new_description: str):
        """
        Updates the description of an existing task.

        Arguments:
        task_id -- The ID of the task to update.
        new_description -- The new description of the task.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE rewards SET reward_description = ? WHERE id = ?', (new_description, ent_id))
            if c.rowcount == 0:
                await ctx.send(f"Reward ID {ent_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Reward ID {ent_id} updated with new description.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update rewards.')

    @commands.command(
        help="Updates the name of an existing task. Usage: !update_taskname <task_id> <new_name>"
    )
    async def update_rewardname(self, ctx, ent_id: int, *, new_name: str):
        """
        Updates the description of an existing reward.

        Arguments:
        task_id -- The ID of the reward to update.
        new_description -- The new description of the reward.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE rewards SET reward_name = ? WHERE id = ?', (new_name, ent_id))
            if c.rowcount == 0:
                await ctx.send(f"Reward ID {ent_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Reward ID {ent_id} updated with new name.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update rewards.')
    
    @commands.command(
        help="Toggles the reward_rate of a reward. If true then it's a cost per minute Usage: !toggle_rewardisrate <task_id>"
    )
    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def toggle_rewardisrate(self, ctx, ent_id: int):
        """
        Toggles the verification requirement of a task.

        Arguments:
        ent_id  -- The ID of the reward to update.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('SELECT reward_rate FROM rewards WHERE id = ?', (ent_id,))
            entity = c.fetchone()
            if not entity:
                await ctx.send(f"Reward ID {ent_id} not found.")
                conn.close()
                return

            entity_value = not entity[0]
            c.execute('UPDATE rewards SET reward_rate = ? WHERE id = ?', (entity_value, ent_id))
            if c.rowcount == 0:
                await ctx.send(f"Reward ID {ent_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Reward ID {ent_id} verification requirement toggled to {entity_value}.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update rewards.')

async def setup(bot):
    await bot.add_cog(Rewards(bot))