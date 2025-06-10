import csv
import pickle

class Contact:
    def __init__(self, surname, phone):
        self.surname = surname
        self.phone = phone

    def __repr__(self):
        return f"{self.surname}: {self.phone}"


class Notebook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, surname, phone):
        self.contacts.append(Contact(surname, phone))

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for contact in self.contacts:
                writer.writerow([contact.surname, contact.phone])

    def load_from_csv(self, filename):
        self.contacts.clear()
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    self.add_contact(row[0], row[1])

    def save_to_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.contacts, f)

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as f:
            self.contacts = pickle.load(f)

    def search_by_letter(self, letter):
        found = [c for c in self.contacts if c.surname.lower().startswith(letter.lower())]
        if(len(found)!= 0):
            print("Найденные контакты:")
            for g in found:
                print(g)
        else:
            print("Нет контактов с такой буквы.")

    def search_by_phone(self, phone:int):
        for c in self.contacts:
            if c.phone == phone:
                print(f"Телефон принадлежит: {c.surname}")
            else:
                print("Телефон не найден.")
    def input_contact(self):
        while(True):
            try:    
                surname = input("Введите фамилию (или 'q' для выхода): ").strip()
                if surname.lower() == "q":
                    break
                number = input("Введите номер телефона (или 'q' для выхода): ").strip()
                if number.lower() == "q":
                    break
                number = (int)(number)
                if not surname or not number:
                    print("Фамилия и номер телефона не могут быть пустыми. Попробуйте снова.")
                    continue
                self.add_contact(surname, number)
            except:
                print('Try again!')            
    
class Task1:
    
    def __init__(self):
        self.book = Notebook()

    def run(self):
        while True:
            print(
                'Choose one of the options:\n'
                '0) Back\n'
                '1) Set contacts\n'
                '2) Search by letter\n'
                '3) Search by phone\n'
                '4) Save to csv\n'
                '5) Save to pickle\n'
                '6) Load from csv\n'
                '7) Load from pickle\n'
            )
            option = (int)(input())
            match option:
                case 0:
                    return
                case 1:
                    self.book.input_contact()
                case 2:
                    letter = input("Введите первую букву фамилии для поиска: ")
                    self.book.search_by_letter(letter)
                case 3:
                    phone = int(input("Введите номер телефона для поиска: "))
                    self.book.search_by_phone(phone)
                case 4:
                    self.book.save_to_csv(r"C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\contacts.csv")
                case 5:
                    self.book.save_to_pickle(r"C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\contacts.pkl")
                case 6:
                    self.book.load_from_csv(r"C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\contacts.csv")
                case 7:
                    self.book.load_from_pickle(r"C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\contacts.pkl")               