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
       v_player_id = get_authentication(g_conn, v_username, v_password)
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
       v_player_info = get_player_info(g_conn, v_player_id)
    else:
       v_player_info = -1

    if v_player_info == -1:
       return jsonify(v_player_info="INCORRECTLY FORMED GET QUERY TO playerInfo")
    else:
       return v_player_info

@app.route("/nextMatch",methods=['GET'])
def nextMatch():
    try:
        v_player_id=request.args.get('playerID')
    except:
        print ("You didn't pass the right values to nextMatch")

    if v_player_id:
        v_match_info = get_next_match(g_conn,v_player_id)
    else:
        v_match_info = -1

    if v_match_info == -1:
       return jsonify(v_player_info="INCORRECTLY FORMED GET QUERY TO playerInfo")
    else:
       return v_match_info

#This is the end of all application endpoints.  Below here are the functions related to the database
#which are USED by the application endpoints.

def connect_to_postgres(p_username,p_password):
    """
       This module gets a connection to the postgres database being used for the App.
       @param p_username
          - The username to use to connect to the database
       @param p_password
          - The password to use to connect to the nw_rball_app database.
    """
    return common_functions_rball.get_pg_connection(p_username,p_password,'127.0.0.1','nw_rball_app')

def execute_a_query(p_connection, p_query):
    """
       This module executes any query it is passed using the connection it's passed and returns the
       results to the calling functino.
       @param p_connection
          - A global connection variable used for the cursor connection to execute the query.
       @param p_query
          - The query to be executed.
    """
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

def get_next_match(p_connection,p_player_id):
    """
       This module creates a query which it then executes to get the next match for
       a given player ID.
       @param get_pg_connection
          - The global connection object to be used in querying the database.
       @param p_player_id
          - The ID of the player to query for.
    """
    v_query = ("select court_description, game_time from next_match_vw where player_id = " + str(p_player_id))
    try:
        v_next_match = execute_a_query(p_connection,v_query)
    except:
        print ("Unable to query mext match information...investigate\n" + traceback.format_exc())
    else:
        if v_next_match is not None:
            return jsonify(next_match_court=v_next_match[0][0],
            next_match_game_time=v_next_match[0][1])
        else:
            return -1

def get_player_info(p_connection,p_player_id):
    """
       This module creates a query which it then executes and returns results for.
       @param p_connection
          - The global connectino object to be used in querying the database
       @param p_player_id
          - The player ID you're requesting information on.
    """
    v_query = ("select player_first_name, player_last_name, player_phone, player_email, season_description, skill_description, is_administrator from rball_app.player_info_vw where player_id = " + str(p_player_id))
    try:
       v_player_info = execute_a_query(p_connection,v_query)
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
    """
       This module determines if the requested userID and password are present in the database.
       @param p_connection
          - The conneciton object to be used in querying the database.
       @param p_username
          - The username the app is trying to log in as.
       @param p_password
          - The password the app is trying to use to log in.
    """
    v_query = ("select player_id from rball_app.auth_login_vw where username = '" + p_username + "' and password = '" + p_password + "'")
    try:
       v_auth_info = execute_a_query(p_connection,v_query)
    except:
       print("Unable to query database...investigate\n" + traceback.format_exc())

    if len(v_auth_info) > 0:
       return v_auth_info[0][0]
    else:
       return -1

def get_connection(p_username,p_password):
    """
       The module is called to establish a connection to the database for use in query execution.
       @param p_username
          - The username to use when logging into the database
       @param p_password
          - The password to use to authenticate against the database.
    """
    try:
       global g_conn
       g_conn=connect_to_postgres(p_username,p_password)
       g_conn.autocommit=False
    except:
       print ("Whoops...you're still dumb...\n" + traceback.format_exc())

def get_credentials():
    """
       This module will read a parameter file and get the username and password, which are presumed, currently,
       to be the only entries.
       @return v_user
          - The username to use for authentication against the database
       @return v_password
          - The password to use for authentication against the password
    """
    try:
       parameter_file=open("../parameters/parameters.txt","r")
    except:
       print ("ERROR:  Unable to open parameter file.")
    else:
       v_creds=parameter_file.read()
       v_user,v_password=v_creds.split(":")
       return v_user,v_password.rstrip("\n")

#Main is invoked when the application is started on the server.
if __name__ == '__main__':

    #We start by connecting to the postgres database
    v_username,v_password=get_credentials()
    get_connection(v_username,v_password)

    #Begin running the application listener
    app.run('0.0.0.0',port=80)
