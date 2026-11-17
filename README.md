[![Python Tests](https://github.com/mortiest-morty/qa-task/actions/workflows/ci.yml/badge.svg)](https://github.com/mortiest-morty/qa-task/actions/workflows/ci.yml)

# Тестовое задание QA: E2E-тест покупки на SauceDemo и API-тест GitHub

Автоматизированные тесты для тестового задания Effective Mobile (QA):
E2E UI-тест покупки товара на SauceDemo и API-тест управления репозиторием GitHub.

**Исходное задание:** Effective Mobile, каталог Hexlet —
https://github.com/Hexlet/ru-test-assignments/tree/main/qa/effective-mobile

## Что сделано

- E2E UI-тест покупки на SauceDemo: авторизация, добавление товара «Sauce Labs Backpack» в корзину, проверка наличия товара в корзине, заполнение полей оформления, завершение заказа и проверка подтверждения.
- API-тест GitHub: создание публичного репозитория, проверка его наличия в списке репозиториев пользователя, проверка публичности, удаление в блоке `finally`.
- CI в GitHub Actions: тесты запускаются автоматически по пушу и pull request.
- Инструкция по запуску и настройке окружения (этот README).

## Требования

- Python 3.10 или новее
- Google Chrome
- GitHub Personal Access Token с правами:
  - Fine-grained token: `Administration: Read and write`, `Contents: Read and write`
  - Классический токен: scope `repo`

## Установка

Клонировать репозиторий и перейти в его каталог:
```bash
git clone https://github.com/mortiest-morty/qa-task.git
cd qa-task
```

Создать виртуальное окружение:
```bash
python -m venv .venv
```

Активировать его.
Linux/macOS:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

Установить зависимости:
```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

В репозитории лежит файл .env.example (пример конфигурации). Рабочий файл .env создаётся из него и не коммитится в Git (он добавлен в .gitignore).
Скопировать пример конфигурации.

Linux/macOS:
```bash
cp .env.example .env
```
Windows:
```bash
copy .env.example .env
```

Заполнить в .env реальные значения:
```bash
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_token
GITHUB_REPOSITORY=qa-api-test
```

GITHUB_REPOSITORY используется как префикс: во время теста к нему добавляется уникальный суффикс, поэтому существующие репозитории не перезаписываются.

## Запуск E2E-теста

По умолчанию Chrome запускается в headless-режиме:
```bash
pytest tests/test_e2e.py -v
```
Чтобы увидеть работу браузера.

Linux/macOS:
```bash
HEADLESS=false pytest tests/test_e2e.py -v
```

Windows PowerShell:
```bash
$env:HEADLESS="false"; pytest tests/test_e2e.py -v
```
ChromeDriver подбирается Selenium Manager автоматически под установленную версию Chrome. Если автоматический подбор не сработал, версия браузера фиксируется в опциях Chrome в коде теста.

## Запуск GitHub API-теста
```bash
pytest tests/test_api.py -v
```

Тест выполняет следующие операции:

  1. Создаёт публичный репозиторий.
  2. Получает список репозиториев пользователя.
  3. Проверяет наличие созданного репозитория.
  4. Проверяет, что репозиторий публичный.
  5. Удаляет временный репозиторий.

Удаление выполняется в блоке finally, включая случаи падения проверки.

##Запуск всех тестов
```bash
pytest -v
```

Отдельно:
```bash
pytest tests/test_e2e.py -v   # только UI-тест
pytest tests/test_api.py -v   # только API-тест
```

## CI
https://github.com/mortiest-morty/qa-task/actions/workflows/ci.yml/badge.svg

Тесты запускаются в GitHub Actions по пушу и pull request (workflow: .github/workflows/ci.yml).
Для запуска API-теста в CI токен передаётся через секрет репозитория GH_TOKEN.

```bash
.github/
  workflows/
    ci.yml           # Конфигурация GitHub Actions
tests/
  __init__.py
  test_e2e.py        # E2E UI-тест покупки на SauceDemo
  test_api.py        # API-тест GitHub
.env.example         # Пример переменных окружения
.gitignore
README.md
requirements.txt
```

## Безопасность
Файл .env не должен добавляться в Git. Он уже включён в .gitignore.
Токен GitHub хранится только в переменных окружения и не попадает в код.
