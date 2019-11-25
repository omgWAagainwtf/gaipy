import argparse
import json
import ast
from gaipy import Update

parser = argparse.ArgumentParser(description='Gais DB Update Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-i', '--record-id', dest='rid', type=int)
parser.add_argument('-r', '--record-arg', dest='record_arg', type=str)
parser.add_argument('-m', '--modify-all', dest='modify_all', type=bool)
parser.add_argument('-g', '--get-rec', dest='get_record', type=bool)

args = parser.parse_args()

res_db = args.database
res_rid = args.rid
res_record_arg = args.record_arg
res_modify_all = args.modify_all
res_get_rec = args.get_record

if res_modify_all == True:
    status = Update(res_db, res_rid, res_record_arg,
                    res_modify_all, 'json', res_get_rec)
else:
    status = Update(res_db, res_rid, res_record_arg,
                    res_modify_all, 'json', res_get_rec)

print(status)
