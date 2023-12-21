from tests.api import PetFriends
from tests.settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Метод делает запрос к API сервера и объявляет нового пользователя с валидными email и паролем """
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Метод делает запрос к API сервера и выводит питомцев по фильтру """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_create_pet(auth_key, name='Персик', animal_type='кот', age = 2):
    ''' Метод проверяет статус ключа 200 и проверяет, что пользователь создал питомца '''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    my_pet = pf.get_list_of_pets(auth_key, 'my_pet')

    if len(my_pet['pets']) > 0:
        status, result = pf.create_pet_simple(auth_key, my_pet['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result[name] == 'name'
    else:
        raise Exception('Это не мои питомцы')


def test_get_api_pets(auth_key, name, animal_type, age, pet_photo):
    '''  '''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_succesful_add_new_pet(name='Шуля', animal_type='кошка', age='2', pet_photo='kitty.jpg'):
    ''' Метод проверяет, что пользователь добавил нового питомца '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_succesful_delete_pet(auth_key, pet_id):
    ''' Метод проверяет, что пользователь удалил питомца '''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pet = pf.get_list_of_pets(auth_key, 'my_pet')

    pet_id = my_pet['pet'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    my_pet = pf.get_list_of_pets(auth_key, 'my_pet')

    assert status == 200
    assert pet_id not in my_pet.values()


def test_succesful_set_photo(pet_id='pet_id', pet_photo='kitty.jpg'):
    ''' Метод проверяет, что пользователь изменил фотографию питомца '''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result, my_pet = pf.get_list_of_pets(auth_key, pet_id, pet_photo)

    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert my_pet in my_pet.values()
