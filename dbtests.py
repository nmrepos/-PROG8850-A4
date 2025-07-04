import mysql.connector
import pytest
from datetime import datetime, timedelta

DB_CONFIG = {
    'host':     'localhost',
    'user':     'flyway',
    'password': 'flyway_pass_123',
    'database': 'subscribers',
}


def _get_columns(cursor, table):
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    return {row[0]: row[1] for row in cursor.fetchall()}


@pytest.fixture
def db_conn():
    cnx = mysql.connector.connect(**DB_CONFIG)
    yield cnx
    cnx.close()


def test_subscriber_table_has_email_and_date(db_conn):
    cur = db_conn.cursor()
    cols = _get_columns(cur, 'subscriber')
    assert 'email' in cols, 'email column missing'
    assert 'subscription_date' in cols, 'subscription_date column missing'
    cur.close()


def test_subscription_date_defaults_to_now(db_conn):
    cur = db_conn.cursor()
    test_email = 'pytest_user@example.com'

    cur.execute("DELETE FROM subscriber WHERE email = %s", (test_email,))
    db_conn.commit()

    cur.execute("INSERT INTO subscriber (email) VALUES (%s)", (test_email,))
    db_conn.commit()

    cur.execute("SELECT subscription_date FROM subscriber WHERE email = %s", (test_email,))
    row = cur.fetchone()
    assert row is not None, "No row returned for inserted subscriber"
    sub_date = row[0]
    assert isinstance(sub_date, datetime), "subscription_date is not a datetime"

    assert datetime.now() - sub_date < timedelta(minutes=1), \
        f"subscription_date ({sub_date}) not within the last minute"

    cur.execute("DELETE FROM subscriber WHERE email = %s", (test_email,))
    db_conn.commit()
    cur.close()
