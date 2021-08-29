import sys
import boto3
import os


API_KEY = ('PKFX5PGWS1QSUG9GT8VP')
API_URL = ('https://paper-api.alpaca.markets')
SECRET_KEY = ('Ojkf8iL3T4j2tOKGHfObZqVWbpUZ8W6Quog82Cpe')

DB_FILE = ('/Users/Kaleb/Documents/GitHub/auto_trade_app_kk/app.db')



ENDPOINT="ls-0ac799628b5dad6ae5fff0c755e9025170d01b85.clyjtmyhlt3z.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="dbmasteruser"
REGION="us-east-1"

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='RDSCreds')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)                    
                