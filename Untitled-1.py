import os
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name):
        self._name = name
    
    @abstractmethod
    def show_info(self):
        pass

class Book:
    def __init__(self, title, author):
        self.__title = title
        self.__author = author
        self.__taken_by = None

    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author
    
    def is_taken(self):
        return self.__taken_by is not None
    
    def take(self, user_name):
        if not self.__taken_by:
            self.__taken_by = user_name
            return True
        return False
    
    def return_book(self):
        self.__taken_by = None
        return True

class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__my_books = []

    def show_info(self):
        return f"{self._name} (книг: {len(self.__my_books)})"
    
    def get_books(self):
        return self.__my_books
    
    def take_book(self, book):
        if book.take(self._name):
            self.__my_books.append(book.get_title())
            return True
        return False
    
    def return_book(self, book):
        if book.return_book():
            self.__my_books.remove(book.get_title())
            return True
        return False

class Librarian(Person):
    def show_info(self):
        return f"Библиотекарь: {self._name}"

class Library:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__current_user = None
        self.load_data()
    
    def load_data(self):
        if os.path.exists("books.txt"):
            with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("|")
                        if len(parts) == 3:
                            book = Book(parts[0], parts[1])
                            if parts[2] != "None":
                                book.take(parts[2])
                            self.__books.append(book)

        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        name, books_str = line.split("|")
                        user = User(name)
                        if books_str:
                            for book_title in books_str.split(","):
                                if book_title:
                                    user.get_books().append(book_title)
                        self.__users.append(user)
    
    def save_data(self):
        with open("books.txt", "w", encoding="utf-8") as f:
            for book in self.__books:
                taken_by = book.__taken_by if hasattr(book, '_Book__taken_by') else None
                f.write(f"{book.get_title()}|{book.get_author()}|{taken_by}\n")
                
        with open("users.txt", "w", encoding="utf-8") as f:
            for user in self.__users:
                books_str = ",".join(user.get_books())
                f.write(f"{user._name}|{books_str}\n")

    def add_book(self):
        title = input("Название книги: ")
        author = input("Автор: ")
        self.__books.append(Book(title, author))
        print("Книга добавлена")
    
    def show_all_books(self):
        for book in self.__books:
            status = "выдана" if book.is_taken() else "доступна"
            print(f"{book.get_title()} - {book.get_author()} ({status})")
    
    def add_user(self):
        name = input("Имя пользователя: ")
        self.__users.append(User(name))
        print("Пользователь добавлен")
    
    def show_all_users(self):
        for user in self.__users:
            print(user.show_info())
    
    def user_login(self):
        name = input("Ваше имя: ")
        for user in self.__users:
            if user._name == name:
                self.__current_user = user
                print(f"Привет, {name}")
                return True
        print("Пользователь не найден")
        return False
    
    def show_available_books(self):
        for book in self.__books:
            if not book.is_taken():
                print(f"{book.get_title()} - {book.get_author()}")
    
    def take_book(self):
        title = input("Название книги: ")
        for book in self.__books:
            if book.get_title() == title and not book.is_taken():
                self.__current_user.take_book(book)
                print("Книга взята")
                return
        print("Книга не найдена или уже выдана")
    
    def return_book(self):
        if not self.__current_user.get_books():
            print("У вас нет книг")
            return
        
        print("Ваши книги:", ", ".join(self.__current_user.get_books()))
        title = input("Название книги для возврата: ")
        
        if title in self.__current_user.get_books():
            for book in self.__books:
                if book.get_title() == title and book.is_taken():
                    self.__current_user.return_book(book)
                    print("Книга возвращена")
                    return
        print("У вас нет такой книги")
    
    def run(self):
        while True:
            print("\n1. Библиотекарь")
            print("2. Пользователь")
            print("3. Выход")
            choice = input("Выбор: ")
            
            if choice == "1":
                self.librarian_menu()
            elif choice == "2":
                self.user_menu()
            elif choice == "3":
                self.save_data()
                print("До свидания!")
                break
    
    def librarian_menu(self):
        librarian = Librarian("Админ")
        print(librarian.show_info())
        
        while True:
            print("\n1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Добавить пользователя")
            print("4. Показать всех пользователей")
            print("5. Назад")
            choice = input("Выбор: ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_all_books()
            elif choice == "3":
                self.add_user()
            elif choice == "4":
                self.show_all_users()
            elif choice == "5":
                break
    
    def user_menu(self):
        if not self.user_login():
            return
        
        while True:
            print(f"\n1. Показать доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Назад")
            choice = input("Выбор: ")
            
            if choice == "1":
                self.show_available_books()
            elif choice == "2":
                self.take_book()
            elif choice == "3":
                self.return_book()
            elif choice == "4":
                self.__current_user = None
                break

if __name__ == "__main__":
    library = Library()
    library.run()
