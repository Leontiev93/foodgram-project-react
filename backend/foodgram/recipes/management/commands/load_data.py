import os
from dotenv import load_dotenv
import psycopg2
import csv

from django.core.management.base import BaseCommand

load_dotenv()

HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')


class Command(BaseCommand):
    help = 'Import CSV from data file'

    def handle(self, *args, **options):
        conn = psycopg2.connect(
            f"host={HOST} port={PORT} dbname={DB_NAME}"
            f" user={USER} password={PASSWORD}")
        cur = conn.cursor()
        temp = []
#        with open(
#                   r'Z:\Dev\foodgram-project-react\data\ingredients.csv',
#                   encoding='UTF-8', mode='r') as f:
        with open(
            r'/home/german/Dev/foodgram-project-react/data/ingredients.csv',
             encoding='UTF-8', mode='r') as f:

            new = csv.reader(f, delimiter=',', )
            for r in new:
                temp.append(r)
        cur.executemany(
            "INSERT INTO recipes_ingredient"
            "(name, measurement_unit) VALUES (%s, %s)", temp)
        conn.commit()
        print('Данные закгруженны, коммит выполнен')
        conn.close()
