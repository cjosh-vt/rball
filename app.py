from flask import Flask, request, jsonify
import common_functions_rball
import traceback
import sys
import psycopg2


# Define all application endpoints beginning Here
app = Flask(__name__)

@app.route("/login",methods=['GET'])
def login():
    try:
       v_username=request.args.get('username')
       v_password=request.args.get('password')
    except:
       print ("You didn't pass the right values to login")

    if v_username and v_password:
       v_player_id = get_authentication(g_cursor, v_username, v_password)
    else:
       v_player_id = -1
    
    if v_player_id == -1 and v_username and v_password:
        return jsonify(player_id="PLAYER NOT FOUND")
    elif v_player_id == -1:
        return jsonify(player_id="INCORRECTLY FORMED GET QUERY to login")
    else:
        return jsonify(player_id=v_player_id)
        
@app.route("/playerInfo",methods=['GET'])
def playerInfo():
    try:
       v_player_id=request.args.get('playerID')
    except:
       print ("You didn't pass the right values to playerInfo")

    if v_player_id:
       v_player_info = get_player_info(g_cursor, v_player_id)
    else:
       v_player_info = -1
    
    if v_player_info == -1:
       return jsonify(v_player_info="INCORRECTLY FORMED GET QUERY TO playerInfo")
    else:
       return v_player_info

#This is the end of all application endpoints.  Below here are the functions related to the database
#which are USED by the application endpoints.

def connect_to_postgres(p_username,p_password):
    return common_functions_rball.get_pg_connection(p_username,p_password,'127.0.0.1','nw_rball_app')

def execute_a_query(p_connection, p_query):
    v_cursor = p_connection.cursor()
    
    try:
       v_cursor.execute(p_query)
       v_query_result=v_cursor.fetchall()
    except psycopg2.errors.SyntaxError:
       p_connection.rollback()
    except psycopg2.errors.InsufficientPrivilege:
       p_connection.rollback()
    except psycopg2.errors.UndefinedTable:
       p_connection.rollback()
    except:
       print ("Failed to execute query:  \n" + p_query + "\n" + traceback.format_exc())
    else:
       return v_query_result

def get_player_info(p_connection,p_player_id):
    v_query = ("select player_first_name, player_last_name, player_phone, player_email, season_description, skill_description, is_administrator from rball_app.player_info where player_id = " + str(p_player_id))
    try:
       v_player_info = execute_a_query(v_query)
    except:
       print ("Unable to query player information...investigate\n" + traceback.format_exc())
    else:
       if v_player_info is not None:
          return jsonify(player_first_name=v_player_info[0][0],
             player_last_name=v_player_info[0][1],
             player_phone=v_player_info[0][2],
             player_email=v_player_info[0][3],
             season_description=v_player_info[0][4],
             skill_description=v_player_info[0][5],
             is_administrator=v_player_info[0][6])
       else:
          return -1

def get_authentication(p_connection,p_username, p_password):
    v_query = ("select player_id from rball_app.auth_login where username = '" + p_username + "' and password = '" + p_password + "'")
    try:
       v_auth_info = execute_a_query(v_query)
    except:
       print("Unable to query database...investigate\n" + traceback.format_exc())
 
    if len(v_auth_info) > 0:
       return v_auth_info[0][0]
    else:
       return -1

def get_connection(p_username,p_password):
    try:
       v_conn=connect_to_postgres(p_username,p_password)
       v_conn.autocommit=False
    except:
       print ("Whoops...you're still dumb...\n" + traceback.format_exc())
       
def get_credentials():
    try:
       parameter_file=open("../parameters/parameters.txt","r")
    except:
       print ("ERROR:  Unable to open parameter file.")
    else:
       v_creds=parameter_file.read()
       v_user,v_password=v_creds.split(":")
       return v_user,v_password

#Main is invoked when the application is started on the server.
if __name__ == '__main__':

    v_usersname,v_password=get_credentials()

    #We start by connecting to the postgres database
    get_connection(v_username,v_password)
    
    #Begin running the application listener
    app.run('0.0.0.0',port=80)
