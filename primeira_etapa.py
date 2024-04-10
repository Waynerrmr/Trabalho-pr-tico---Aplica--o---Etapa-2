#  Implementar um programa em qualquer linguagem de programação escolhida pelo
#  grupo que faz a comunicação com o SGBD. O programa deve se conectar ao SGBD
#  criado na parte 3 do trabalho prático. Além disso, deve ter dois métodos, um método
#  para inserir uma linha e outro para consultar alguma tabela escolhida pelo grupo.
#  Nessa etapa não deve ser usado nenhum framework de desenvolvimento. O código
#  deve ser executado localmente e as consultas devem estar explícitas nos métodos.
#  Será criada uma tarefa no SIGAA e basta enviar o código-fonte

import psycopg2

# Parâmetros de conexão
dbname = 'Parte-3'
user = 'WaynerYtallo'
password = 'WaynerYtallo'
host = 'database-faculdade.cdqauergwnin.us-east-1.rds.amazonaws.com'
port = '5432'
schema = 'mydb'

def conectar():
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        print(f'Conectado ao banco de dados {dbname}')
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

def inserir_linha(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SET search_path TO {schema}")
        print('\nSearch_path definido para', schema)

        # Exemplo de inserção na tabela Endereço
        cursor.execute('INSERT INTO "Endereço" (cep, logradouro, rua, numero, bairro, cidade) VALUES (%s, %s, %s, %s, %s, %s);', 
                       (49097330, 'Avenida Augusto Franco', 'C', 10, 'Ponto Novo', 'Aracaju'))
        conn.commit()
        print("Inserção realizada com sucesso!")
        cursor.close()
    except psycopg2.Error as e:
        print("Erro ao inserir linha:", e)

def consultar_tabela(conn, tabela):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SET search_path TO {schema}")
        print('\nSearch_path definido para', schema)

        cursor.execute(f'SELECT * FROM "{tabela}";')
        rows = cursor.fetchall()
        print(f"Consultando tabela {tabela}:")
        for row in rows:
            print(row)
        cursor.close()
    except psycopg2.Error as e:
        print("Erro ao consultar tabela:", e)

# Função principal
def main():
    conn = conectar()
    if conn:
        inserir_linha(conn)
        consultar_tabela(conn, 'Endereço')
        conn.close()

if __name__ == "__main__":
    main()
