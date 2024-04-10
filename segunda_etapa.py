#  API Web que efetua o CRUD (insert,delete,
#  update e leitura) de três tabelas do banco de dados, sendo duas tabelas geradas a
#  partir de entidades e uma tabela gerada a partir de um relacionamento ou
#  agregação.
#  A aplicação desenvolvida não representa a aplicação descrita na especificação.
#  Essa etapa tem como objetivo o desenvolvimento de um programa que se comunica
#  com umSGBDeexecuta operações de manipulação de dados.
#  Nesta etapa, é necessário enviar o código fonte idealmente através de um projeto
#  no github ou ferramenta similar. Além disso, ao final da disciplina, o grupo deverá
#  apresentar a apresentação funcionando diretamente ao professor

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Parâmetros de conexão
dbname = 'Parte-3'
user = 'WaynerYtallo'
password = 'WaynerYtallo'
host = 'database-faculdade.cdqauergwnin.us-east-1.rds.amazonaws.com'
port = '5432'

# Função para conectar ao banco de dados
def conectar():
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Endpoint para criar um endereco
@app.route('/endereco', methods=['POST'])
def criar_endereco():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        data = request.json
        cursor.execute('INSERT INTO mydb."Endereço" (cep, logradouro, rua, numero, bairro, cidade) VALUES (%s, %s, %s, %s, %s, %s);', 
                       (data['cep'], data['logradouro'], data['rua'], data['numero'], data['bairro'], data['cidade']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensagem': 'endereco criado com sucesso'}), 201
    return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

# Endpoint para listar todos os enderecos
@app.route('/enderecos', methods=['GET'])
def listar_enderecos():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mydb."Endereço"')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        enderecos = [{'cep': row[0], 'logradouro': row[1], 'rua': row[2], 'numero': row[3], 'bairro': row[4], 'cidade':row[5]} for row in rows]
        return jsonify(enderecos)
    return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

# Endpoint para atualizar um endereco
@app.route('/enderecos/<int:cep>', methods=['PUT'])
def atualizar_endereco(cep):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        data = request.json
        cursor.execute('UPDATE mydb."Endereço" SET cep = %s, logradouro = %s, rua = %s, numero = %s, bairro = %s, cidade = %s WHERE cep = %s', 
                       (data['cep'], data['logradouro'], data['rua'], data['numero'], data['bairro'], data['cidade'], cep))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensagem': 'endereco atualizado com sucesso'})
    return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

# Endpoint para deletar um endereco
@app.route('/enderecos/<int:cep>', methods=['DELETE'])
def deletar_endereco(cep):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM mydb."Endereço" WHERE cep = %s', (cep,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensagem': 'endereco deletado com sucesso'})
    return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 500

if __name__ == '__main__':
    app.run(debug=True)
