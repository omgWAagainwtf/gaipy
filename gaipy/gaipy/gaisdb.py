import requests
import json
from .basic import __return, __parse_column_args, __build_query,__parse_to_gaisrec

valid_format = {'text', 'json'}
valid_type = {'str', 'list', 'dict'}
match_mode = {'AndMatch', 'OrMatch', 'BestMatch'}
type_d = {"num":"-numfieldindex","date":"-dateindex","text":"text","weighted_column":"-title","time":"-timeindex"}
map_type = {v: k for k, v in type_d.items()}
domain = 'http://gais.ccu.edu.tw:5801/nudb/'

def Create(db, args_dict={},weighted_col=[]):
    if args_dict == {} :
        return __return(False, 'missing column argument')
    elif type(args_dict) is not dict :
        return __return(False, 'column argument must be dictionary type')
    elif type(weighted_col) is not list:
        return __return(False, 'weighted column argument must be list type')
    for wc in weighted_col:
        if wc not in args_dict:
            return __return(False, "No such column %s in your DB"%wc)
    wcs = ''
    if len(weighted_col) != 0:
        wcs = ','.join(__parse_to_gaisrec(str(i)) for i in weighted_col)
        wcs = "-title '" + wcs + "'"
    args = __parse_column_args(args_dict)    
    
    cmd = domain +'create?name=%s&arg=%s %s' % (db, args,wcs)
    response = requests.get(cmd)
    gaisdb_res =response.json()
    if response.status_code == requests.codes.ok:
        return __return(True, 'create %s successed' % db)
    else:
        return __return(False, gaisdb_res['error']['message'])

def Show(db):
    cmd = domain +'getDBInfo?db=%s' % db
    response = requests.get(cmd)
    if response.status_code == requests.codes.ok:
        r = json.loads(response.text)
        if 'error' in r:
            return __return(False, r['error'])

        l = r['result']['create_arg'].split(' ')[2:]
        d = {}
        f = '{type:<16}{column}'
        not_text = set()
        for i in range(0,len(l),2):
            d[l[i]] = l[i+1][1:-1].split(',')

        for k in d:
            if k != '-indexfield' and k != '-title' and k != '-fieldindex':
                not_text.update(d[k])
        
        d['text'] = list(set(d['-indexfield']) - not_text)
        print(f.format(type = 'type',column = 'column'))
        print("-"*80)
        for k in d:
            if k != '-indexfield' and k != '-fieldindex' and k != '-title':
                print(f.format(type = map_type[k],column = ', '.join(d[k])))
        print("-"*80)
        print(f.format(type = 'fieldindex',column = ', '.join(d['-fieldindex'])))

        return __return(True, 'show %s info successed' % db)
    else:
        return __return(False, 'fail to show %s info' % db)

def Drop(db):
    cmd = domain + 'delete?name=%s' % db
    response = requests.get(cmd)
    if response.status_code == requests.codes.ok:
        return __return(True, 'drop %s successed' % db)
    else:
        return __return(False, 'fail to drop %s' % db)

def Insert(db, record, record_format='text', rb=''):
    if type(record).__name__ not in valid_type :
        return __return(False, 'Invalid record type: record type must be str, dict or a list of dict')
    elif record_format not in valid_format :
        return __return(False, 'Invalid record format: format must be text or json')
    else :
        cmd = domain +'getDBInfo?db=%s' % db
        response = requests.get(cmd).json()
        if 'error' in response :
            return __return(False, response['error'])

        cmd = domain + 'rput?db=%s&record=%s&format=%s' % \
            (db, record, record_format)

        if rb != '' :
            cmd += '&recbeg=%s' % rb

        response = requests.get(cmd)
        gaisdb_res = response.json()
        if response.status_code == requests.codes.ok:
            return __return(True, 'insert successed', gaisdb_res['result'])
        else:
            return __return(False, gaisdb_res['error']['message'])

def Update(db, rid=0, new_record='', modify_all=False, record_format='text', getrec=False):
    if type(rid) != int or rid == 0 :
        return __return(False, 'Invalid rid: missing rid or wrong rid type')
    elif type(new_record).__name__ not in valid_type :
        return __return(False, 'Invalid record type: record type must be str, dict or a list of dict')
    elif record_format not in valid_format :
        return __return(False, 'Invalid record format: format must be text or json')
    else :
        cmd = domain +'getDBInfo?db=%s' % db
        response = requests.get(cmd).json()
        if 'error' in response :
            return __return(False, response['error'])

        cmd = domain + 'rupdate?db=%s&rid=%s&format=%s' % (db, rid, record_format)
        new_record.replace('"', '\"')

        if modify_all == False :
            cmd += '&field=%s' % new_record
        else :
            cmd += '&record=%s' % new_record

        if getrec == True :
            cmd += '&out=json&getrec=y'
        else :
            cmd += 'getrec=n'

        response = requests.get(cmd)
        gaisdb_res = response.json()
        if response.status_code == requests.codes.ok :
            return __return(True, 'update sucessed', gaisdb_res['result'])
        else :
            if gaisdb_res['error']['status'] == 400 :
                return __return(False, 'input new record does not match your record format')
            else :
                return __return(False, 'rid not found')

def Select(db, pattern={}, filter_args={}, mode='', page_cnt=10, page=1, order_by='', order='desc'):
    if page_cnt < 1 :
        return __return(False, 'page count must be more than 1')
    elif page < 1 :
        return __return(False, 'page must be more than 1')
    else :
        cmd = domain +'getDBInfo?db=%s' % db
        response = requests.get(cmd).json()
        if 'error' in response :
            return __return(False, response['error'])

        cmd = domain + 'query?db=%s&p=%s&ps=%s&out=json' % (db, page, page_cnt)
        
        if type(pattern) == dict and len(pattern) != 0 :
            cmd += '&q=%s' % __build_query(db, pattern)

        if mode in match_mode :
            cmd += '&matchmode=%s' % mode

        if order_by != '' :
            cmd += '&order_by=%s' % order_by

        if order == 'asc' :
            cmd += '&order=%s' % order

        if type(filter_args) == dict and len(filter_args) != 0 :
            cmd += '&filter=%s' % __build_query(db, filter_args)
        
        response = requests.get(cmd)
        gaisdb_res = response.json()
        if response.status_code == requests.codes.ok :
            return __return(True, 'complete search', gaisdb_res['result'])
        else :
            return __return(False, gaisdb_res['error'])

def Search(db, term_list='', filter_args={}, mode='', page_cnt=10, page=1, order_by='', order='desc'):
    if page_cnt < 1 :
        return __return(False, 'page count must be more than 1')
    elif page < 1 :
        return __return(False, 'page must be more than 1')
    else :
        cmd = domain +'getDBInfo?db=%s' % db
        response = requests.get(cmd).json()
        if 'error' in response :
            return __return(False, response['error'])

        cmd = domain + 'query?db=%s&q=%s&p=%s&ps=%s&out=json' % (db, term_list, page, page_cnt)
        
        if mode in match_mode :
            cmd += '&matchmode=%s' % mode

        if order_by != '' :
            cmd += '&order_by=%s' % order_by

        if order == 'asc' :
            cmd += '&order=%s' % order

        if type(filter_args) == dict and len(filter_args) != 0 :
            cmd += '&filter=%s' % __build_query(db, filter_args)

        response = requests.get(cmd)
        gaisdb_res = response.json()
        if response.status_code == requests.codes.ok :
            return __return(True, 'complete search', gaisdb_res['result'])
        else :
            return __return(False, gaisdb_res['error'])

def Del(DB, rid = []):
    url = 'http://gais.ccu.edu.tw:5801/nudb/rdel'
    if type(rid) != list:
        return __return(False, 'Type Error!, Please pass list of rid.')
    rids = ','.join(str(i) for i in rid)
    argData = {'db':DB,'rid': rids}
    res = requests.post(url,data=argData)
    resjson = res.json()
    if res.status_code == requests.codes.ok:
        return __return(True, 'deleted')
    else:
        return __return(True, 'No such record in DB %s'%DB, resjson['error'])
