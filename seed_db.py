import os
import json

import crud
import model
import server

os.system("dropdb -U postgres python-capstone-db")
os.system("createdb -U postgres python-capstone-db")

model.connect_to_db(server.app)
model.db.create_all()

for n in range(3):
    email = f"user{n}@test.com" 
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()

with open("data/goals.json") as f:
    goal_data = json.loads(f.read())

goals_in_db = []
for goal in goal_data:
    description, picture_path, deadline, complete, user_id = (
        goal["description"],
        goal["picture_path"],
        goal["deadline"],
        goal["complete"],
        goal["user_id"]
    )

    db_goal = crud.create_goal(description, picture_path, deadline, complete, user_id)
    goals_in_db.append(db_goal)

model.db.session.add_all(goals_in_db)
model.db.session.commit()

