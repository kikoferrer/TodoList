import requests
import time
import subprocess


subprocess.Popen(["uvicorn", "api:app", "--reload"], cwd="backend/")

time.sleep(2)

title = input("Enter todo list title: ")
init_response = requests.post("http://127.0.0.1:8000/tables", json={"message": title})

cache = {}


def update_list(todo_cache):
    if not todo_cache:
        return todo_cache
    else:
        todo_list = {}
        for i, entry in enumerate(todo_cache.values(), start=1):
            entry["id_num"] = i
            todo_list[i] = entry
        return todo_list


if init_response.status_code == 200:
    while True:
        print("Current list of entries")
        get_list = requests.get("http://127.0.0.1:8000/entries").json()
        print(get_list)
        current_list = update_list(get_list)
        entry_list = []
        for key, value in current_list.items():
            for k, v in value.items():
                entry_list.append(f"{k}: {v}, ")
            entry_list.append("\n")
        final_list = "".join(entry_list)
        print(final_list)

        options = {
            "A": "Create entry",
            "B": "View entry",
            "C": "Update entry",
            "D": "Delete entry",
        }
        print("Please choose among the following options:\n")
        for key, value in options.items():
            print(f"{key}. {value}")
        prompt = input("\nEnter your option: ")
        if prompt.lower() == "q":
            response = requests.post("http://127.0.0.1:8000/shutdown")
            if response.status_code == 200:
                message = response.json()
                print(message["message"])
            break
        elif prompt.upper() in options.keys():
            if prompt.lower() == "a":
                print("You chose create an entry.\n")
                entry = input("Enter your entry: ")
                response = requests.post(
                    "http://127.0.0.1:8000/entries", json={"message": entry}
                )
                if response.status_code == 200:
                    data = response.json()
                    print(data)
                else:
                    print("Failed request")
                print("What would you like to do next?")
            elif prompt.lower() == "b":
                print("you want to view a certain entry?\n")

                id_num = int(
                    input("Select the id number of the one you want to view: ")
                )
                entry_dict = requests.get(
                    f"http://127.0.0.1:8000/entries/{id_num}"
                ).json()

                for key, value in entry_dict.items():
                    print(f"{key}: {value}")

                print("What would you like to do next?")
            elif prompt.lower() == "c":
                print("you want to update a certain entry?\n")
                id_num = int(
                    input("Select the id number of the one you want to update: ")
                )
                entry = input("Enter your entry update: ")
                requests.put(
                    f"http://127.0.0.1:8000/entries/{id_num}", json={"message": entry}
                )
                print("What would you like to do next?")
            elif prompt.lower() == "d":
                print("You chose delete an entry.\n")
                id_num = int(
                    input("Select the id number of the one you want to delete: ")
                )
                requests.delete(f"http://127.0.0.1:8000/entries/{id_num}").json()
                print("What would you like to do next?")
        else:
            print("Invalid option. Choose again.")
else:
    print("Error has occurred")
    exit
