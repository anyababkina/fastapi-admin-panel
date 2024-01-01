import pytest


# Вход на страницы со свободным доступом
@pytest.mark.parametrize('url', ['/registration', '/login'])
async def test_pages_registration_login(ac, url):
    response = await ac.get(url)
    assert response.status_code == 200


# Перенаправление на страницу со входом при попытке обратиться к страницам, доступным только авторизованным пользователям
async def test_redirect_if_user_not_logged(ac):
    response = await ac.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert response.url.path == '/login'


# Регистрация
async def test_registry(ac):
    response = await ac.post(
        '/registration',
        data={'email': 'test@test.com', 'username': 'test', 'password': '12345678'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.url.path == '/login'


# Ошибка регистрации если такое имя пользователя или почта существуют
async def test_registry_failed_when_email_or_username_already_exists(ac):
    response = await ac.post(
        '/registration',
        data={'email': 'admin@example.com', 'username': 'test', 'password': '12345678'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        follow_redirects=True
    )
    assert response.status_code == 422
    assert response.json()['detail'] == 'Username and/or email is occupied'

    response = await ac.post(
        '/registration',
        data={'email': 'test@test.com', 'username': 'admin', 'password': '12345678'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        follow_redirects=True
    )
    assert response.status_code == 422
    assert response.json()['detail'] == 'Username and/or email is occupied'


# Авторизация пользователя, установка кук при логине. Удаление кук при выходе.
async def test_login_logout_and_set_cookie(ac):
    response = await ac.post(
        '/login',
        data={'email': 'admin@example.com', 'password': '12345678'},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert response.cookies.get('admin_cookie') is not None

    response = await ac.get('/logout', follow_redirects=False)

    assert response.status_code == 302
    assert response.cookies.get('admin_cookie') is None



