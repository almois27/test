**Запуск**
1. Создать и активировать виртуальное окружение

2. Установить зависимости
   
	 		(venv) \test>pip install -r requirements.txt

3. В 1 терминале запустить redis:

			(venv) \test>docker-compose up —build
	
	
   Во 2 терминале запустить celery:
	 
			(venv) \test\VideoFacesDetection> celery -A VideoFacesDetection worker -l info
	
	
   В 3 терминале запустить сервер:
	 
			(venv) \test\VideoFacesDetection> python manage.py runserver

4. Если все три службы запускаются правильно, перейти по адресу: 

		http://127.0.0.1:8000/processing/video/

