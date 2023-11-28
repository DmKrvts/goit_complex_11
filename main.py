from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    ...

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if value.isdigit() and len(value) == 10:
            self._value = value
        else:
            raise ValueError("Invalid phone number format.")

class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self._value = datetime.strptime(value, '%Y.%m.%d').date()

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        try:
            if self.birthday:
                current_date = datetime.now().date()
                record_nearest_birthday = self.birthday.value.replace(year=current_date.year)
                
                if record_nearest_birthday < current_date:
                    record_nearest_birthday = self.birthday.value.replace(year=current_date.year + 1)
                    days_until_birthday = (record_nearest_birthday - current_date).days
                   
                    print(f"Record: {self.name.value}, Nearest Birthday: {record_nearest_birthday}, Days until Birthday: {days_until_birthday}")
                return days_until_birthday
                
        except AttributeError:
            print(f"Contact name: {self.name.value}, do not have birthday record")
     
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))            

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, phone, new_phone):
        existing_phone = self.find_phone(phone)
        if existing_phone:
            existing_phone.value = new_phone
        else:
            raise ValueError("Phone not found")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        key = record.name.value
        self.data[key] = record

    def find(self, name):
        key = Name(name).value
        return self.data.get(key)

    def delete(self, name):
        key = Name(name).value
        
        if self.find(key):
            del self.data[key]

    def iterator(self, item_number: int):
        print(f"Received item_number: {item_number}")
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
            
        
if __name__ == '__main__':
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    found_phone = john_record.find_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення:John: 5555555555

    # Видалення запису Jane
    # book.delete("Jane")

    
    # Створення запису для Tony з днем народження
    tony_record = Record("Tony", "1999.11.06")
    tony_record.add_phone("0000000000")
    book.add_record(tony_record)
    tony_record.add_phone("0000000001")
    tony_record.add_phone("0000000002")
    tony_record.add_phone("0000000003")
    tony_record.add_phone("0000000004")
    
    # Дізнаємось кількість днів до наступного дня народження.
    tony_record.days_to_birthday()
    john_record.days_to_birthday()

    # Виведення N записів у книзі
   
    for result_chunk in book.iterator(2):
        print(result_chunk)



    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)