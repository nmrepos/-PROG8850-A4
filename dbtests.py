import mysql.connector
import pytest

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'database': 'subscribers',
}


def _get_columns(cursor, table):
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    return {row[0]: row[1] for row in cursor.fetchall()}


def test_subscriber_table_has_email_and_date():
    cnx = mysql.connector.connect(**DB_CONFIG)
    cur = cnx.cursor()
    cols = _get_columns(cur, 'subscriber')
    assert 'email' in cols, 'email column missing'
    assert 'subscription_date' in cols, 'subscription_date column missing'
    cur.close()
    cnx.close()

