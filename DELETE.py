import argparse
import ast
from gaipy import Del

parser = argparse.ArgumentParser(description='Gais DB Delete Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-i', '--record-id', dest='rid', type=int)


args = parser.parse_args()

res_db = args.database
res_record_id = ast.literal_eval(args.rid)

status = Del(res_db, res_record_id)

print(status)
