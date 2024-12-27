from sqlalchemy import create_engine , Column, Integer, String, Sequence, DATE
from  sqlalchemy.orm import sessionmaker
from  sqlalchemy.orm import declarative_base
import json
from sqlalchemy.sql import text
#create_engine -створює обєкт engine представляє зєднання з БД
 #COLUMN представляє колонку таблиці бд
#Integer, String тип даних колонки
#Sequence для визначення послідовності (генерація унікальні ід)
#sessionmaker обєкт який обгортає зєднання з бд
#declerative_base - дозволяє вик.декларативний спосіб


with open("config.json") as f:
    config = json.load(f)

db_user = config["database"]["user"]
db_password = config["database"]["password"]

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/People"
engine = create_engine(db_url)

Base = declarative_base()
class Person(Base):
    __tablename__ = "people"
    id = Column(Integer,primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    birth_date = Column(DATE)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()#сесія для взаємодії з бд

# person1 = Person(first_name = "Jon",last_name = "Doe", city = "New York",
#                  country = "USA", birth_date = "1998-03-22" )
#
# person2 = Person(first_name = "Jonny",last_name = "Boe", city = "London",
#                  country = "Uk", birth_date = "1998-08-22" )
#
# session.add_all([person1,person2])
# session.commit()

while True:
        user_query = input("Ведіть селект запит або exit")
        if user_query.lower() == "exit":
            break
        try:
            if "UPDATE" in user_query.upper() or "DELETE" in user_query.upper():
                if "WHERE" not in user_query.upper():
                    raise ValueError("Запит на оновлення має містити умову WHERE ")
            result = session.execute(text(user_query))
            session.commit()
            if user_query.strip().upper().startswith("SELECT"):
             rows = result.fetchall()
             if rows:
                print("Result")
                for row in rows:
                    print(row)
             else:
                print("Рузультат відсутній")
             print("Операція пройшла успішно")

        except Exception as e:
            print(f"Помилка виконання запиту:{str(e)}")
session.close()