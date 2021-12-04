def input_error(func):
    # Responsible for exceptions in each user command
    def is_error(user_input):
        if func.__name__ in ['say_hello', 'ask_to_show_all']:
            return func()
        try:
            return func(user_input)
        except KeyError as no_key:
            return no_key
        except IndexError as no_idx:
            return no_idx
        except ValueError as wrong_val:
            return wrong_val
    return is_error


@input_error
def say_hello():
    # greetings msg
    return "How can I help you?"


@input_error
def ask_to_show_all():
    # all phones
    return "\n".join(f"{name}: {phone}" for name, phone in phone_book.items())


@input_error
def add_contact(user_input):
    # add new contact
    name, phone = user_input.split()
    phone_book[name.strip()] = phone.strip()
    return f"{phone} added to your phone book as {name}"


@input_error
def make_change(user_input):
    # replace user phone with a new one
    name, phone = user_input.split()
    phone_book[name.strip()] = phone.strip()
    return f"{phone} is new number for {name}"


@input_error
def get_the_phone(user_input):
    # display number for this name
    name = user_input
    return_phone = phone_book.get(name)
    if return_phone:
        return f"{return_phone} for {name}"
    else:
        return "Not found"


@input_error
def get_command_from_user(user_input):
    # proceed the command from user
    magic_word = ''.join([word for word in all_commands if user_input.startswith(word)])
    if magic_word:
        print(commands_func[magic_word](user_input[len(magic_word):].strip()))
    else:
        print("Command not found. Try: 'hello', 'add', 'change', 'phone', 'show all' ")


def main():
    user_command = input("Waiting for the command: ").lower().strip()
    while user_command not in ['good bye', 'close', 'exit']:
        get_command_from_user(user_command)
        user_command = input("Waiting for the command: ").lower().strip()

    print("Good bye!")


if __name__ == "__main__":
    # make empty dict for future contacts
    phone_book = {}
    # list with commands
    all_commands = ['hello', 'add', 'change', 'phone', 'show all']
    # functions for each command
    commands_functions = [say_hello, add_contact, make_change, get_the_phone, ask_to_show_all]
    # chain commands with funcs
    commands_func = {command: func for command, func in zip(all_commands, commands_functions)}
    main()
