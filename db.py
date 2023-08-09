import mysql.connector,json,sys

class DBhelper:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user="root",
                password="root",
                port=3306,
                database="ainova"
            )
            self.mycursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print("Error connecting to database:", str(e))
            sys.exit(0)
        else:
            print("Connected to Database")

    def search_db(self,cluster_num):
        # Specify the table name and column name
        table_name = "table_"+str(cluster_num)
        column_name = 'link'

        # Execute the query to retrieve random entries
        self.mycursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        total_rows = self.mycursor.fetchone()[0]

        if int(total_rows) > 5:
            query = f"SELECT {column_name} FROM {table_name} ORDER BY RAND() LIMIT 5"
            self.mycursor.execute(query)
            # Fetch the selected entries
            entries = self.mycursor.fetchall()

            # Convert the entries to JSON format
            entries_json = json.dumps(entries)
            return entries_json
        elif int(total_rows) <= 5:
            query = f"SELECT {column_name} FROM {table_name}"
            self.mycursor.execute(query)
            # Fetch the selected entries
            entries = self.mycursor.fetchall()

            # Convert the entries to JSON format
            entries_json = json.dumps(entries)
            return entries_json
        else:
            return {"Respose": "No links found"}

    def create_table(self,links, cluster_num):
        table_name = "table_" + str(cluster_num)
        create_table_query = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, link TEXT);"
        self.mycursor.execute(create_table_query)
        # Insert the links into the table
        insert_query = f"INSERT INTO {table_name} (link) VALUES (%s)"
        values = [(link,) for link in links]
        self.mycursor.executemany(insert_query, values)

        # Commit the changes and close the cursor
        self.conn.commit()

    def delete_table(self, cluster_num):
        table_name = "table_"+str(cluster_num)
        delete_table_query = f"DROP TABLE IF EXISTS {table_name}"
        self.mycursor.execute(delete_table_query)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


a = DBhelper()
