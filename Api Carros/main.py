from flask import Flask, make_response, jsonify, request
from conecta_bd import conecta_banco, encerra_conexao



app = Flask(__name__)
app.config['JSON_SORTE_KEYS'] = False

@app.route('/carros', methods=['GET'])
def get_car():
    conn = conecta_banco()  # Conecta ao banco de dados Oracle
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Carros")
    meus_carros = cursor.fetchall()
    
    carros_list = []
    for carro in meus_carros:
        carros_list.append({
            'marca': carro[1],
            'modelo': carro[2],
            'ano': carro[3],
            'id': carro[0],
        })

    return make_response(
        jsonify(
            data=carros_list,
            message='Lista de carros'
        )
    )


@app.route('/carros', methods=['POST'])
def create_car():
    carro = request.json
    
    conn = conecta_banco()  # Conecta ao banco de dados Oracle
    cursor = conn.cursor()
    
    sql = f"INSERT INTO CARROS (marca, modelo, ano) VALUES ('{carro['marca']}', '{carro['modelo']}', '{carro['ano']}')"
    
    cursor.execute(sql)
    conn.commit()
    
    
    return  make_response(
        jsonify(
            message = 'Carro cadastrado com sucesso.',
            carro = carro
        )
    )
    
    
@app.route('/carros/<int:id>', methods=['DELETE'])
def delete_car(id):
    # Conectar ao banco de dados
    conn = conecta_banco()
    cursor = conn.cursor()

    try:
        # Verificar se o carro existe no banco de dados
        cursor.execute("SELECT * FROM Carros WHERE id = :id", {'id': id})
        carro = cursor.fetchone()
        if not carro:
            return make_response(jsonify(message=f"Carro com id {id} não encontrado"), 404)

        # Deletar o carro do banco de dados
        cursor.execute("DELETE FROM Carros WHERE id = :id", {'id': id})
        conn.commit()  # Commit da transação

        return make_response(jsonify(message=f"Carro com id {id} deletado com sucesso"), 200)

    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        return make_response(jsonify(message=f"Erro ao deletar carro: {str(e)}"), 500)

    finally:
        encerra_conexao(cursor, conn)  # Fechar conexão
        
        
@app.route('/carros', methods=['PUT'])
def update_car():
    # Obter dados da requisição
    dados = request.get_json()

    # Verificar se os dados necessários estão presentes
    if 'id' not in dados:
        return make_response(jsonify(message='O campo "id" é obrigatório'), 400)

    # Conectar ao banco de dados
    conn = conecta_banco()
    cursor = conn.cursor()

    try:
        # Verificar se o carro existe no banco de dados
        cursor.execute("SELECT * FROM Carros WHERE id = :id", {'id': dados['id']})
        carro = cursor.fetchone()
        if not carro:
            return make_response(jsonify(message=f"Carro com id {dados['id']} não encontrado"), 404)

        # Atualizar os dados do carro
        cursor.execute("""
            UPDATE Carros
            SET marca = :marca, modelo = :modelo, ano = :ano
            WHERE id = :id
        """, {
            'marca': dados.get('marca', carro[1]),  # Se não especificado, mantém o valor existente
            'modelo': dados.get('modelo', carro[2]),
            'ano': dados.get('ano', carro[3]),
            'id': dados['id']
        })

        conn.commit()  # Commit da transação

        return make_response(jsonify(message=f"Carro com id {dados['id']} atualizado com sucesso"), 200)

    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        return make_response(jsonify(message=f"Erro ao atualizar carro: {str(e)}"), 500)

    finally:
        encerra_conexao(cursor, conn)  # Fechar conexão
        
        
@app.route('/carros/<int:id>', methods=['GET'])
def get_car_by_id(id):
    # Conectar ao banco de dados
    conn = conecta_banco()
    cursor = conn.cursor()

    try:
        # Preparar e executar a consulta SQL
        sql = "SELECT * FROM Carros WHERE id = :id"
        cursor.execute(sql, {'id': id})

        # Recuperar o carro encontrado
        carro_id = cursor.fetchone()
        
        if not carro_id:
            return make_response(jsonify(message=f"Carro com id {id} não encontrado"), 404)
        
        carro_formatado = {
            'id': carro_id[0],
            'marca': carro_id[1],
            'modelo': carro_id[2],
            'ano': carro_id[3],
        }
        
        return make_response(jsonify(carro_formatado), 200)
    
    except Exception as e:
        return make_response(jsonify(message=f"Erro ao buscar carro por id {id}: {str(e)}"), 500)
    
    finally:
        encerra_conexao(cursor, conn)  # Fechar conexão
        
        

        
if __name__ == '__main__':
    app.run(debug=True)