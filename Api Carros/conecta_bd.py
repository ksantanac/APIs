import cx_Oracle

def conecta_banco():
    try:
        dsn = cx_Oracle.makedsn(host="oracle.fiap.com.br", port=1521, sid="ORCL")
        
        conn = cx_Oracle.connect(user='rm551732', password='fiap24', dsn=dsn)
        print("Conectado na primeira tentativa")

    except Exception as ex:
        print(f"Erro ({ex}) na primeira tentativa...tentando segunda forma")
        cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_14")  # Certifique-se de que este caminho está correto
        conn = cx_Oracle.connect(user='rm551732', password='fiap24', dsn=dsn)
    finally:
        print("Conectado!")
    
    return conn

def encerra_conexao(cursor, conn):
    cursor.close()
    conn.close()
    print("Conexão encerrada com sucesso!")

