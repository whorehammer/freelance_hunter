from config_app import DbConfig
from my_exceptions import AdminAccessException
import psycopg2


class DbInterface(DbConfig):
    def create_default_table(self, cursor):
        try:
            query = "CREATE TABLE IF NOT EXISTS {table}(" \
                    "{identifier} serial primary key," \
                    "{group_name} char(64)," \
                    "{message} char(256))".format(table=self.destination_table,
                                                  identifier=self.identifier,
                                                  group_name=self.group_name,
                                                  message=self.message)
            cursor.execute(query)
        except Exception as e:
            print(e)

    def get_groups(self, cursor):
        query = "SELECT {group_name} FROM {table}".format(group_name=self.group_name,
                                                          table=self.destination_table)
        cursor.execute(query)
        return cursor.fetchall()

    def get_message(self, cursor):
        query = "SELECT {message} FROM {table} ORDER BY {identifier} DESC".format(message=self.message, table=self.destination_table,
                                                                                  identifier=self.identifier)
        cursor.execute(query)
        return cursor.fetchall()[0][0].strip()

    def set_message(self, cursor, message):
        query = "INSERT INTO {table}({message}) VALUES (%s)".format(table=self.destination_table,
                                                                    message=self.message)
        try:
            cursor.execute(query, (message, ))
        except Exception as e:
            print(e)


class AdminInteraction:
    def __init__(self, owner_list):
        self.__owner_list = owner_list

    def set_message_to_db(self, userid, message):
        if userid in self.__owner_list:
            DATABASE_URL = DbConfig.DATABASE_URL
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn.autocommit = True
            cursor = conn.cursor()
            db_int = DbInterface()
            try:
                db_int.set_message(cursor=cursor, message=message)
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
        else:
            raise AdminAccessException("нет прав на выполнение данного действия")

    def get_message_from_db(self, userid):
        if userid in self.__owner_list:
            DATABASE_URL = DbConfig.DATABASE_URL
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn.autocommit = True
            cursor = conn.cursor()
            db_int = DbInterface()
            try:
                response = db_int.get_message(cursor=cursor)
            except Exception as e:
                print(e)
                return
            finally:
                cursor.close()
                conn.close()
            return response
        else:
            raise AdminAccessException("нет прав на выполнение данного действия")
