# gets json file from sql output 

import json
import sqlparse 

# read json file 
def read_json(plan_path): 
    # plan_path = str(input("Query Plan (in JSON) path: "))

    plan_file = open(plan_path, 'r')
    plan_json = json.loads(plan_file.read())

    return plan_json


def read_query(query_path): 
    # query_path = str(input("SQL query path: "))

    query_file = open(query_path, 'r')
    query_text = query_file.read()

    query_string = query_text.replace('\n', ' ')
    query_formatted = sqlparse.format(query_string, reindent=True, keyword_case='upper')
    # print(query_formatted)

    return query_formatted