# Сервис "Биржа труда"
Учебный сервис в рамках разработки тестового приложения школы "Айти в нефти"

**С заданием можно ознакомиться в файле [TASK.md](TASK.md)**

Инструкция по настройке среды для разработки:
Работаем из корневого каталога

1) Создайте виртуальное окружение
```bash
python -m venv venv
```зне
2) Активируйте его, также выберите его в настройках
`Pycharm Settings/Project/Python Intepreter`,
чтобы оно автоматически подхватывалось
```bash
venv\Scripts\activate
```
3) Установите необходимые библиотеки
```bash
pip install -r requirements.txt
```
4) Поднимите базу:
```bash
docker-compose up 
```
5) Накатите миграцию:
```shell
alembic upgrade head
```
6) Запустите файлик `src/main.py` через pycharm или командой
```bash
python src/main.py
```
7) Теперь приложение запущено и доступно по адресу `localhost:8080/docs`
