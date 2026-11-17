[![Python Tests](https://github.com/mortiest-morty/qa-task/actions/workflows/ci.yml/badge.svg)](https://github.com/mortiest-morty/qa-task/actions/workflows/ci.yml)

# Тестовое задание QA

Исходное задание: Effective Mobile, каталог Hexlet - https://github.com/Hexlet/ru-test-assignments/tree/main/qa/effective-mobile

Проект содержит два автоматизированных теста:

1. E2E UI-тест покупки товара на SauceDemo.
2. Тест GitHub API для создания, проверки и удаления публичного репозитория.

## Требования

- Python 3.10 или новее
- Google Chrome
- GitHub Personal Access Token с правами:
  - `Contents: Read and write`
  - `Administration: Read and write`

Для классического токена GitHub потребуется scope `repo`.

## Установка

Клонировать репозиторий и перейти в его каталог:

```bash
git clone <repository-url>
cd qa-test-task
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

Скопировать пример конфигурации.

Linux/macOS:

```bash
cp .env.example .env
```

Windows:

```bash
copy .env.example .env
```

Заполнить в `.env` реальные значения:

```text
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_token
GITHUB_REPOSITORY=qa-api-test
```

`GITHUB_REPOSITORY` используется как префикс. Во время теста к нему добавляется уникальный суффикс, поэтому существующие репозитории не перезаписываются.

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

```powershell
$env:HEADLESS="false"
pytest tests/test_e2e.py -v
```

Selenium Manager автоматически подбирает подходящий ChromeDriver.

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

Удаление выполняется в блоке `finally`, включая случаи падения проверки.

## Запуск всех тестов

```bash
 pytest tests/test_e2e.py -v — запуск UI-теста
 pytest tests/test_api.py -v — запуск API-теста
```

## Безопасность

Файл `.env` не должен добавляться в Git. Он уже включён в `.gitignore`.

