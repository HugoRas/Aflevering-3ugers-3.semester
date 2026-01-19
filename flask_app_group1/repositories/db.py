import logging
import mariadb


def get_conn(cfg):
    logging.info(
        "DB cfg: host=%r port=%r user=%r db=%r password_set=%s",
        cfg.get("DB_HOST"),
        cfg.get("DB_PORT", 3306),
        cfg.get("DB_USER"),
        cfg.get("DB_NAME"),
        bool(cfg.get("DB_PASSWORD")),
    )

    return mariadb.connect(
        host=cfg["DB_HOST"],
        port=int(cfg.get("DB_PORT", 3306)),
        user=cfg["DB_USER"],
        password=cfg["DB_PASSWORD"],
        database=cfg["DB_NAME"],
        connect_timeout=5,
        autocommit=True,   # ok til jeres setup
    )


def _cursor(conn):
    return conn.cursor(dictionary=True)


def fetchone_dict(cfg, sql: str, params=()):
    conn = get_conn(cfg)
    cur = _cursor(conn)
    try:
        cur.execute(sql, params)
        return cur.fetchone()
    except Exception:
        logging.exception("DB fetchone failed. SQL=%r params=%r", sql, params)
        raise
    finally:
        cur.close()
        conn.close()


def fetchall_dict(cfg, sql: str, params=()):
    conn = get_conn(cfg)
    cur = _cursor(conn)
    try:
        cur.execute(sql, params)
        return cur.fetchall()
    except Exception:
        logging.exception("DB fetchall failed. SQL=%r params=%r", sql, params)
        raise
    finally:
        cur.close()
        conn.close()


def execute(cfg, sql: str, params=()):
    conn = get_conn(cfg)
    cur = _cursor(conn)
    try:
        logging.debug("EXECUTING SQL: %r | params=%r", sql, params)
        cur.execute(sql, params)
        return getattr(cur, "lastrowid", None)
    except Exception:
        logging.exception("DB execute failed. SQL=%r params=%r", sql, params)
        raise
    finally:
        cur.close()
        conn.close()
