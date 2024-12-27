from sqlalchemy import create_engine, Column, Integer, String, DATE, and_
from sqlalchemy.orm import sessionmaker, declarative_base
import json

# Завантаження конфігурації
with open("config.json") as f:
    config = json.load(f)

db_user = config["database"]["user"]
db_password = config["database"]["password"]

# Підключення до бази даних
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/People"
engine = create_engine(db_url)

# Базовий клас для декларативного стилю
Base = declarative_base()

# Модель таблиці
class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    birth_date = Column(DATE)

# Створення таблиці
Base.metadata.create_all(engine)

# Налаштування сесії
Session = sessionmaker(bind=engine)
session = Session()

# Функції для роботи з даними
def display_all():
    """Відображення всіх записів."""
    results = session.query(Person).all()
    if results:
        print("\nРезультат:")
        for row in results:
            print(f"{row.id} | {row.first_name} {row.last_name} | Місто: {row.city} | Країна: {row.country} | Дата народження: {row.birth_date}")
    else:
        print("\nРезультат відсутній.")

def add_person():
    """Додавання нового запису."""
    first_name = input("Введіть ім'я: ").strip()
    last_name = input("Введіть прізвище: ").strip()
    city = input("Введіть місто: ").strip()
    country = input("Введіть країну: ").strip()
    birth_date = input("Введіть дату народження (YYYY-MM-DD): ").strip()

    new_person = Person(first_name=first_name, last_name=last_name, city=city, country=country, birth_date=birth_date)
    session.add(new_person)
    session.commit()
    print("Запис успішно додано.")

def delete_person():
    """Видалення запису."""
    person_id = input("Введіть ID запису для видалення: ").strip()
    person = session.query(Person).filter_by(id=person_id).first()
    if person:
        session.delete(person)
        session.commit()
        print("Запис успішно видалено.")
    else:
        print("Запис із таким ID не знайдено.")

def update_person():
    """Оновлення запису."""
    person_id = input("Введіть ID запису для оновлення: ").strip()
    person = session.query(Person).filter_by(id=person_id).first()
    if person:
        print("Введіть нові значення (залиште порожнім для пропуску):")
        first_name = input(f"Ім'я ({person.first_name}): ").strip()
        last_name = input(f"Прізвище ({person.last_name}): ").strip()
        city = input(f"Місто ({person.city}): ").strip()
        country = input(f"Країна ({person.country}): ").strip()
        birth_date = input(f"Дата народження ({person.birth_date}): ").strip()

        if first_name:
            person.first_name = first_name
        if last_name:
            person.last_name = last_name
        if city:
            person.city = city
        if country:
            person.country = country
        if birth_date:
            person.birth_date = birth_date

        session.commit()
        print("Запис успішно оновлено.")
    else:
        print("Запис із таким ID не знайдено.")

# Меню взаємодії
while True:
    print("\nОберіть опцію:")
    print("1 - Відображення всіх записів")
    print("2 - Фільтр за містом")
    print("3 - Комплексний фільтр (за країною та містом)")
    print("4 - Додати новий запис")
    print("5 - Видалити запис")
    print("6 - Оновити запис")
    print("7 - Вихід")
    option = input("Введіть номер опції: ")

    if option == "1":
        display_all()
    elif option == "2":
        city_name = input("Введіть назву міста: ").strip()
        results = session.query(Person).filter_by(city=city_name).all()
        if results:
            print("\nРезультат:")
            for row in results:
                print(f"{row.first_name} {row.last_name} | Місто: {row.city} | Країна: {row.country} | Дата народження: {row.birth_date}")
        else:
            print("\nРезультат відсутній.")
    elif option == "3":
        city_name = input("Введіть назву міста (або залиште порожнім): ").strip()
        country_name = input("Введіть назву країни (або залиште порожнім): ").strip()
        filters = []
        if city_name:
            filters.append(Person.city == city_name)
        if country_name:
            filters.append(Person.country == country_name)

        if filters:
            results = session.query(Person).filter(and_(*filters)).all()
            if results:
                print("\nРезультат:")
                for row in results:
                    print(f"{row.first_name} {row.last_name} | Місто: {row.city} | Країна: {row.country} | Дата народження: {row.birth_date}")
            else:
                print("\nРезультат відсутній.")

    elif option == "4":
        add_person()
    elif option == "5":
        delete_person()
    elif option == "6":
        update_person()
    elif option == "7":
        print("Завершення роботи з БД.")
        break

session.close()
