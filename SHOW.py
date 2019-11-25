import argparse
from gaipy import Show 

parser = argparse.ArgumentParser(description='Gais DB Show Tools')
parser.add_argument('-d', '--database', dest='database', type=str)

args = parser.parse_args()

res_db = args.database

result = Show(res_db)

print(result)