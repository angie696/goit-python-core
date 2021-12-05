from collections import UserDict
from typing import List, Optional


class Field:
    # parental class for future fields
    def __init__(self, value):
        self.value = value


class Name(Field):
    """must-have field with name"""


class Phone(Field):
    # optional field, might be few records
    def __str__(self):
        return f"Phone: {self.value}"


class Record:
    # responsible for main logic
    def __init__(self, name: str, phone: List[str] = None):
        if phone is None:
            self.phone = []
        else:
            self.phone = [Phone(phone_number) for phone_number in phone]
        self.name = Name(name)

    def add_phone(self, phone_number: str) -> None:
        phone = Phone(phone_number)
        if phone not in self.phone:
            self.phone.append(phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        for ph_num in self.phone:
            if ph_num.value == phone:
                return ph_num

    def delete_phone(self, phone: str) -> None:
        phone_to_delete = self.find_phone(phone)
        self.phone.remove(phone_to_delete) if phone_to_delete else None

    def edit_phone(self, old_phone, new_phone) -> None:
        new_phone = Phone(new_phone)
        phone_to_remove = self.find_phone(old_phone)
        if phone_to_remove:
            self.phone.remove(phone_to_remove) if phone_to_remove else None
            self.phone.append(new_phone)

    def __str__(self):
        return f"Record of {self.name.value}, phones {[ph_num.value for ph_num in self.phone]}"


class AddressBook(UserDict):
    # responsible for logic in search process

    def add_record(self, name: str, phones: list) -> None:
        new_record = Record(name, phones)
        self.data[new_record.name.value] = new_record

    def find_record(self, value: str) -> Optional[Record]:
        return self.data.get(value)

    def delete_record(self, value: str) -> None:
        self.data.pop(value)

    def __str__(self):
        return str(self.data)


if __name__ == '__main__':
    # hard-code example:

    book = AddressBook()
    book.add_record('Alex', ["066 111 22 33", "911"])
    book.add_record('Clover', ["122", "7 777 77 777"])
    book.add_record('Sam', ["069 696 99 66", "103"])

    record = book.find_record("Sam")

    record.delete_phone("911")
    record.add_phone("122")
    record.edit_phone("122", "112")

    print(record)
