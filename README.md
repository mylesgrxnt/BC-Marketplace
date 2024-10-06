# Example App

## Starting Virtual Environment
```
python -m venv flask_environment
source f
```

## Installing Dependencies
```
pip install flask flask-sqlalchemy flask-login python-dotenv flask-wtf flask_optional_routes
```
or
```
pip install -r requirements.txt
```

## Running Application
create .env
```
FLASK_APP=project
FLASK_DEBUG=1
```
run app
```
flask run
```