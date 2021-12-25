import snowflake.connector
from config import username as uname, password as pword, account as acc

class getConnection:
    def makeconnection(self):
        conn = snowflake.connector.connect(
            user=uname,
            password=pword,
            account=acc,
            warehouse='COMPUTE_WH',
            schema='PUBLIC',
            database='MYNEWDB')
        return conn