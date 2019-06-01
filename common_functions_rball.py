import psycopg2
import traceback

def get_pg_connection(p_username, p_password, p_host, p_database):
    try:
       v_conn=psycopg2.connect(user=p_username, password=p_password, host=p_host, port="5432", database=p_database)
    except:
       print ("ERROR:  Failed to connect...you did something wrong, Dummy \n" + str(traceback.format_exc()))
    else:
       print ("INFO:  Connection successful")
       return v_conn
