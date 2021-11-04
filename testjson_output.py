import psycopg2
import preprocessing
import interface


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


conn = psycopg2.connect(
    host="localhost",
    database="TPC-H",
    user="postgres",
    password="password")

cur = conn.cursor()

def get_json():
    """ query parts from the parts table """
    conn = None
    try:
        params = preprocessing.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON)
select
	l_orderkey,
	o_orderdate,
	o_shippriority
from
	customer,
	orders,
	lineitem
where
	c_mktsegment = ':1'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey""")
        rows = cur.fetchall()
        print(json.dumps(rows))
       
        # for i in range(len(data)):
        #     my_str = data.replace("'","\"")
        #     print(my_str)
        # rows = cur.fetchall()
        # print("The number of parts: ", cur.rowcount)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

get_json()
    
# To close communication with Postgresql
cur.close() 
conn.close()