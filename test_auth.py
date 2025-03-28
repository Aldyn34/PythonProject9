import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def load_config():
    """Fixture для загрузки конфигурационного файла."""
    with open('config.json') as f:
        config = json.load(f)
    return config

@pytest.fixture
def setup():
    """Fixture для настройки веб-драйвера."""
    driver = webdriver.Chrome()  # Убедитесь, что драйвер установлен и доступен в PATH
    driver.get("https://b2c.passport.rt.ru/")  # URL вашего приложения
    yield driver
    driver.quit()

def test_registration_new_user(setup, load_config):
    """Тест регистрации нового пользователя."""
    driver = setup
    config = load_config

    try:
        # Переход на страницу регистрации
        register_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))
        )
        register_link.click()

        # Заполнение формы регистрации
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        driver.find_element(By.NAME, "email").send_keys(config["email"])
        driver.find_element(By.NAME, "password").send_keys(config["password"])
        driver.find_element(By.NAME, "confirm_password").send_keys(config["password"])

        # Нажатие кнопки регистрации
        driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]").click()

        # Проверка сообщения об успешной регистрации
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message"))
        ).text
        assert "Регистрация успешна" in success_message
        logging.info("Тест регистрации прошел успешно.")
    except Exception as e:
        logging.error("Ошибка в тесте регистрации: %s", e)
        raise

def test_login_existing_user(setup, load_config):
    """Тест входа для существующего пользователя."""
    driver = setup
    config = load_config

    try:
        # Переход на страницу входа
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Войти"))
        )
        login_link.click()

        # Заполнение формы входа
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        driver.find_element(By.NAME, "email").send_keys(config["email"])
        driver.find_element(By.NAME, "password").send_keys(config["password"])

        # Нажатие кнопки входа
        driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Проверка сообщения о приветствии
        welcome_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".welcome-message"))
        ).text
        assert "Добро пожаловать" in welcome_message
        logging.info("Тест входа прошел успешно.")
    except Exception as e:
        logging.error("Ошибка в тесте входа: %s", e)
        raise

def test_password_reset(setup, load_config):
    """Тест сброса пароля."""
    driver = setup
    config = load_config

    try:
        # Переход на страницу сброса пароля
        forgot_password_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Забыли пароль?"))
        )
        forgot_password_link.click()

        # Заполнение формы сброса пароля
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        driver.find_element(By.NAME, "email").send_keys(config["email"])

        # Нажатие кнопки сброса пароля
        driver.find_element(By.XPATH, "//button[contains(text(), 'Сбросить пароль')]").click()

        # Проверка сообщения об успешном сбросе пароля
        reset_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".reset-message"))
        ).text
        assert "Инструкция по сбросу пароля отправлена" in reset_message
        logging.info("Тест сброса пароля прошел успешно.")
    except Exception as e:
        logging.error("Ошибка в тесте сброса пароля: %s", e)
        raise

def test_elements_presence(setup):
    """Тест проверки наличия ключевых элементов на главной странице."""
    driver = setup

    try:
        assert WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Зарегистрироваться")))
        assert WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Войти")))
        logging.info("Тест наличия элементов прошел успешно.")
    except Exception as e:
        logging.error("Ошибка в тесте наличия элементов: %s", e)