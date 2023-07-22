from src.head_hunter_api import HeadHunterAPI
from src.db_manager import DBManager
from src.config_db import config


def main():
    print("Привествую, эта программа - парсер вакансий.")
    while True:
        try:
            print("_" * 30, "\nВыберите команду:\n"
                            "1. Обновить базу данных;\n"
                            "2. Получить список компаний и вакансий\n"
                            "3. Получить список всех вакансий\n"
                            "4. Получить среднюю зарплату по вакансиям\n"
                            "5. Получить список вакансий с ЗП выше средней\n"
                            "6. Поиск вакансий по ключевому слову\n"
                            "0. Выйти")
            command = int(input().strip())
            if command == 1:
                employers_data = hh_api.get_data_company()
                vacancies_data = hh_api.get_data_vacancies()
                db.create_tables()
                db.insert_employers_data(employers=employers_data)

                db.insert_vacancies_data(vacancies=vacancies_data)

            if command == 2:
                db.get_companies_and_vacancies_count()
            if command == 3:
                db.get_all_vacancies()
            if command == 4:
                db.get_avg_salary()
            if command == 5:
                db.get_vacancies_with_higher_salary()
            if command == 6:
                key_word = input('Введите ключевое слово: ').strip()
                db.get_vacancies_with_keyword(key_word)
            if command == 0:
                db.close_connection()
                print("Прогрмма завершает работу")
                break

        except ValueError:
            print("Команда должна быть числом")


if __name__ == '__main__':
    db_name = 'head_hunter'
    hh_api = HeadHunterAPI()
    db = DBManager(config)
    db.create_database(db_name=db_name)
    db.update_config(db_name=db_name)
    db.reconnect()
    main()
