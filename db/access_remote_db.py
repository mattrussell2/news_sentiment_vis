import pymysql

conn = pymysql.connections.Connection(host='0.tcp.ngrok.io',port=18650,user='newz',password='comp177')

conn.select_db('news_vis')

print(conn)
print(conn.open)

conn.close()
