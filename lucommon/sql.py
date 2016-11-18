"""
Do the raw SQL injection execution
"""

import re

from django.db import connections

from lucommon.logger import lu_logger
from lucommon.exception import (
    LuSQLNotAllowError,
    LuSQLSyntaxError,
)


class LuSQL(object):
    """
    Raw SQL Interface, efficient for multiple table SQL
    """
    def __init__(self, db, sql, sql_param=[], allow_sql=['SELECT'], map_sql={},
                       search_condition='', conf_sql={}):
        self._db = db
        self._sql = sql
        self._sql_param = sql_param
        self.__filter_sql(allow_sql, map_sql, search_condition, conf_sql)
        self._conn = connections[self._db]
        self._cursor = self._conn.cursor()

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.commit()
        except Exception, err:
            lu_logger.error(str(err))

    def execute(self):
        """
        Raw SQL execution
        """
        try:
            if self._sql_param:
                self._cursor.execute(self._sql, self._sql_param)
            else:
                self._cursor.execute(self._sql)
        except Exception, err:
            raise LuSQLSyntaxError(str(err))

        if not self._sql.upper().startswith('SELECT'):
            return []

        fetchall = self._cursor.fetchall()

        col_names = [desc[0] for desc in self._cursor.description]

        data = []

        for row in fetchall:
            dic = {}

            for index, value in enumerate(row):
                dic[col_names[index]] = value

            data.append(dic)

        return data

    def __convert_sql(self, search_condition, conf_sql):
        """
        SQL runtime replacement and convertion
        """
        self._sql = self._sql.replace('LU_SEARCH_CONDITION', search_condition)

        if search_condition:
            #TODO: smart analyzer and replacement
            for key, value in conf_sql.items():
                self._sql = self._sql.replace(key, value[0])

    def __filter_sql(self, allow_sql, map_sql, search_condition, conf_sql):
        """
        SQL filter is a security policy from lucommon,
        Allow and Deny policy here

        Usually, lucommon will do the sql map firstly,
        then do sql allow check.
        """
        # Do the sql mapping
        self._sql = map_sql.get(self._sql, self._sql)

        # Do the replacement and convertion
        # This will be specially important to lucommon SQL injection powerful
        self.__convert_sql(search_condition, conf_sql)

        # Do the sql filtering
        for sql in allow_sql:
            patten = re.compile(sql, re.IGNORECASE)
            if patten.match(self._sql.strip()):
                return

        raise LuSQLNotAllowError('LU SQL injection only support for: %s' % str(allow_sql))


