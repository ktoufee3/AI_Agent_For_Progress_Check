#create database
import config
import psycopg2

conn = psycopg2.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_password, dbname="postgres")
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE DATABASE sms_progress_checker OWNER {};".format(config.db_user))
cur.close()
conn.close()
print("Database sms_progress_checker created.")