from src.class_db_manager import DBManager
from src.class_get_hh_api import HeadHunterAPI
from src.config import HOST, DB_NAME, USER, PASSWORD

def main():
    """
    Функция для взаимодействия с пользователем
    :return:
    """
    print("Для дальнейшей работы программы выберите пункт:\n"
          "a - Получить список всех компаний и узнать количество вакансий у каждой компании \n"
          "b - Получить список всех вакансий с указанием названия "
          "компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          "c - Получить среднюю зарплату по вакансиям\n"
          "d - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
          "f - Введите ключевое слово, что бы получить список всех вакансий по ключевому слову - \n")

    # choice = input("Введите значение (для п.п. a,b,c,d) или ключевое слово (для п.п.f):")

    get_hh_api = HeadHunterAPI()
    # get_hh_api.load_in_postgresql(HOST, DB_NAME, USER, PASSWORD)
    d_b_m = DBManager(HOST, DB_NAME, USER, PASSWORD)
    get_companies_and_vacancies_count = d_b_m.get_companies_and_vacancies_count()
    get_all_vacancies = d_b_m.get_all_vacancies()
    get_avg_salary = d_b_m.get_avg_salary()
    get_vacancies_with_higher_salary = d_b_m.get_vacancies_with_higher_salary()
    # get_vacancies_with_keyword = d_b_m.get_vacancies_with_keyword(choice)

    user_commands = {
        "a": get_companies_and_vacancies_count,
        "b": get_all_vacancies,
        "c": get_avg_salary,
        "d": get_vacancies_with_higher_salary
    }

    for i in user_commands:
        choice = input("Введите значение a,b,c,d (для п.п. a,b,c,d) или ключевое слово например 'python' (для п.п.f):")
        if choice in ("a", "b", "c", "d"):
            print(user_commands[choice])
            break
        else:
            print(d_b_m.get_vacancies_with_keyword(choice))
        break


if __name__ == '__main__':
    main()

