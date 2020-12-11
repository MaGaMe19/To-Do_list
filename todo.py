import os
import json
from time import sleep as wait

print("Welcome to your To-Do list!")

filename = "todo.json"
todos = []
todosDone = []

def prepareFile():
    # Prepare file to store data if no file has been generated yet
    with open(filename, "w") as f:
        json.dump(
            {
                "todo": [],
                "done": []
            }, f, indent=4)

if os.path.exists(filename):
    print("Loading your saved To-Dos...")
    # load file and make sure that it isn't corrupted
    try:
        with open(filename) as f:
            data = json.load(f)
            for todo in data["todo"]:
                todos.append(todo)
            for todoDone in data["done"]:
                todosDone.append(todoDone)
        wait(.5)
    except:
        prepareFile()
        print()
        print(f"WARNING: The file '{filename}' has been reset because it was corrupted or modified.")
else:
    prepareFile()

done = False
changes = False
while not done:
    print()
    print("What would you like to do? List, Add <todo>, Remove <todo>, Finish <todo>, [Delete] To-Do list or [Quit] and save?")
    action = input("> ")
    
    if action.lower() in ("quit", "q"):
        if changes:
            print("Saving your To-Dos...")
            with open(filename, "w") as f:
                # Dump everything into file
                json.dump(
                    {
                        "todo": todos,
                        "done": todosDone
                    }, f, indent=4)
            wait(.5)
        print("Bye!")
        done = True
    
    elif action.lower() in ("list", "l"):
        if len(todos) == 0 and len(todosDone) == 0:
            print("There are currently no To-Dos in your To-Do list.")
        else:
            if len(todos) != 0:
                print("Unfinished To-Dos:")
                for num, todo in enumerate(todos, 1):
                    print(f"{num}. {todo}")
            if len(todosDone) != 0:
                print()
                print("Finished To-Dos:")
                for todoDone in todosDone:
                    print(f"· {todoDone}")
    
    elif action.lower() in ("delete", "del"):
        if os.path.exists(filename):
            done2 = False
            while not done2:
                confirmation = input("Do you want to delete all your To-Dos? (yes/no) ")
                if confirmation.lower() in ("yes", "y"):
                    todos, todosDone = [], []
                    os.remove(filename)
                    print("Your To-Do list has been cleared.")
                    done2 = True
                    changes = False
                else:
                    break
        else:
            print("You cannot delete your To-Do list, because it does not exist yet.")
                
    else:
        try:
            command, todo = action.split(maxsplit=1)
            
            if command.lower() in ("add", "a"):
                todos.append(todo)
                print(f"'{todo}' has been added to your To-Do list.")
                changes = True
                
            elif command.lower() in ("remove", "rem", "r"):
                try:
                    num = int(todo)
                    if 0 < num <= len(todos):
                        print(f"'{todos[num - 1]}' has been removed from your To-Do list.")
                        todos.remove(todos[num - 1])
                    else:
                        print(f"There is no To-Do with the index {num} in your To-Do list.")
                except:
                    if todo in todos:
                        todos.remove(todo)
                        print(f"'{todo}' has been removed from your To-Do list.")
                    elif todo in todosDone:
                        todosDone.remove(todo)
                        print(f"'{todo}' has been removed from your To-Do list.")
                    else:
                        print(f"'{todo}' could not be found in your To-Do list.")
                changes = True
                
            elif command.lower() in ("finish", "fin", "f"):
                try:
                    num = int(todo)
                    if 0 < num <= len(todos):
                        toChange = todos[num - 1]
                        print(f"You have finished '{toChange}'.")
                        todos.remove(toChange)
                        todosDone.append(toChange)
                    else:
                        print(f"There is no To-Do with the index {num} in your To-Do list.")
                except:
                    if todo in todos:
                        todos.remove(todo)
                        todosDone.append(todo)
                        print(f"You have finished '{todo}'.")
                    else:
                        print(f"'{todo}' could not be found in your To-Do list.")
            else:
                print("Error Unknown command.")
            
        except:
            print("Error: Unknown command or incorrect use of command.")
