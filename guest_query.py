#!/usr/bin/python3

import argparse
import time
import pymysql.cursors

class DatabaseQuery:
    def __init__(self, user, password, db, host='localhost'):
        self._user = user
        self._password = password
        self._db = db
        self._host = host

    def __query_db(self):
        connection = pymysql.connect(host=self._host,
                                     user=self._user,
                                     password=self._password,
                                     db=self._db,
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                _query = "SELECT Email,(Sessions.LastActivityAt/1000) AS LastActivityAt FROM Users \
                         JOIN Sessions on Sessions.UserId=Users.ID WHERE Users.Roles='system_guest';"
                cursor.execute(_query)
                return cursor.fetchall()
        finally:
            connection.close()

    def __filter_dict(self, query_output, days):
        filtered = {}
        blacklist = []
        for dict in query_output:
            if dict['Email'] in filtered:
                if time.time() - float(dict['LastActivityAt']) < 86400 * days:
                    del filtered[dict['Email']]
                    blacklist.append(dict['Email'])
            else:
                if time.time() - float(dict['LastActivityAt']) >= 86400 * days and dict['Email'] not in blacklist:
                    filtered[dict['Email']] = float(dict['LastActivityAt'])
        return filtered

    def get_guests(self, days):
        guests = self.__filter_dict(self.__query_db(), days)
        return guests

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Get inactive users from Mysql database.")
    parser.add_argument("-d", "--days", help="days of inactivity", required=True, type=int)
    parser.add_argument("-u", "--username", help="username for database", required=True)
    parser.add_argument("-p", "--password", help="password for database", required=True)
    parser.add_argument("-D", "--database", help="database name", required=True)
    parser.add_argument("-H", "--host", help="database host (e.g. localhost, 127.0.0.1")
    args = parser.parse_args()

    if args.host:
        result = DatabaseQuery(args.username, args.password, args.database, args.host)
    else:
        result = DatabaseQuery(args.username, args.password, args.database)

    for key in result.get_guests(args.days):
        print(key)
