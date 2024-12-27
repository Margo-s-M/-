from sqlalchemy import create_engine , Column, Integer, String, Sequence, DATE,or_,and_
from  sqlalchemy.orm import sessionmaker
from  sqlalchemy.orm import declarative_base
import json

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

while True:
        print("оберіть опцію")
        print("1 - відображення")
        print("2 - фільтр за містом")
        print("3 - комплексний фільтр,за країною та містом ")
        print("4 - вихід")
        option = input("введіьт номер опції")
        if option =="1":
            result = session.query(Person).all()
        elif option == "2":
            city_name = input("введіть назву міста")
            result = session.query(Person).filter_by(city=city_name).all()
        elif option == "3":
            city_name = input("введіть назву міста").strip()
            country_name = input("введіть назву країни").strip()
            filters = []
            if city_name:
                filters.append(Person.city == city_name)
            if country_name:
                filters.append(Person.country == country_name)

            if filters:
                result = session.query(Person).filter(and_(*filters)).all()
        elif option == "4":
            print("завершення роботи з БД")
            break

        if result:
            print("Peзультат")
            for row in result:
                print(f"{row.first_name} {row.last_name} | Місто: {row.city} | Країна: {row.country} | Дата народження: {row.birth_date}")
        else:
            print("Результат відсутній")
session.close()