![screen](https://user-images.githubusercontent.com/71208265/117562308-f5e85280-b0d8-11eb-9f35-d4bb0c0d0b45.png)

<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat"> <img src="https://img.shields.io/badge/-React-555.svg?logo=react&style=flat"> <img src="https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=flat"> <img src="https://img.shields.io/badge/-Sass-CC6699.svg?logo=sass&style=flat"> <img src="https://img.shields.io/badge/-PostgreSQL-336791.svg?logo=postgresql&style=flat"> <img src="https://img.shields.io/badge/-Docker-EEE.svg?logo=docker&style=flat"> <img src="https://img.shields.io/badge/-Heroku-430098.svg?logo=heroku&style=flat"> <img src="https://img.shields.io/badge/-CircleCI-343434.svg?logo=circleci&style=flat">

# [Atom](https://atom-production.herokuapp.com/)

Technique/Version:

local

- docker==20.10.0
- docker-compose==1.25.5
- python==3.7.10
- pip==20.2.1
- django==3.0.14
- node==12.16.2
- npm==6.14.4
- yarn==1.22.4
- react==17.0.1
- axios==0.21.1
- bootstrap(cdn)==4.5.0
- scss
- sass compiler(vscode plugin)
- minifer(vscode plugin)
- gcp
- circleci==0.2.1

unique to production

- heroku==7.50.0
- postgresql==13.2
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

- [ ] Change inner files/directories' path from app/_ to BASE_DIR/_.

- [ ] Install npm.

```
$ docker-compose run --rm react npm install
```

- [ ] Run node.js server.

```
$ docker-compose run --rm --service-ports react npm start
```

- [ ] Then, type "localhost:3000" at search screen, you can see the content of /src/App.js !

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

- [ ] To check log,

```
$ heroku logs --tail
```

- [ ] To connect with database at heroku from local,

```
$ heroku pg:psql
```

- [ ] To enter files at heroku,

```
$ heroku run bash
```

### How to set environment variables at Heroku?

https://developer.yukimonkey.com/article/20200423/

- [ ] To register environment variables,

```
$ heroku config:set hoge="hogehoge"
```

- [ ] If you want to confirm,

```
$ heroku config
```

## How to deploy Django × React at Heroku?

https://dev.to/mdrhmn/deploying-react-django-app-using-heroku-2gfa

- [ ] Install Axios.

```
$ docker-compose run --rm react sh -c "npm i -g axios"
```

- [ ] add proxy at package.json like, "proxy": "http://localhost:8000".
- [ ] add some code at /src/App.js in order to get CSRF token by Axios.

```
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
```

- [ ] Then, enable Procfile at Heroku GUI.

[NOTE for myself]
To clear sessions,

```
python manage.py clearsessions
```
