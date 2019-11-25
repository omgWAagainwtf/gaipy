import argparse
import json
import ast
from gaipy import Insert

parser = argparse.ArgumentParser(description='Gais DB Insert Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-r', '--record-arg', dest='record_arg', type=str)

args = parser.parse_args()

res_db = args.database
res_record_arg = args.record_arg

status = Insert(res_db, res_record_arg, 'json')

print(status)
