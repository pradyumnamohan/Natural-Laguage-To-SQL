import sqlite3

connection = sqlite3.connect('emp.db')
cursor = connection.cursor()

table_info = """
CREATE TABLE IF NOT EXISTS employee (
    EMP_NAME varchar(50),
    EMP_ID varchar(50),
    DESIGNATION varchar(50),
    EMP_AGE int);
"""
cursor.execute(table_info)

cursor.execute("""Insert into employee values ('John Doe', 'E123', 'Software Engineer', 30)""")
cursor.execute("""Insert into employee values ('Jane Smith', 'E124', 'Data Scientist', 28)""")
cursor.execute("""Insert into employee values ('Alice Johnson', 'E125', 'Project Manager', 35)""")
cursor.execute("""Insert into employee values ('Bob Brown', 'E126', 'UX Designer', 27)""")
cursor.execute("""Insert into employee values ('Charlie Black', 'E127', 'DevOps Engineer', 32)""")
cursor.execute("""Insert into employee values ('Diana White', 'E128', 'QA Engineer', 29)""")

print("The inserted data is:")
data = cursor.execute("""SELECT * FROM employee""")
for row in data:
    print(row)

connection.commit()
connection.close()
