# Monolith로 Nginx, Gunicorn, MySql, Django 배포 (Ubuntu)

## 패키지 및 라이브러리 설치 

1. nginx, python3, mysqlclient, virtualvenv 등 다운로드


```bash
sudo apt-get update
sudo apt-get install nginx mysql-server python3-pip python3-dev libmysqlclient-dev ufw virtualenv
sudo apt install python3-venv
```

2. django 파일에서 python3으로 가상환경 만들고 활성화
가상환경이름: myvenv

```bash
sudo mkdir django
cd django
python3 -m venv myvenv
source myvenv/bin/activate
```

3. 필요한 라이브러리 pip install

```bash
(myvenv) cd ~/django/ebook
(myvenv) pip install -r requirements.txt
(myvenv) pip install mysqlclient django gunicorn
```


## 방화벽
- 활성화 하여 port open하거나 disable시킨다.


## MySql 데이터베이스 세팅

1. mysql 설치 후 root로 로그인
``` bash
sudo mysql_secure_installation
sudo mysql -u root -p

```

2. DB 생성
- 한글 사용한다면 CHARACTER SET utf8 COLLATE utf8_general_ci 설정할 것
- 접속 ID : BALI
- 접속 PW : EBOOKSERVER4
- DB 이름: EBOOK
```
CREATE DATABASE EBOOK DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE USER BALI;
GRANT ALL ON EBOOK.* TO 'BALI'@'%' IDENTIFIED BY 'EBOOKSERVER4';
FLUSH PRIVILEGES;
QUIT
```

## Django Skeleton 참고
```
\home\lab18\django\Ebook\
│
├── myvenv      # 가상환경
│
└── Ebook
    │
    ├── requirements.txt      # 필요 패키지
    ├── manage.py
    ├── media     # 유저가 업로드 한 파일
    ├── static
    │    │
    │    ├── user_app
    │    ├── book_app
    │    ├── book_rank_app
    │    ├── map_app
    │    └── trend_book_app     # HTML에 연결되는 개발 리소스
    │        │
    │        ├── slide.js
    │        ├── mypic.jpg
    │        └── styles.css ...
    │
    ├── templates     #  공용 html
    │    │
    │    ├── index.html
    │    └── base-layout.html
    │
    ├── user_app     # 개별 앱 (Feature)
    ├── book_app
    ├── book_rank_app
    ├── map_app
    ├── trend_book_app
    │    │
    │    ├── templates
    │    │    |
    │    │    └── trend_book_app
    │    │        |
    │    │        └── trend-book.html      # 개별 앱의 HTML 파일
    │    │
    │    ├── __init__.py
    │    ├── apps.py
    │    ├── models.py
    │    ├── urls.py
    │    └── views.py
    │
    └── Ebook
        │
        ├── __init__.py
        ├── urls.py
        ├── settings.py
        └── wsgi.py
```

## Django settings.py에 데이터베이스 설정

``` python

```