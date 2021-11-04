import psycopg2
import preprocessing

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
        cur.execute("""
                    EXPLAIN(ANALYZE, VERBOSE, FORMAT JSON)
                    SELECT  
                        l_returnflag,
                        l_linestatus,
                        sum(l_quantity) as sum_qty,
                        sum(l_extendedprice) as sum_base_price,
                        sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
                        sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
                        avg(l_quantity) as avg_qty,
                        avg(l_extendedprice) as avg_price,
                        avg(l_discount) as avg_disc,
                        count(*) as count_order
                    FROM
                        lineitem
                    WHERE
                        l_shipdate <= date '1998-12-01'
                    GROUP BY
                        l_returnflag,
                        l_linestatus
                    ORDER BY
                        l_returnflag,
                        l_linestatus;""")
        rows = cur.fetchall()
        print("The number of parts: ", cur.rowcount)
        for row in rows:
            print(row)
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