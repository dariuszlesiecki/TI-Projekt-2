import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


DB_URL = "postgres://jsjoeakm:q9n27mL92Hdfd0gCwoFHEp18TwRYUXTW@kandula.db.elephantsql.com:5432/jsjoeakm"

def execute_fetchall(what):
    try:
        conn = psycopg2.connect(DB_URL)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(f"{what};")
                records = cursor.fetchall()
        return records
    except (Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        conn.close()
        print("conn closed")

def execute_fetchone(what):
    try:
        conn = psycopg2.connect(DB_URL)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(f"{what};")
                records = cursor.fetchone()
        return records
    except (Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        conn.close()
        print("conn closed")

def insert(what):
    try:
        conn = psycopg2.connect(DB_URL)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(f"{what};")
    except (Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        conn.close()
        print("conn closed")