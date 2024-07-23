import psycopg2



class DBManager:
    """
    Подключаеться к БД PostgreSQL
    """
    def __init__(self, host: str, dbname: str, user: str, password: str):

        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.con = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password
            )

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return:
        """
        with self.con.cursor() as cursor:
            cursor.execute(
                "SELECT employers.company_name, "
                "COUNT(vacancies.vacancy_id) FROM employers "
                "LEFT JOIN vacancies USING(employer_id) "
                "GROUP BY employers.company_name"
            )
            return cursor.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        with self.con.cursor() as cursor:
            cursor.execute(
                "SELECT title, salary_from, salary_to, vacancies.url, employers.company_name "
                "FROM vacancies "
                "LEFT JOIN employers USING(employer_id) "
                )
            return cursor.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        with self.con.cursor() as cursor:
            cursor.execute("SELECT salary_from, salary_to FROM vacancies")
            count = 0
            value_salary = 0
            for row in cursor.fetchall():
                if row[0] != 0 and row[1] != 0:
                    value_salary += (row[1] - row[0])/2 + row[0]
                    count += 1
                elif row[0] != 0 and row[1] == 0:
                    value_salary += row[0]
                    count += 1
                elif row[0] == 0 and row[1] != 0:
                    value_salary += row[1]
                    count += 1
            return value_salary / count

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        average_salary = int(self.get_avg_salary())
        higher_salary_list = []
        for row in self.get_all_vacancies():
            if row[1] > average_salary:
                higher_salary_list.append(row)
            elif row[2] > average_salary:
                higher_salary_list.append(row)
            elif (row[2] - row[1]) / 2 + row[1] > average_salary:
                higher_salary_list.append(row)
        return higher_salary_list

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий, в названии
        которых содержатся переданные в метод слова, например "python".
        """
        query = f"SELECT title, salary_from, salary_to, url FROM vacancies WHERE title LIKE '%{keyword}%'"
        with self.con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
