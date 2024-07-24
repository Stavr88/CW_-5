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
    # создаем экземпляры классов HeadHunterAPI и DBManager
    get_hh_api = HeadHunterAPI()
    get_hh_api.create_table_in_postgresql(HOST, DB_NAME, USER, PASSWORD)  # после первого запуска необходимо замутить
    get_hh_api.load_in_postgresql(HOST, DB_NAME, USER, PASSWORD)  # после первого запуска необходимо замутить
    d_b_m = DBManager(HOST, DB_NAME, USER, PASSWORD)
    # создаем переменные с экземплярами классов для словаря
    get_companies_and_vacancies_count = d_b_m.get_companies_and_vacancies_count()
    get_all_vacancies = d_b_m.get_all_vacancies()
    get_avg_salary = d_b_m.get_avg_salary()
    get_vacancies_with_higher_salary = d_b_m.get_vacancies_with_higher_salary()

    # создание словаря с методами класса DBManager
    user_commands = {
        "a": get_companies_and_vacancies_count,
        "b": get_all_vacancies,
        "c": get_avg_salary,
        "d": get_vacancies_with_higher_salary
    }

    for i in user_commands:
        choice = input("Введите значение a,b,c,d (для п.п. a,b,c,d)\n"
                       " или ключевое слово например 'python' (для п.п.f)\n "
                       "или слова 'стоп', 'stop' для завершения поиска:")
        if choice == "стоп" or choice == "stop":
            break
        else:
            if choice == "a":
                for company in user_commands[choice]:
                    print(f"{company[0]} - {company[1]} вакансий")

            elif choice == "b":
                for company_vac in user_commands[choice]:
                    if company_vac[1] == 0 and company_vac[2] == 0:
                        salary = "Зарплата не указана."
                    elif company_vac[1] == 0 and company_vac[2] != 0:
                        salary = "Зарплата до " + str(company_vac[2]) + " руб."
                    elif company_vac[1] != 0 and company_vac[2] == 0:
                        salary = "Зарплата от " + str(company_vac[1]) + " руб."
                    else:
                        salary = "Зарплата от " + str(company_vac[1]) + " до " + str(company_vac[2]) + "  руб."
                    print(f"{company_vac[0]}. {salary} Ссылка: {company_vac[3]} Компания: {company_vac[4]}")

            elif choice == "c":
                print(f"Средняя зарплата по вакансиям составляет {int(user_commands[choice])} руб.")

            elif choice == "d":
                for company_vac in user_commands[choice]:
                    if company_vac[1] == 0 and company_vac[2] == 0:
                        salary = "Зарплата не указана."
                    elif company_vac[1] == 0 and company_vac[2] != 0:
                        salary = "Зарплата до " + str(company_vac[2]) + " руб."
                    elif company_vac[1] != 0 and company_vac[2] == 0:
                        salary = "Зарплата от " + str(company_vac[1]) + " руб."
                    else:
                        salary = "Зарплата от " + str(company_vac[1]) + " до " + str(company_vac[2]) + "  руб."

                    print(f"{company_vac[0]}. {salary} Ссылка: {company_vac[3]} Компания: {company_vac[4]}")

            else:
                get_vacancies_with_keyword = d_b_m.get_vacancies_with_keyword(choice)
                if get_vacancies_with_keyword == None:  # незнаю как обыграть, что бы выполнилось условие если ничего
                    # не нашлось
                    print('Профессия не найдена, повторите запрос:')
                else:
                    for company_vac in get_vacancies_with_keyword:
                        # if company_vac == None:
                        #     print('Профессия не найдена, повторите запрос:')
                        if company_vac[1] == 0 and company_vac[2] == 0:
                            salary = "Зарплата не указана."
                        elif company_vac[1] == 0 and company_vac[2] != 0:
                            salary = "Зарплата до " + str(company_vac[2]) + " руб."
                        elif company_vac[1] != 0 and company_vac[2] == 0:
                            salary = "Зарплата от " + str(company_vac[1]) + " руб."
                        else:
                            salary = "Зарплата от " + str(company_vac[1]) + " до " + str(company_vac[2]) + "  руб."

                        print(f"{company_vac[0]}. {salary} Ссылка: {company_vac[3]} ")


if __name__ == '__main__':
    main()
