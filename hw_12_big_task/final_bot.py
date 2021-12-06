from collections import UserDict
from typing import Optional, List
from datetime import datetime, date
from pathlib import Path
import pickle


class Field:
    # parental class for future fields
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Phone(Field):
    # optional field, might be few records
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value[0] != '+':
            raise ValueError("Start phone with '+'")
        number = value[1:]
        if len(number) != 12 or not number.isalnum():
            raise ValueError("Only 12 digits after '+'")
        self.__value = value

    def __str__(self):
        return f"Phone: {self.value}"


class Birthday(Field):
    # users date of birth
    @property
    def value(self) -> datetime:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        try:
            self.__value = datetime.strptime(value, '%d %m %Y')
        except (ValueError, TypeError):
            raise ValueError("Data must match pattern '%d %m %Y'")


class Record:
    # responsible for main logic
    def __init__(self, name: str, phone: Optional[List[str]] = None, birthday: Birthday = None) -> None:
        if phone is None:
            self.phone = []
        else:
            self.phone = [Phone(phone_number) for phone_number in phone]
        self.name = Name(name)
        self.birthday = birthday

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

    def count_days_till_birthday(self) -> Optional[int]:
        if self.birthday and self.birthday.value:
            value = self.birthday.value
            today = date.today()

            data_1 = date(today.year, value.month, value.day)
            data_2 = date(today.year + 1, value.month, value.day)

            logic_data = data_2 if data_1 < today else data_1
            return (logic_data-today).days

    def __str__(self):
        return f"Record of {self.name.value}, phones {[ph_num.value for ph_num in self.phone]}"


class AddressBook(UserDict):
    # responsible for logic in search process

    def add_record(self, record: list) -> None:
        new_record = Record(record[0], record[1:])
        self.data[new_record.name.value] = new_record

    def find_record(self, value: str) -> Optional[Record]:
        return self.data.get(value)

    def delete_record(self, value: str) -> None:
        self.data.pop(value)

    def search_info(self, user_request):
        output = f"Found for '{user_request}': "
        search_flag = False
        for key, data in self.data.items():
            one_number = [ph_num.value for ph_num in data.phone]
            print(one_number)
            if (user_request in one_number[0]) or (user_request in key):
                output += f"{key}, {data}"
                search_flag = True
        if not search_flag:
            output += f"No match"
        return output

    def dump_it(self, file: str) -> None:
        try:
            with open(file, 'wb') as fh:
                pickle.dump(self.data, fh)
            print(f"{file} saved")
        except FileNotFoundError:
            print("File not found")

    def load_it(self, file: str) -> None:
        try:
            with open(file, 'rb') as fh:
                self.data = pickle.load(fh)
            print(f"Got information from {file}")
        except FileNotFoundError:
            print("File not found")

    def iterator(self, n):
        values = list(self.data.values())
        while values:
            yield values[:n]
            values = values[n:]

    def __str__(self):
        return str(self.data)


if __name__ == '__main__':
    book = AddressBook()

    # hard-code example:
    path_for_this_code = Path(__file__).absolute()
    file_name = f"{path_for_this_code.stem}.bin"
    general_file = path_for_this_code.parent.joinpath(file_name)
    book.load_it(general_file)

    book.add_record(['Alex', "+380696969696"])
    book.add_record(['Clover', "+380777777777"])
    book.add_record(['Sam', "+380333333333"])

    record_iterator = book.iterator(2)

    print(next(record_iterator))
    print(next(record_iterator))

    book.dump_it(general_file)

    print(book.search_info('380'))
