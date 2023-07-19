import requests

class HeadHunterAPI:
    """Класс для получения данных о работодателях и их вакансиях с сайта hh.ru."""

    def __init__(self) -> None:
        self.employers_ids: list[int] = [78638, 1740, 3529, 80660, 1122462, 1092837, 105904, 9501038, 1178447, 1455]
        self.url_employers: str = 'https://api.hh.ru/employers/'
        self.url_vacancies: str = 'https://api.hh.ru/vacancies'
        self.headers: dict[str] = {'User-Agent': '150014979'}

    def get_data_company(self) -> list[dict]:
        '''Получить данные о работодателях'''
        data = []
        for employer_id in self.employers_ids:
            try:
                response = requests.get(f"{self.url_employers}{employer_id}", headers=self.headers)
                if response.status_code == 200:
                    data_tmp = response.json()
                    data_company = {
                                    'employer_id': data_tmp['id'],
                                    'name': data_tmp['name'],
                                    'area': data_tmp['area']['name'],
                                    'open_vacancies': data_tmp['open_vacancies'],
                                    'url': data_tmp['site_url']
                                    }
                    data.append(data_company)
                    print(f"Данные о компани '{data_tmp['name']}' получены.")
                else:
                    print(f'Ошибка при получении данных о компаниях. Код ошибки: {response.status_code}')
                    break
            except requests.exceptions.RequestException as e:
                print(f"{e}")
        return data

    def get_data_vacancies(self) -> list[dict]:
        """Получить данные о вакансиях работодателей"""
        data = []
        vacancies = None
        for employer_id in self.employers_ids:
            try:
                page = 0
                pages = 1
                while page < pages:
                    params = {
                        'employer_id': employer_id,
                        'per_page': 100,
                        'page': page,
                        'archived': False
                    }
                    response = requests.get(url=self.url_vacancies, params=params, headers=self.headers)
                    if response.status_code == 200:
                        data_tmp = response.json()
                        data.extend(data_tmp['items'])
                        print(f"Данные о вакансиях {data_tmp['items'][0]['employer']['name']} страница {page} получены.")
                        page += 1
                        pages = data_tmp['pages']

                    else:
                        print(f'Ошибка при получении вакансий. Код ошибки: {response.status_code}')
                        break
            except requests.exceptions.RequestException as e:
                print(f"{e}")
            vacancies = self.__filter_vacancy(data)
        return vacancies

    @staticmethod
    def __filter_vacancy(vacancy_data: list[dict]) -> list[dict]:
        """Извлекает и конвертирует данные о вакансиях."""
        vacancies = []
        for vacancy in vacancy_data:
            if vacancy['type']['id'] == 'open':
                if vacancy['salary']:
                    if vacancy['salary']['from']:
                        salary = vacancy['salary']['from']
                    elif vacancy['salary']['from']:
                        salary = vacancy['salary']['from']
                else:
                    salary = 0
                processed_vacancy = {
                    "vacancy_id": vacancy["id"],
                    "employer_id": vacancy['employer']["id"],
                    "name": vacancy['name'],
                    'area': vacancy['area']['name'],
                    'title': vacancy['name'],
                    'salary': salary,
                    'url': vacancy['alternate_url'],
                    'date_published': vacancy['created_at'],
                    }
                vacancies.append(processed_vacancy)

        return vacancies

# if __name__ == '__main__':
#     a = HeadHunterAPI()
#     c = a.get_data_vacancies()
#     for i in c:
#         print(i)
#     # pprint(c)
#     # params = {
#     #     'employer_id': 78638,
#     #     'per_page': 100,
#     #     'page': 0}
#     # headers = {'User-Agent': '150014979'}
#     # response = requests.get(url='https://api.hh.ru/vacancies', params=params, headers=headers)
#     # d = response.json()
#     # pprint(d)