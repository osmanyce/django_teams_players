# Python-Django project

Project created with Python-Django and SQLite3, with the help of the Pycharm IDE. It is a REST API that includes two CRUDs to two related entities (Teams and Players).

### Deployment:

  1. Clone repository
     
    git clone https://github.com/osmanyce/django_teams_players.git

  2. Move to project dir
     
    cd django_teams_players

  3. Create virtual environment and install python requirements
            
    - Create new folder outside project: dtp_venv
    - Configure Interpreter Settings in PyCharm
    - Add a new virtual enviroment with python3 as Base Interpreter in dtp_venv folder
    - Open django_teams_players/requirements.txt and install requirements. Or you can use pip for all requeriments

    Note: If you are not using Pycharm, you can use the following commands to create the virtual environment.
    - virtualenv dtp_venv
    - cd dtp_venv/bin
    - source activate
    - Execute "pip3 install" for each of the requirements

  4. Make migrations
     
    python3 manage.py makemigrations

  5. Migrate
     
    python3 manage.py migrate

  6. Create super user
     
    python3 manage.py createsuperuser

  7. Run project
  
  8. Load initial data (teams and players)
  
    python3 manage.py loaddata teams_players_initial_data.json

  9. Postman Collection:

    In the root of the project find the file: Tournament apis.postman_collection.json    
    You can import it on Postman to have acceso to all rest apis