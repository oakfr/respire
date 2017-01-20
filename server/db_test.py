import MySQLdb

print ('hey there')

# Open database connection
db = MySQLdb.connect("localhost","phpmyadmin","respirea","respire" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
#cursor.execute("SELECT VERSION()")
cursor.execute("SELECT * FROM sensors WHERE 1")

# Fetch a single row using fetchone() method.
results = cursor.fetchall()

for row in results:
    print (row)

# disconnect from server
db.close()
