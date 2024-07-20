import sqlite3
from datetime import datetime

def insert_test_data():
    conn = sqlite3.connect('scooterbot.db')
    c = conn.cursor()

    # Insert 20 tasks
    tasks = [
        ("Sweep the floor", "Sweep the floor in the living room", 5.0, 3.5, True),
        ("Wash dishes", "Wash the dishes after dinner", 15.0, 10.5, True),
        ("Vacuum the house", "Vacuum all rooms in the house", 45.0, 31.5, True),
        ("Dust the shelves", "Dust all shelves in the living room", 10.0, 7.0, False),
        ("Take out trash", "Take out the trash to the bin outside", 5.0, 3.5, False),
        ("Clean bathroom", "Clean the bathroom including sink and toilet", 30.0, 21.0, True),
        ("Mop the floor", "Mop the floor in the kitchen", 20.0, 14.0, True),
        ("Wash clothes", "Wash a load of clothes", 10.0, 7.0, False),
        ("Fold clothes", "Fold the dried clothes and put them away", 15.0, 10.5, False),
        ("Clean windows", "Clean all windows in the living room", 30.0, 21.0, True),
        ("Water plants", "Water all indoor plants", 5.0, 3.5, False),
        ("Feed the cat", "Give food and water to the cat", 5.0, 3.5, False),
        ("Clean the fridge", "Clean the inside of the refrigerator", 20.0, 14.0, True),
        ("Organize bookshelf", "Organize and arrange books on the bookshelf", 10.0, 7.0, False),
        ("Change bed sheets", "Change and wash the bed sheets", 15.0, 10.5, True),
        ("Cook dinner", "Prepare and cook dinner", 60.0, 42.0, True),
        ("Clean kitchen counters", "Wipe and clean all kitchen counters", 10.0, 7.0, False),
        ("Rake leaves", "Rake the leaves in the garden", 30.0, 21.0, True),
        ("Clean the garage", "Organize and clean the garage", 45.0, 31.5, True),
        ("Wash the car", "Wash the car outside", 30.0, 21.0, True)
    ]

    for task in tasks:
        task_name, task_description, time_estimation, points, requires_verification = task
        c.execute('''
            INSERT INTO tasks (task_name, task_description, task_contributor, points, requires_verification)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_name, task_description, "TestMan", points, requires_verification))

    # Insert 20 rewards
    rewards = [
        ("Scooter time", "Spend time riding the scooter", 0.5, 0.5, True),
        ("Computer time", "Spend time on the computer", 0.5, 0.5, True),
        ("TV time", "Watch TV", 0.5, 0.5, True),
        ("Popcorn", "Get a bag of popcorn", 1.0, 1.0, False),
        ("Ice Cream", "Get a scoop of ice cream", 2.0, 2.0, False),
        ("Extra dessert", "Get an extra dessert after dinner", 1.0, 1.0, False),
        ("Movie night", "Watch a movie at home", 3.0, 3.0, False),
        ("Board game night", "Play a board game with family", 3.0, 3.0, False),
        ("Video game time", "Play video games", 0.5, 0.5, True),
        ("Stay up late", "Stay up 30 minutes past bedtime", 2.0, 2.0, False),
        ("Sleepover", "Have a sleepover with a friend", 5.0, 5.0, False),
        ("Pizza night", "Get a pizza night", 5.0, 5.0, False),
        ("Gift card", "Get a $10 gift card", 10.0, 10.0, False),
        ("Day off chores", "Get a day off from all chores", 7.0, 7.0, False),
        ("Picnic", "Go for a picnic", 4.0, 4.0, False),
        ("Camping trip", "Go for a camping trip", 15.0, 15.0, False),
        ("New toy", "Get a new toy", 8.0, 8.0, False),
        ("Book", "Get a new book", 5.0, 5.0, False),
        ("Park visit", "Visit the park for 1 hour", 2.0, 2.0, False),
        ("Bicycle time", "Spend time riding the bicycle", 0.5, 0.5, True)
    ]

    for reward in rewards:
        reward_name, reward_description, points, cost, reward_rate = reward
        c.execute('''
            INSERT INTO rewards (reward_name, reward_description, cost, reward_rate)
            VALUES (?, ?, ?, ?)
        ''', (reward_name, reward_description, cost, reward_rate))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_test_data()