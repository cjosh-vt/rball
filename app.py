from flask import Flask, request
import common_functions_rball
import traceback
import sys

app = Flask(__name__)

@app.route("/login",methods=['GET'])
def login():
    v_username=request.args.get('username')
    v_password=request.args.get('password')
    
    v_valid_login = 

def connect_to_postgres():
    return common_functions_rball.get_pg_connection('rball_app','vMBY8kU3E67Cz2ZC','127.0.0.1','nw_rball_app')

def get_connection_information(p_cursor,p_username, p_password):
    v_query = ("select player_id, username, password from rball_app.auth_login")
    try:
       p_cursor.execute(v_query)
       v_auth_info = p_cursor.fetchall()
    except:
       sys.exit("Unable to query database...investigate\n" + traceback.format_exc())

    return v_auth_info

if __name__ == '__main__':
    try:
       global v_cursor
       v_conn=connect_to_postgres()
       v_cursor=v_conn.cursor()
    except:
       sys.exit ("Whoops...you're still dumb...\n" + traceback.format_exc())

    app.run('0.0.0.0',port=80)
