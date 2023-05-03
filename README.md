##  Blog Django project

--------
This web application creates a blog, where users can create post and comments.

The main features that have currently been implemented are:

Users can view list and detail information for posts and authors, also user can contact with admin.
Users can update profile, edit post.
--------
**How to start project**
* install all from requirements.txt
* for start project write in terminal:
```
python manage.py runserver
```
* for creating 10 users write in terminal:
```
./manage.py create_users
```
* for create 2000 posts
```
./manage.py create_post
```
* for create 1000 comments
```
./manage.py create_comment
```
* for loading fixtures:
  * clear table:
```
./manage.py flush
```
  * load fixtures
```
./manage.py loaddata fixtures/db.json
```
* for check apps:
```
http://127.0.0.1:8000/
```
* for start celery:
```
celery -A core worker --loglevel=info
```
* for starts the celery beat service:
```
celery -A core beat -l info
```
* for start rabbitmq-server:
```
sudo systemctl start rabbitmq-server
```
* Quit the server with CONTROL-C.
--------
Project checked by flake8