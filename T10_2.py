from typing import List, Tuple, Union, Callable, Any
from models import AddressBook, Record  # Припускаємо, що класи в models.py

def input_error(func: Callable) -> Callable:
    def inner(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter user name and the required information."
        except KeyError:
            return "Contact not found."
    return inner

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise IndexError
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone updated."
    raise KeyError

@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(p.value for p in record.phones)
    raise KeyError

def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise IndexError
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    raise KeyError

@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    elif record:
        return "Birthday not set for this contact."
    raise KeyError

@input_error
def birthdays(book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    # Формуємо список іменинників
    return "\n".join([f"{item['name']}: {item['congratulation_date']}" for item in upcoming])

def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        elif not command:
            continue
            
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
