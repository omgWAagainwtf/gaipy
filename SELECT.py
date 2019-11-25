import argparse
import json
import ast
from gaipy import Select

parser = argparse.ArgumentParser(description='Gais DB Select Tools')
parser.add_argument('-d', '--database', dest='database', type=str)
parser.add_argument('-pat', '--pattern', dest='pattern', type=str)
parser.add_argument('-f', '--filter-args',
                    dest='filter_args', type=str, default='{"col": [], "val": []}')
parser.add_argument('-fm', '--filter-mode',
                    dest='filter_mode', type=str, default='AndMatch')
parser.add_argument('-pc', '--page-count',
                    dest='page_count', type=int, default=10)
parser.add_argument('-pn', '--page-number',
                    dest='page_number', type=int, default=1)
parser.add_argument('-ob', '--order-by', dest='order_by',
                    type=str, default='rid')
parser.add_argument('-oa', '--order-attr',
                    dest='order_attr', type=str, default='desc')


args = parser.parse_args()

res_db = args.database
res_pattern = ast.literal_eval(args.pattern)
res_filter_args = ast.literal_eval(args.filter_args)
res_filter_mode = args.filter_mode
res_page_count = args.page_count
res_page_number = args.page_number
res_order_by = args.order_by
res_order_attr = args.order_attr

result = Select(res_db, res_pattern, res_filter_args,
                res_filter_mode, res_page_count, res_page_number, res_order_by, res_order_attr)

print(result)
