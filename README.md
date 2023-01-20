Prerequisites:- Docker

1. Run setup and run project
   Commnad: docker-compose up --build -d

2. Create superuser
   - Go inside project container
     Command: docker exec -it website /bin/sh
   - Create superuser command
     Command: python manage.py createsuperuser
