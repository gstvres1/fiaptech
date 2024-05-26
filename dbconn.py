import psycopg2
import os

def get_connection():
    connection = psycopg2.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return connection

def consultaCPF(cpf):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_cliente WHERE cpf = %s", (cpf,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def criaCliente(cpf, nome, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tb_cliente (cpf, nome, email) VALUES (%s, %s, %s)",(cpf, nome, email))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def criaProduto(categoria, nome, preco, descricao):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO db_produto (categoria, nome, preco, descricao) VALUES (%s, %s, %s, %s)",(categoria, nome, preco, descricao))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def deletaProduto(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM db_produto WHERE codigo = %s",(codigo,))
        if cursor.rowcount == 0:
            raise Exception("Produto não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def atualizaProduto(codigo, categoria, nome, preco, descricao):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE db_produto SET categoria = COALESCE(%s, categoria), nome = COALESCE(%s, nome), preco = COALESCE(%s, preco), descricao = COALESCE(%s, descricao) WHERE codigo = %s",(categoria, nome, preco, descricao, codigo))
        if cursor.rowcount == 0:
            raise Exception("Produto não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def consultaProduto(categoria=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if categoria:
            cursor.execute("SELECT codigo, categoria, nome, preco, descricao FROM db_produto WHERE categoria = %s",(categoria,))
        else:
            cursor.execute("SELECT codigo, categoria, nome, preco, descricao FROM db_produto")
        rows = cursor.fetchall()
        produto = []
        for row in rows:
            produto.append({
                "codigo": row[0],
                "categoria": row[1],
                "nome": row[2],
                "preco": row[3],
                "descricao": row[4]
            })
        return produto
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def criaPedido(cpf, lanche, bebida, acompanhamento, sobremesa):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tb_pedido (cpf, lanche, bebida, acompanhamento, sobremesa, status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING npedido",
            (cpf, lanche, bebida, acompanhamento, sobremesa, 'Recebido')
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def consultaPedido():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT npedido, cpf, lanche, bebida, acompanhamento, sobremesa, status FROM tb_pedido"
        )
        rows = cursor.fetchall()
        pedidos = []
        for row in rows:
            pedidos.append({
                "npedido": row[0],
                "cpf": row[1],
                "lanche": row[2],
                "bebida": row[3],
                "acompanhamento": row[4],
                "sobremesa": row[5],
                "status": row[6]
            })
        return pedidos
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT npedido, cpf, status FROM tb_pedido")
        pedidos_rows = cursor.fetchall()
        pedidos = []
        for pedido_row in pedidos_rows:
            cursor.execute("SELECT codigo_produto, quantidade FROM tb_pedido_produto WHERE npedido = %s",(pedido_row[0],))
            produtos_rows = cursor.fetchall()
            produtos = [{"codigo": row[0], "quantidade": row[1]} for row in produtos_rows]
            pedidos.append({
                "npedido": pedido_row[0],
                "cpf": pedido_row[1],
                "status": pedido_row[2],
                "produtos": produtos
            })
        return pedidos
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()