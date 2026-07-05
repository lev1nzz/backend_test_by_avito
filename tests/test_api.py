from fastapi.testclient import TestClient

def test_client_running(client: TestClient):
    '''Проверяет запуск сервера'''
    response = client.get('/')
    
    assert response.status_code == 404
    
    
def test_create_short_url(client:TestClient):
    '''Проверка, что можно создать короткую ссылку'''
    # 1. Подготовка данных
    test_data = {
        'url': 'https://github.com/community-of-python/pylines/blob/main/tests.md'
    }
    
    # 2. Проводим действие - отправляем запрос
    response = client.post('/short_url', json=test_data)
    
    # 3. Проверяем результат 
    assert response.status_code == 200
    assert 'short_url' in response.json() # проверка что есть короткая урл
    # Совпадает ли урл
    assert response.json()['url'] == 'https://github.com/community-of-python/pylines/blob/main/tests.md'
    

def test_redirect_to_url(client: TestClient):
    '''Проверка на редирект'''
    # 1. Подготовка данных
    create_response = client.post('/short_url', json={
        'url': 'https://github.com/community-of-python/pylines/blob/main/tests.md'
    })
    
    short_slug = create_response.json()['short_url']
    
    # 2. Проводим действие - отправляем запрос на редирект 
    redirect_response = client.get(f'{short_slug}', follow_redirects=False)
    
    # 3. Проверяем результат
    assert redirect_response.status_code == 301
    assert redirect_response.headers['location'] == 'https://github.com/community-of-python/pylines/blob/main/tests.md'

def test_create_empty_url(client: TestClient):
    '''Проверка на создание короткого урла с путсой ссылкой'''
    # 1. Подготовка данных 
    test_data_url = {
        'url': ''
    }
    
    # 2. Проводим действие - отправляем запрос 
    response = client.post('/short_url', json=test_data_url)
    
    # 3. Проверяем результат 
    assert response.status_code == 422

 
def test_create_short_slug_none_date(client: TestClient):
    '''Проверка создания короткого урла без ссылки'''
    # 1. Подготовка данных 
    test_data_withot_url = {}
    
    # 2. Проводим действие - отправляем запрос 
    response = client.post('/short_url', json=test_data_withot_url)
    
    # 3. Проверяем результат
    assert response.status_code == 422
    
def test_redirect_noneextantion_url(client: TestClient):
    '''Проверка на переход по несуществющей ссылке'''
    
    # 1. Подготовка данных и проводим действие - отправляем запрос 
    response = client.get('/test123124')
    
    # 2. Проверяем результат
    assert response.status_code == 404