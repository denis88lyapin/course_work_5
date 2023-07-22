import psycopg2
from configparser import ConfigParser


class DBManager:

    def __init__(self, config) -> None:
        self.config_file = "src/database.ini"
        self.config = config
        self.params = self.config()
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def update_config(self, db_name='postgres'):
        """Обновление параметра dbname в файле конфигурации."""
        parser = ConfigParser()
        parser.read(self.config_file)
        parser.set("postgresql", "dbname", db_name)
        with open(self.config_file, "w") as config_file:
            parser.write(config_file)

    def reconnect(self):
        """Переподключение к базе данных с новыми параметрами"""
        self.close_connection()
        self.params = self.config()
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_database(self, db_name: str) -> None:
        """
        Создание базы данных
        """
        try:
            self.cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
            self.cur.execute(f'CREATE DATABASE {db_name}')
            print(f"БД {db_name} успешно создана")
            self.update_config(db_name)
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_tables(self):
        """Создает таблицы employers и vacancies."""
        try:
            self.cur.execute('''DROP TABLE IF EXISTS employers CASCADE''')
            self.cur.execute(
                """
                CREATE TABLE employers (
                    employer_id int PRIMARY KEY,
                    employer_name varchar(100) NOT NULL,
                    employer_area varchar(100) NOT NULL,
                    open_vacancies int NOT NULL,
                    employer_url varchar(150) NOT NULL
                )
                """
            )
            self.cur.execute('''DROP TABLE IF EXISTS vacancies CASCADE''')
            self.cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id int PRIMARY KEY,
                    employer_id int,
                    vacancy_name text NOT NULL,
                    vacancy_area varchar(100) NOT NULL,
                    salary int NOT NULL,
                    vacancy_url varchar(100) NOT NULL,
                    date_published DATE NOT NULL
                                        )
                """
            )
            self.cur.execute(
                '''
                            ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers
                            FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
                            '''
            )
            print("Таблицы employers и vacancies успешно созданы")
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_employers_data(self, employers: list[dict]) -> None:
        """Добавляет данные из suppliers в таблицу suppliers."""
        try:
            for employer in employers:
                self.cur.execute(
                    '''
                    INSERT INTO employers (employer_id, employer_name, employer_area, open_vacancies, employer_url)
                    VALUES (%s, %s, %s, %s, %s)

                    ''',
                    (employer.get('employer_id'), employer.get('name'), employer.get('area'),
                     employer.get('open_vacancies'), employer.get('url'))
                )
            print('Данные в таблицу employers успешно добавлены')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_vacancies_data(self, vacancies: list[dict]) -> None:
        """Добавляет данные из suppliers в таблицу suppliers."""
        try:
            for vacancy in vacancies:
                self.cur.execute(
                    '''
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, vacancy_area, salary, vacancy_url, date_published)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)

                    ''',
                    (vacancy.get('vacancy_id'), vacancy.get('employer_id'), vacancy.get('name'), vacancy.get('area'),
                     vacancy.get('salary'), vacancy.get('url'), vacancy.get('date_published'))
                )
            print('Данные в таблицу vacancies успешно добавлены')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_companies_and_vacancies_count(self) -> None:
        """
        получает список всех компаний и
        количество вакансий у каждой компании.
        """
        try:
            self.cur.execute(
                """
                SELECT employer_name, open_vacancies FROM employers
                """
            )
            data = self.cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        for item in data:
            print(f"Компания: {item[0]}, вакансий: {item[1]}")

    def get_all_vacancies(self) -> None:
        """
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        try:
            self.cur.execute(
                """
                SELECT employer_name, vacancy_name, salary, vacancy_url 
                FROM vacancies
                JOIN employers USING (employer_id)
                """
            )
            data = self.cur.fetchall()
            for item in data:
                print(f"Компания: {item[0]}, вакансия: {item[1]}, ЗП: {item[2]} URL: {item[3]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при получении данных:", error)

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        """
        try:
            self.cur.execute(
                """
                SELECT avg(salary)::int
                FROM vacancies
                """
            )
            data = self.cur.fetchall()

            print(f"Средняя ЗП: {data[0][0]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при получении данных:", error)

    def get_vacancies_with_higher_salary(self) -> None:
        """
        получает список всех вакансий, у которых зарплата выше средней
        по всем вакансиям.
        """
        try:
            self.cur.execute(
                """
                SELECT employer_name, vacancy_name, salary, vacancy_url 
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE salary > (SELECT avg(salary)::int
                                FROM vacancies)
                """
            )
            data = self.cur.fetchall()
            for item in data:
                print(f"Компания: {item[0]}, вакансия: {item[1]}, ЗП: {item[2]} URL: {item[3]}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при получении данных:", error)

    def get_vacancies_with_keyword(self, key_word: str) -> None:
        """
        Получает список всех вакансий, в названиях которых содержатся переданные в метод слова, например “python”.
        """
        try:
            self.cur.execute(
                """
                SELECT employer_name, vacancy_name, salary, vacancy_url 
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE vacancy_name ILIKE %s
                """,
                ('%' + key_word + '%',)
            )
            data = self.cur.fetchall()
            if data:
                for item in data:
                    print(f"Компания: {item[0]}, вакансия: {item[1]}, ЗП: {item[2]} URL: {item[3]}")
            else:
                print(f"Нет вакансий с ключевым словом {key_word}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при получении данных:", error)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
