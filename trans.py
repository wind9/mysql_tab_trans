import pymysql
import logging
import os

db_host = '192.168.1.180'
db_port = 3307
db_user = 'admin'
db_password = 'admin'
log_path = os.path.join(os.path.dirname(__file__), __name__ + '.log')

con = pymysql.Connect(host=db_host, port=db_port, user=db_user, passwd=db_password)
cursor = con.cursor()


def get_log(log_path):
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    file_hanblder = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
    file_hanblder.setFormatter(formatter)
    log.addHandler(file_hanblder)
    return log


def get_src_tables():
    tables = []
    try:
        sql = "select table_name from information_schema.tables where table_schema='test' and table_name like 'Group%'"
        log.info("执行SQL:{}".format(sql))
        cursor.execute(sql)
        result = cursor.fetchall()
        for r in result:
            tables.append(r[0])
    except Exception as e:
        log.info("查询执行异常")
        log.exception(e)
    finally:
        return tables


def trans_table(src_table, dst_table):
    try:
        sql = "insert into {} select * from {}".format(dst_table, src_table)
        log.info("开始从{}复制数据至{}".format(src_table, dst_table))
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        log.info("执行异常")
        log.exception(e)


log = get_log(log_path)
log.info("测试log")
tables = get_src_tables()
for t in tables:
    src_table = "test.{}".format(t)
    dst_table = "data.Group"
    trans_table(src_table, dst_table)
cursor.close()
con.close()
log.info("数据迁移完成,连接已关闭")
