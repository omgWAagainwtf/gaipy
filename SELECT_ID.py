import argparse
import json
import ast
from gaipy import QueryRid

parser = argparse.ArgumentParser(description='Gais DB Select RID Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-i', '--record-id', dest='rid', type=str)


args = parser.parse_args()

res_db = args.database
res_record_id = json.loads(args.rid)
result = QueryRid(res_db, res_record_id)

print(result)
