--- создает таблицу employers
CREATE TABLE employers (
                    employer_id int PRIMARY KEY,
                    employer_name varchar(100) NOT NULL,
                    employer_area varchar(100) NOT NULL,
                    open_vacancies int NOT NULL,
                    employer_url varchar(150) NOT NULL;
--- создает таблицу vacancies
CREATE TABLE vacancies (
                    vacancy_id int PRIMARY KEY,
                    employer_id int,
                    vacancy_name text NOT NULL,
                    vacancy_area varchar(100) NOT NULL,
                    salary int NOT NULL,
                    vacancy_url varchar(100) NOT NULL,
                    date_published DATE NOT NULL;

ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers
                            FOREIGN KEY(employer_id) REFERENCES employers(employer_id);

--- получает список всех компаний и количество вакансий у каждой компании.
SELECT employer_name, open_vacancies FROM employers;

--- получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT employer_name, vacancy_name, salary, vacancy_url
                FROM vacancies
                JOIN employers USING (employer_id);

--- получает среднюю зарплату по вакансиям.
SELECT avg(salary)::int
                FROM vacancies;
--- получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT employer_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            JOIN employers USING (employer_id)
            WHERE salary > (SELECT avg(salary)::int
                            FROM vacancies);
--- получает список всех вакансий, в названии которых содержатся переданные в метод слова.
SELECT employer_name, vacancy_name, salary, vacancy_url
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE vacancy_name ILIKE key_word