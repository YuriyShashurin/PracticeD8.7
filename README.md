# Example todoapp project

###Развертывание проекта на локальном устройстве:
В командной строке набираем: 
1. git clone https://github.com/YuriyShashurin/projectD5_10.git
2. Переходим в папку проекта: cd pets_site
3. Создаем командное окружение и запускаем его
   -python -m venv C:/YourFolder/pets_site/env
   - Launch: C:/YourFolder/pets_site> env\Scripts\activate.bat
4. Устанавливаем модули совместимостей pip install -r requirements.txt
5. запускаем проект python manage.py runserver

#####Вход в админку: 
http://127.0.0.1:8000/admin/

Логин: pws_admin<br/>
Пароль: sf_password

#####Модели: 
* Создание задач в моделе Todo items http://127.0.0.1:8000/admin/tasks/todoitem/
* Создание категорий в моделе Категории http://127.0.0.1:8000/admin/tasks/category/

###Проект на Хероку
https://rocky-coast-74518.herokuapp.com/

#####Админка: 
https://rocky-coast-74518.herokuapp.com/admin/
Логин: pws_admin<br/>
Пароль: sf_password

#####Страницы: 
* https://rocky-coast-74518.herokuapp.com/ - счетчики по категориям и приоритетам
* https://rocky-coast-74518.herokuapp.com/list/ - список задач
* https://rocky-coast-74518.herokuapp.com/cache_page/ - view c кэширование. Дата и время только через 5 минут
