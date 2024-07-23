from abc import ABC, abstractmethod
import requests
import psycopg2
# from config import HOST, DB_NAME, USER, PASSWORD


class Parser(ABC):
    """
    Абстрактный родительский класс для взаимодействия с API
    """

    @abstractmethod
    def connect_postgresql(self, *args, **kwargs):
        pass


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter и сохранением данных в БД PostgreSQL
    """
    __url: str
    __headers: dict
    __params: dict

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {"employer_id": (3529, 78638, 1272486, 3388, 4233, 2180, 64174, 83056, 1433, 208189),
                         "area": "113",
                         "per_page": 100}

    @staticmethod
    def connect_postgresql(host: str, dbname: str, user: str, password: str):
        """
        Выполняет подключение к БД PostgreSQL
        :param host: str
        :param dbname: str
        :param user: str
        :param password: str
        """
        try:
            con = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password
            )
            con.autocommit = True
        except:
            print('Ошибка подключения')
        return con

    def load_in_postgresql(self, host: str, dbname: str, user: str, password: str):
        """
        Выполняет выгрузку данных с hh.ru о вакансиях и фирмах в БД PostgreSQL
        :return:
        """
        # Создаем таблицы в БД PostgreSQL
        with self.connect_postgresql(host, dbname, user, password).cursor() as curs:
            curs.execute(
                "CREATE TABLE employers("
                "employer_id int PRIMARY KEY NOT NULL, "
                "company_name varchar(255), "
                "url varchar(255));"
            )
            curs.execute(
                "CREATE TABLE vacancies("
                "vacancy_id int PRIMARY KEY NOT NULL, "
                "salary_from int, "
                "salary_to int, "
                "title varchar(255), "
                "url varchar(255), "
                "employer_id int REFERENCES employers(employer_id))"
            )
            # Загружаем данные в БД PostgreSQL с сайта hh.ru с условием если salary_from/salary_to нет, присвоить 0
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            for item in response.json()['items']:
                if item['salary'] is None:
                    salary_from = 0
                    salary_to = 0
                else:
                    salary_from = item['salary']['from']
                    salary_to = item['salary']['to']
                if salary_from == None:
                    salary_from = 0
                if salary_to == None:
                    salary_to = 0

                curs.execute(
                    "INSERT INTO employers (employer_id, company_name, url) "
                    "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (item['employer']['id'],
                     item['employer']['name'],
                     item['employer']['alternate_url'])
                )

                curs.execute(
                    "INSERT INTO vacancies (vacancy_id, salary_from, salary_to, title, url, employer_id)"
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    (item['id'],
                     salary_from,
                     salary_to,
                     item['name'],
                     item['alternate_url'],
                     item['employer']['id'])
                )


# a = HeadHunterAPI()
# a.load_in_postgresql(HOST, DB_NAME, USER, PASSWORD)

