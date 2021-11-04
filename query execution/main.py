from create_tree import *
from read_sql import * 

def main(): 
    query_path = './samplebig.json'
    # query_path = str(input("Query path: "))
    query_text = read_query(query_path)

    plan_path = './samplebig_q.sql'
    # plan_path = str(input("Plan path: "))
    plan_json = read_json(plan_path)

    root = build_tree(plan_json[0]["Plan"])[0]

    print(RenderTree(root))

    match_dict = build_relation(query_text, root)
    print(match_dict)

main()