try:
    import pymysql
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "PyMySQL is required for the MySQL database backend. Install it with: pip install PyMySQL"
    ) from exc

pymysql.install_as_MySQLdb()