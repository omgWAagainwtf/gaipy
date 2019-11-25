import argparse
import json
from gaipy import Del

parser = argparse.ArgumentParser(description='Gais DB Delete Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-i', '--record-id', dest='rid', type=str)


args = parser.parse_args()

res_db = args.database
res_record_id = json.loads(args.rid)
print(res_record_id)
status = Del(res_db, res_record_id)

print(status)
