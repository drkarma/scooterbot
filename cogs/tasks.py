from discord.ext import commands
from utils.database import get_db_connection

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Tasks Cog is Active")

    @commands.command()
    async def boi(self, ctx, love: bool=None):
        if love == None:
            await ctx.send(f'Ok. I understand you cant state if it is True or False')
        else:
            if love: 
                await ctx.send("Love you too!")
            else:
                await ctx.send(f"Don't you love me boi?")


    @commands.command(
        help="Use this command to add a new task it has arguments see description how to use it attr1 <name of task> attr2 <how many points> attr3 <need to be acknowledged - True/False>"
    )
   # @commands.has_role('taskadmin')  # Only users with the "taskadmin" role can use this command

    async def add_task(self, ctx, task_name: str, task_description: str , points: float, requires_verification: bool):
        print ("Hej \n\n")
        task_author = str(ctx.author)
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
            c.execute('INSERT INTO tasks (task_name, task_description, task_contributor, points, requires_verification) VALUES (?, ?, ?, ?, ?)',
                      (task_name, task_description, task_author, points, requires_verification))
            conn.commit()
            conn.close()
            await ctx.send(f'Task {task_name} added with {points} points. by {task_author}')
        else:
            await ctx.send('You do not have permission to add tasks.')
    @commands.command(
        help="Deletes a task. Usage: !delete_task <task_id>"
    )

    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def delete_task(self, ctx, task_id: int):
        """
        Deletes a task.

        Arguments:
        task_id -- The ID of the task to delete.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            if c.rowcount == 0:
                await ctx.send(f"Task ID {task_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Task ID {task_id} has been deleted.')
            conn.close()
        else:
            await ctx.send('You do not have permission to delete tasks.')
    
    @commands.command(
        help="Updates an existing task. Usage: !update_task <task_id> <name> <points> <requires_verification>"
    )
    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def update_task(self, ctx, task_id: int, name: str, points: float, requires_verification: bool):
        """
        Updates an existing task.

        Arguments:
        task_id -- The ID of the task to update.
        name -- The new name of the task.
        points -- The new points for the task.
        requires_verification -- The new verification requirement for the task.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE tasks SET task_name = ?, points = ?, requires_verification = ? WHERE id = ?',
                      (name, points, requires_verification, task_id))
            if c.rowcount == 0:
                await ctx.send(f"Task ID {task_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Task ID {task_id} updated to {name} with {points} points and verification requirement: {requires_verification}.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update tasks.')

    @commands.command(
        help="Lists all tasks."
    )
    async def list_tasks(self, ctx):
        """
        Lists all tasks.
        """
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, task_name, task_description, points, requires_verification FROM tasks')
        tasks = c.fetchall()
        conn.close()
        if tasks:
            response = "```\n"
            response += "{:<4} {:<20} {:<30} {:<10} {:<10}\n".format("ID", "Name", "Description", "points", "Approval")
            response += "-" * 75 + "\n"
            for task in tasks:
               # response += "{:<5} {:<20} {:<30} {:<10} {:<10}\n".format(reward[0], reward[1], reward[2], reward[3], reward[4])
                response += "{:<4} {:<20} {:<30} {:<10} ".format(task[0], task[1], task[2], task[3])
                if task[4]:
                    response += "{:<6}\n".format("Yes")
                else:
                    response += "{:<6}\n".format("No")
                    response += "```"
            await ctx.send(response)
        else:
            await ctx.send("No tasks found.")

        # if tasks:
        #     tasks_list = "\n".join([f"ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Points: {task[3]}, Verification Required: {task[4]}" for task in tasks])
        #     await ctx.send(f"Tasks:\n{tasks_list}")
        # else:
        #     await ctx.send("No tasks found.")

    @commands.command(
        help="Updates the description of an existing task. Usage: !update_taskdesc <task_id> <new_description>"
    )
    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def update_taskdesc(self, ctx, task_id: int, *, new_description: str):
        """
        Updates the description of an existing task.

        Arguments:
        task_id -- The ID of the task to update.
        new_description -- The new description of the task.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE tasks SET task_description = ? WHERE id = ?', (new_description, task_id))
            if c.rowcount == 0:
                await ctx.send(f"Task ID {task_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Task ID {task_id} updated with new description.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update tasks.')

    @commands.command(
        help="Updates the name of an existing task. Usage: !update_taskname <task_id> <new_name>"
    )
    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def update_taskname(self, ctx, task_id: int, *, new_name: str):
        """
        Updates the description of an existing task.

        Arguments:
        task_id -- The ID of the task to update.
        new_description -- The new description of the task.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('UPDATE tasks SET task_name = ? WHERE id = ?', (new_name, task_id))
            if c.rowcount == 0:
                await ctx.send(f"Task ID {task_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Task ID {task_id} updated with new name.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update tasks.')
    
    @commands.command(
        help="Toggles the verification requirement of a task. Usage: !toggle_validation <task_id>"
    )
    #@commands.has_role('parent')  # Only users with the "parent" role can use this command
    async def toggle_validation(self, ctx, task_id: int):
        """
        Toggles the verification requirement of a task.

        Arguments:
        task_id -- The ID of the task to update.
        """
        if ctx.author.guild_permissions.administrator:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('SELECT requires_verification FROM tasks WHERE id = ?', (task_id,))
            task = c.fetchone()
            if not task:
                await ctx.send(f"Task ID {task_id} not found.")
                conn.close()
                return

            requires_verification = not task[0]
            c.execute('UPDATE tasks SET requires_verification = ? WHERE id = ?', (requires_verification, task_id))
            if c.rowcount == 0:
                await ctx.send(f"Task ID {task_id} not found.")
            else:
                conn.commit()
                await ctx.send(f'Task ID {task_id} verification requirement toggled to {requires_verification}.')
            conn.close()
        else:
            await ctx.send('You do not have permission to update tasks.')

async def setup(bot):
    await bot.add_cog(Tasks(bot))