# Important!!
main branch is for heroku only. chatbot and llm module is to be ran locally in the frontend branch. \
requirements.txt is for Heroku to set up. \
dev-requirements.txt contains the requirements to run the streamlit app locally.

For this, download Ollama in https://ollama.com/ \
Then pull llama3.2 by inputing in your terminal: \

ollama pull llama3.2

The schema for the Heroku postgress DB is found in file: \
ETL/Load/create_schema.sql

# Team Members
Jorge L. Rivera González - jorge.rivera94@upr.edu

# Database Credentials
Heroku App Name: db-ciic4060-team-fulcrum\
Database Name: DATABASE\
Host: c57oa7dm3pc281.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com \
Port: 5432 \
User: u7ve47tk2bll2p \
Password: pf62c4799770f5b46bb61127026d2ffb543bf759a1221e6f9cb86b2dc0dde73b2 \
URL: postgres://u7ve47tk2bll2p:pf62c4799770f5b46bb61127026d2ffb543bf759a1221e6f9cb86b2dc0dde73b2@c57oa7dm3pc281.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfcsar0vfdptop

# To run
python filehandler.py \

In a terminal A so the route /chat is active: \
python main.py \

In a terminal B to run the streamlit app: \
streamlit run .\frontend\01_Log_in.py
