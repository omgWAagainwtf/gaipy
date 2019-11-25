import requests
import json


type_d = {
        "num": "-numfieldindex",
        "date": "-dateindex",
        "text": "text",
        "weighted_column": "-title",
        "time": "-timeindex",
    }
domain = 'http://gais.ccu.edu.tw:5801/nudb/'


def __return(res=True, msg='', data={}):

    info = {
        'res': res,
        'msg': msg,
        'data': data
    }

    return json.dumps(info)


def __parse_to_gaisrec(key):

    key = key.lstrip('@').rstrip(':')

    return '@' + key + ':'


def __parse_column_args(args_dict):

    rec = {}
    for k in args_dict:
        rec[__parse_to_gaisrec(k)] = args_dict[k]
    d = {}
    for k in rec:
        if rec[k] not in d:
            d[rec[k]] = [k]
        else:
            d[rec[k]].append(k)
    if '-fieldindex' not in d:
        d['-fieldindex'] = d['text']
    d['-fieldindex'] = d['text']
    s = ''
    for k in d:
        if k == 'text':
            s += '-indexfield ' + '"' + ','.join(d[k]) + '" '
        elif k == '-fieldindex':
            s += '-fieldindex ' + '"' + ','.join(d[k]) + '" '
        else:
            s += type_d[k] + ' "' + ','.join(d[k]) + '" '

    return s.rstrip(' ')


def __get_db_col(db):

    cmd = domain + 'getDBInfo?db=%s' % db
    response = requests.get(cmd)
    if response.status_code == requests.codes.ok:
        r = json.loads(response.text)
        if 'error' in r:
            raise Exception(r['error'])
        split_list = r['result']['create_arg'].split(' ')[2:]
        d = {}
        for i in range(0, len(split_list), 2):
            d[split_list[i]] = split_list[i+1][1:-1].split(',')
        fieldindex = d['-fieldindex'] if '-fieldindex' in d else []
        numfieldindex = d['-numfieldindex'] if '-numfieldindex' in d else []

        return fieldindex + numfieldindex


def __build_query(db, d):

    if not(len(d.keys()) == 2 and 'val' in d and 'col' in d):
        raise Exception('''dict syntax error: You should pass {'val':[],'col':[]} format dict''')
    if len(d['col']) != len(d['val']):
        raise Exception("Mismatch length of len(col)=%d and len(val)=%d" % (len(d['col']), len(d['val'])))

    col = __get_db_col(db)
    query_str = ''
    col_list = []
    for c in d['col']:
        if __parse_to_gaisrec(c) not in col:
            raise Exception("no such index %s in %s" % (c, db))
        else:
            col_list.append(__parse_to_gaisrec(c))
    for i in range(len(d['val'])):
        # for val in d['val'][i]:
        query_str += col_list[i] + d['val'][i] + ','

    return query_str.rstrip(',')
