from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt
from abc import ABC, abstractmethod

class Field: # Базовий клас для полів запису
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): # Клас для зберігання імені контакту. Обов'язкове поле.
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)            

class Phone(Field): # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value):
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field): # Клас для валідації та запису дня народження
    def __init__(self, value):
        try:
           self.value = dtdt.strptime(value,"%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record: # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self,phone): # функція додавання телефону
        self.phones.append(Phone(phone))
           
    def remove_phone(self,phone): # функція видалення телефону
         self.phones = [ph for ph in self.phones if ph.value != phone]   

    def edit_phone(self, old_phone: str, new_phone: str): # функція зміни телефону
        self.phones = [phone if str(phone) == old_phone else Phone(new_phone) for phone in self.phones]

    def find_phone(self, phone: str) -> Phone: # функція пошук телефону
        for ph in self.phones:
            if ph.value == phone:
                return ph
        raise ValueError("Phone number not found")                 

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        if self.birthday!=None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},Birthday:{self.birthday}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict): # Клас для зберігання та управління записами.
    def add_record(self, record: Record): # додавання запису
        self.data[record.name.value] = record

    def find(self, name: str) -> Record: # пошук запису
        return self.data.get(name)

    def delete(self, name: str): # видалення запису
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self): # пошук будуючих днів народжень
        today = dtdt.today().date()
        upcoming_birthdays = []
        for name, record in self.data.items():  
            if  record.birthday:
                upcoming_birthday = dict()
                birthday_this_year = record.birthday.value.replace(year = today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year = today.year + 1)
                difference = birthday_this_year.toordinal() - today.toordinal()
                if difference < 7: 
                    if birthday_this_year.weekday() == 5:
                        birthday_this_year += dt.timedelta(days=2)
                    if birthday_this_year.weekday() == 6:
                        birthday_this_year += dt.timedelta(days=1)
                    upcoming_birthday[str(name)] = birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append(upcoming_birthday)    
        return upcoming_birthdays

class UserView(ABC):
    @abstractmethod
    def show_info(self, info):
        pass


class ConsoleUserView(UserView):
    def show_info(self, info):
        print(info)
        
        
if __name__=="__main__":
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("01.02.1992")
    # Додавання запису John до адресної книги

    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    jane_record.add_birthday("02.12.1991")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")