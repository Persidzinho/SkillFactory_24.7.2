import json.decoder

import requests


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'
        """ Метод сохраняет базовый URL сайта дома питомца под названием 'self' """

    def get_api_key(self, email, password):
        """ Метод делает запрос к API сервера и возвращает уникальный ключ пользователя,
        найденного по указанным им email и паролем """

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url+'/api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """ Метод делает запрос к API сервера и возвращает статус запроса и результат со списком
        найденных питомцев, совпадающих с фильтром """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key, name: str, animal_type: str, age: int):
        """ Метод добавляет информацию про питомца без фото """
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except res.text:
            result = res.text
        return status, result


    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        '''Добавляет информацию о новом питомце'''

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        headers = {'auth_key'}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        ''' Метод удаляет питомца '''
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + pet_id, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            res.text
        return
        status, result

    def set_photo(self, auth_key, pet_id, pet_photo):
        ''' Метод добавляет фото питомцу '''
        headers = {auth_key, pet_id, pet_photo}

        res = requests.post(self.base_url + 'api/pets/set_photo/{pet_id}', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            res.text

    def add_info_about_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        ''' Метод добавляет информацию о питомце '''
        headers = {auth_key, name, animal_type, age, pet_photo}

        res = requests.post(self.base_url + 'api/pets', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            res.text
        return status, result

