import argparse
import json
import ast
from gaipy import Create

parser = argparse.ArgumentParser(description='Gais DB Create Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-c', '--create-arg', dest='create_arg', type=str)
parser.add_argument('-w', '--weighted-col',
                    dest='weighted_arg', type=str, default='[]')

args = parser.parse_args()

res_db = args.database
res_create_arg = json.loads(args.create_arg)
res_weighted_arg = ast.literal_eval(args.weighted_arg)

status = Create(res_db, res_create_arg, res_weighted_arg)

print(status)
