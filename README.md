<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat"> <img src="https://img.shields.io/badge/-React-555.svg?logo=react&style=flat"> <img src="https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=flat"> <img src="https://img.shields.io/badge/-Sass-CC6699.svg?logo=sass&style=flat"> <img src="https://img.shields.io/badge/-PostgreSQL-336791.svg?logo=postgresql&style=flat"> <img src="https://img.shields.io/badge/-Docker-EEE.svg?logo=docker&style=flat"> <img src="https://img.shields.io/badge/-Heroku-430098.svg?logo=heroku&style=flat"> <img src="https://img.shields.io/badge/-CircleCI-343434.svg?logo=circleci&style=flat">

# [Atom](https://immense-falls-08135.herokuapp.com/)

Technique/Version:

local

- docker==20.10.0
- docker-compose==1.25.5
- python==3.7.10
- pip==20.2.1
- django==2.2.13
- node==12.16.2
- react
- bootstrap(cdn)==4.5.0
- scss
- sass compiler(vscode plugin)
- minifer(vscode plugin)
- postgresql
- circleci==0.2.1

unique to production

- heroku==7.50.0
- gunicorn
- node==12.16.2

## How to SetUp Docker?

https://inglow.jp/techblog/docker-django/

- [ ] To start Docker based on the image,

```
$ docker-compose up -d
```

Option "d" allows detouch mode.

- [ ] To stop Docker,

```
$ docker-compose stop
```

- [ ] To restart Docker,

```
$ docker-compose restart
```

- [ ] To check Docker's status,

```
$ docker ps
```

- [ ] To create new application,

```
$ docker-compose exec django python manage.py startapp hogehoge
```

- This is the basic template to do something at the Docker container.

```
$ docker container exec -it {container_name} {command}
```

- [ ] To migrate your model,

```
$ docker container exec -it atom_django_1 python manage.py makemigrations
```

```
$ docker container exec -it atom_django_1 python manage.py migrate
```

- [ ] To apply environment variables to Docker,

```
$ docker run -e hoge="hogehoge" -e hugo="hugohugo" ... django env
```

- [ ] To confirm environment variables to Docker,

```
$ docker-compose run --rm django env
```

## How to run local server with React?

https://hodalog.com/tutorial-django-rest-framework-and-react/

- [ ] Install create-react-app and use it to create app.

```
$ docker-compose run --rm react sh -c "npm i -g create-react-app && create-react-app hogehoge"
```

- [ ] Install npm.

```
$ docker-compose run --rm react npm install
```

- [ ] Run server.

```
$ docker-compose run --rm --service-ports node npm start
```

## How to deploy to Heroku?

https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app

[Docker and Heroku combination is here](https://qiita.com/yongjugithub/items/822e5f2f6211b2665acf)

- [ ] If you are Mac user, install Heroku.

```
$ brew install heroku/brew/heroku
```

- [ ] Login to Heroku.

```
$ heroku login
```

- [ ] Make the space(=URL) where the application will be deployed.

```
$ heroku create
```

- [ ] Push local repository to the Heroku remote repository.

```
$ git push heroku master
```

- [ ] To use python command at Heroku remote repository,

```
$ heroku run python manage.py hogehoge
```

- [ ] You can see your application on the Internet.

```
$ heroku open
```

- [ ] To stop Heroku, stop every https processes.

```
$ heroku ps:scale web=0
```

- [ ] To restart Heroku,

```
$ heroku ps:scale web=1
```
