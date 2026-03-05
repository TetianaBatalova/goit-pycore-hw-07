from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Union

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
        try:
            # Перетворення рядка на об'єкт date
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_number: str, new_number: str) -> None:
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return
        raise ValueError("Old phone number not found.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_string: str) -> None:
        self.birthday = Birthday(birthday_string)

    def __str__(self) -> str:
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            # ОБРОБКА 29 ЛЮТОГО: 
            # Якщо людина народилася 29.02, а рік не високосний,
            # замінюємо на 01.03 (найпоширеніша практика)
            try:
                birthday_this_year = record.birthday.value.replace(year=today.year)
            except ValueError:
                # Це трапляється лише 29 лютого в не-високосний рік
                birthday_this_year = record.birthday.value.replace(year=today.year, day=28) + timedelta(days=1)

            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                except ValueError:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1, day=28) + timedelta(days=1)

            # Перевірка на найближчі 7 днів
            if 0 <= (birthday_this_year - today).days <= 7:
                congratulation_date = birthday_this_year
                
                # Перенесення привітання, якщо випадає на вихідні
                weekday = congratulation_date.weekday()
                if weekday == 5:  # Субота
                    congratulation_date += timedelta(days=2)
                elif weekday == 6:  # Неділя
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })
        return upcoming_birthdays
