# Important!!
main branch is for heroku only. chatbot and llm module is to be ran locally in the frontend branch. \
requirements.txt is for Heroku to set up. \
dev-requirements.txt contains the requirements to run the streamlit app locally.

For this, download Ollama in https://ollama.com/ \
Then pull llama3.2 by inputing in your terminal: 

ollama pull llama3.2

The schema for the Heroku postgress DB is found in file: \
ETL/Load/create_schema.sql

# Team Members
Jorge L. Rivera González - jorge.rivera94@upr.edu

# Database Credentials
Heroku App Name: \
Database Name: \
Host: \
Port: \
User: \
Password: \
URL: 

# To run
* Ensure a databese exists with the schema given by ETL/Load/create_schema.sql
* Udate the references to this database in ETL/Load/load_to_heroku.py and llm/remote_clients.py and frontend/.streamlit/secrets.toml
* python ETL/Extract/extract.py
* python ETL/Transform/new_transform.py
* python ETL/Load/load_to_heroku.py
* python filehandler.py 

In a terminal A so the route /chat is active: \
python main.py 

In a terminal B to run the streamlit app: \
streamlit run .\frontend\01_Log_in.py
