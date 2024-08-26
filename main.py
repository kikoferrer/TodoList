from backend.api import create_entry, show_entry, update_entry, delete_entry


while True:
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
        break
    elif prompt in options.keys():
        if prompt.lower() == "a":
            print("You chose create an entry.\n")
            entry = input("Enter your entry: ")
            create_entry(entry)
            print("What would you like to do next?")
        elif prompt.lower() == "b":
            print("you want to view a certain entry?\n")
            id_num = input("Select the id number of the one you want to view")
            show_entry(id_num)
            print("What would you like to do next?")
        elif prompt.lower() == "c":
            print("you want to update a certain entry?\n")
            id_num = input("Select the id number of the one you want to update")
            update_entry(id_num)
            print("What would you like to do next?")
        elif prompt.lower() == "d":
            print("You chose delete an entry.\n")
            id_num = input("Select the id number of the one you want to delete")
            delete_entry(id_num)
            print("What would you like to do next?")
    else:
        print("Invalid option. Choose again.")
