from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from dbconn import consultaCPF, criaCliente, criaProduto, atualizaProduto, deletaProduto, consultaProduto, consultaPedido, criaPedido

app = Flask(__name__)
swagger = Swagger(app)

#
# Toda a parte de consulta e conexões no banco ficam no arquivo dbconn.py
#


## Identificação do cliente via CPF
@app.route('/cliente/<cpf>', methods=['GET'])
@swag_from('./apiDocs/cliente.yml', methods=['get'])
def get_cliente(cpf):
        cliente = consultaCPF(cpf)
        if cliente:
            return jsonify({
                "cpf": cliente[0],
                "nome": cliente[1],
                "email": cliente[2]
            })

## Cadastro do cliente
@app.route('/cliente', methods=['POST'])
@swag_from('./apiDocs/cliente.yml', methods=['post'])
def post_cliente():
        data = request.get_json()
        cpf = data['cpf']
        nome = data['nome']
        email = data['email']
        criaCliente(cpf, nome, email)
        return jsonify({"message": "Cliente criado com sucesso"}), 201

## Criar produto
@app.route('/produto', methods=['POST'])
@swag_from('./apiDocs/produtos.yml', methods=['post'])
def post_produto():
    try:
        data = request.get_json()
        categoria = data['categoria']
        nome = data['nome']
        preco = data['preco']
        descricao = data.get('descricao', '')
        criaProduto(categoria, nome, preco, descricao)
        return jsonify({"message": "Produto criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## Remover Produto
@app.route('/produto/<int:codigo>', methods=['DELETE'])
@swag_from('./apiDocs/produtos.yml', methods=['delete'])
def delete_produto(codigo):
    try:
        deletaProduto(codigo)
        return jsonify({"message": "Produto removido com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## Editar Produto
@app.route('/produto/<int:codigo>', methods=['PUT'])
@swag_from('./apiDocs/produtos.yml', methods=['put'])
def  put_produto (codigo):   
    try:
        data = request.get_json()
        categoria = data.get('categoria')
        nome = data.get('nome')
        preco = data.get('preco')
        descricao = data.get('descricao')
        atualizaProduto(codigo, categoria, nome, preco, descricao)
        return jsonify({"message": "Produto atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## Buscar produto por categoria ou sem (lista todos)
@app.route('/produto', methods=['GET'])
@swag_from('./apiDocs/produtos.yml', methods=['get'])
def get_produto():
    try:
        categoria = request.args.get('categoria')
        produto = consultaProduto(categoria)
        return jsonify(produto), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## Fake Checkout - Envia produtos para 'fila' = tb_pedido
@app.route('/pedido', methods=['POST'])
@swag_from('./apiDocs/pedidos.yml', methods=['post'])
def post_pedido():
    try:
        data = request.get_json()
        cpf = data['cpf']
        lanche = data['lanche']
        bebida = data['bebida']
        acompanhamento = data['acompanhamento']
        sobremesa = data['sobremesa']
        criaPedido(cpf, lanche, bebida, acompanhamento, sobremesa)
        return jsonify({"message": "Pedido criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## Lista os pedidos
@app.route('/pedido', methods=['GET'])
@swag_from('./apiDocs/pedidos.yml', methods=['get'])
def get_pedido():
    try:
        pedidos = consultaPedido()
        return jsonify(pedidos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)