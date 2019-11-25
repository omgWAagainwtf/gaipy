import argparse
from gaipy import Drop 

parser = argparse.ArgumentParser(description='Gais DB Drop Tools')
parser.add_argument('-d', '--database', dest='database', type=str)

args = parser.parse_args()

res_db = args.database

status = Drop(res_db)

print(status)