import os
import json
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name):
        self._name = name
    
    @abstractmethod
    def get_info(self):
        pass

class Book:
    def __init__(self, title, author):
        self.__title = title
        self.__author = author
        self.__is_taken = False
        self.__taken_by = None
    
    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author
    
    def get_is_taken(self):
        return self.__is_taken
    
    def get_taken_by(self):
        return self.__taken_by
    
    def take_book(self, user_name):
        if not self.__is_taken:
            self.__is_taken = True
            self.__taken_by = user_name
            return True
        return False
    
    def return_book(self):
        if self.__is_taken:
            self.__is_taken = False
            self.__taken_by = None
            return True
        return False
    
    def book_info(self):
        status = "Выдана" if self.__is_taken else "Доступна"
        user_info = f" (у пользователя: {self.__taken_by})" if self.__is_taken else ""
        return f"Книга: '{self.__title}', Автор: {self.__author}, Статус: {status}{user_info}"

class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__taken_books = []
    
    def get_info(self):
        return f"Пользователь: {self._name}, Взято книг: {len(self.__taken_books)}"
    
    def get_taken_books(self):
        return self.__taken_books
    
    def take_book_for_user(self, book):
        if book.take_book(self._name):
            self.__taken_books.append(book.get_title())
            return True
        return False
    
    def return_book_for_user(self, book):
        if book.return_book():
            if book.get_title() in self.__taken_books:
                self.__taken_books.remove(book.get_title())
            return True
        return False

class Librarian(Person):
    def get_info(self):
        return f"Библиотекарь: {self._name}"

class Library:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__librarians = [Librarian("Админ")]
        self.__current_user = None
        self.__current_librarian = None
        self.load_data()
    
    def load_data(self):
        if os.path.exists("books.txt"):
            with open("books.txt", "r", encoding="utf-8") as file:
                try:
                    books_data = json.load(file)
                    for book_data in books_data:
                        book = Book(book_data["title"], book_data["author"])
                        if book_data["is_taken"]:
                            book.take_book(book_data["taken_by"])
                        self.__books.append(book)
                except:
                    self.__books = []
        
        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as file:
                try:
                    users_data = json.load(file)
                    for user_data in users_data:
                        user = User(user_data["name"])
                        for book_title in user_data["taken_books"]:
                            user.get_taken_books().append(book_title)
                        self.__users.append(user)
                except:
                    self.__users = []
    
    def save_data(self):
        books_data = []
        for book in self.__books:
            books_data.append({
                "title": book.get_title(),
                "author": book.get_author(),
                "is_taken": book.get_is_taken(),
                "taken_by": book.get_taken_by()
            })
        
        with open("books.txt", "w", encoding="utf-8") as file:
            json.dump(books_data, file, ensure_ascii=False, indent=2)
        
        users_data = []
        for user in self.__users:
            users_data.append({
                "name": user._name,
                "taken_books": user.get_taken_books()
            })
        
        with open("users.txt", "w", encoding="utf-8") as file:
            json.dump(users_data, file, ensure_ascii=False, indent=2)
    
    def librarian_login(self):
        self.__current_librarian = self.__librarians[0]
        print(f"Вы вошли как {self.__current_librarian.get_info()}")
        return True
    
    def add_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        
        for book in self.__books:
            if book.get_title() == title and book.get_author() == author:
                print("Такая книга уже есть в библиотеке!")
                return
        
        new_book = Book(title, author)
        self.__books.append(new_book)
        print(f"Книга '{title}' успешно добавлена!")
    
    def remove_book(self):
        title = input("Введите название книги для удаления: ")
        author = input("Введите автора книги: ")
        
        for book in self.__books:
            if book.get_title() == title and book.get_author() == author:
                if book.get_is_taken():
                    print("Эту книгу нельзя удалить, так как она выдана пользователю!")
                    return
                self.__books.remove(book)
                print(f"Книга '{title}' успешно удалена!")
                return
        
        print("Книга не найдена!")
    
    def register_user(self):
        name = input("Введите имя нового пользователя: ")
        
        for user in self.__users:
            if user._name == name:
                print("Пользователь с таким именем уже существует!")
                return
        
        new_user = User(name)
        self.__users.append(new_user)
        print(f"Пользователь '{name}' успешно зарегистрирован!")
    
    def view_all_users(self):
        if not self.__users:
            print("Нет зарегистрированных пользователей.")
            return
        
        print("Список всех пользователей:")
        for user in self.__users:
            print(user.get_info())
            taken_books = user.get_taken_books()
            if taken_books:
                print(f"  Взятые книги: {', '.join(taken_books)}")
    
    def view_all_books(self):
        if not self.__books:
            print("В библиотеке нет книг.")
            return
        
        print("Список всех книг:")
        for book in self.__books:
            print(book.book_info())
    
    def user_login(self):
        name = input("Введите ваше имя: ")
        
        for user in self.__users:
            if user._name == name:
                self.__current_user = user
                print(f"Вы вошли как {user.get_info()}")
                return True
        
        print("Пользователь не найден! Обратитесь к библиотекарю для регистрации.")
        return False
    
    def view_available_books(self):
        available_books = [book for book in self.__books if not book.get_is_taken()]
        
        if not available_books:
            print("Нет доступных книг.")
            return
        
        print("Доступные книги:")
        for book in available_books:
            print(f"Книга: '{book.get_title()}', Автор: {book.get_author()}")
    
    def take_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        
        for book in self.__books:
            if book.get_title() == title and book.get_author() == author:
                if self.__current_user.take_book_for_user(book):
                    print(f"Книга '{title}' успешно взята!")
                else:
                    print("Эта книга уже выдана другому пользователю!")
                return
        
        print("Книга не найдена!")
    
    def return_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        
        if title not in self.__current_user.get_taken_books():
            print("У вас нет такой книги!")
            return
        
        for book in self.__books:
            if book.get_title() == title and book.get_author() == author:
                if self.__current_user.return_book_for_user(book):
                    print(f"Книга '{title}' успешно возвращена!")
                return
        
        print("Книга не найдена в библиотеке!")
    
    def view_my_books(self):
        taken_books = self.__current_user.get_taken_books()
        
        if not taken_books:
            print("У вас нет взятых книг.")
            return
        
        print("Ваши книги:")
        for title in taken_books:
            for book in self.__books:
                if book.get_title() == title:
                    print(f"Книга: '{title}', Автор: {book.get_author()}")
                    break
    
    def run(self):
        while True:
            print("\nБИБЛИОТЕЧНАЯ СИСТЕМА")
            print("1. Войти как библиотекарь")
            print("2. Войти как пользователь")
            print("3. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                if self.librarian_login():
                    self.librarian_menu()
            elif choice == "2":
                if self.user_login():
                    self.user_menu()
            elif choice == "3":
                self.save_data()
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неверный выбор!")
    
    def librarian_menu(self):
        while True:
            print("\nМЕНЮ БИБЛИОТЕКАРЯ")
            print("1. Добавить новую книгу")
            print("2. Удалить книгу из системы")
            print("3. Зарегистрировать нового пользователя")
            print("4. Просмотреть список всех пользователей")
            print("5. Просмотреть список всех книг")
            print("6. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.register_user()
            elif choice == "4":
                self.view_all_users()
            elif choice == "5":
                self.view_all_books()
            elif choice == "6":
                self.__current_librarian = None
                break
            else:
                print("Неверный выбор!")
    
    def user_menu(self):
        while True:
            print(f"\nМЕНЮ ПОЛЬЗОВАТЕЛЯ: {self.__current_user._name}")
            print("1. Просмотреть доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Просмотреть список взятых книг")
            print("5. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.view_available_books()
            elif choice == "2":
                self.take_book()
            elif choice == "3":
                self.return_book()
            elif choice == "4":
                self.view_my_books()
            elif choice == "5":
                self.__current_user = None
                break
            else:
                print("Неверный выбор!")

if __name__ == "__main__":
    library = Library()
    library.run()