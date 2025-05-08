import sqlite3
from typing import List
from backend.schemas import ColaOut

def get_conn():
    return sqlite3.connect("on_the_job.db")


def criar_colaborador(nome: str, cpf: str, data_adm: str, cargo: str, depart: str, nome_gestor: str, cargo_gestor: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admissao (colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, cpf, data_adm, cargo, depart, nome_gestor, cargo_gestor))
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return ColaOut(id=cid, colaborador=nome, cpf=cpf, data_adm=data_adm, cargo=cargo, departamento=depart, nome_gestor=nome_gestor, cargo_gestor=cargo_gestor)


def listar_colaborador():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admissao")
    rows = cursor.fetchall()
    conn.close()
    return [ColaOut(id=x[0], colaborador=x[1], cpf=x[2], data_adm=x[3], cargo=x[4], departamento=x[5], nome_gestor=x[6], cargo_gestor=x[7]) for x in rows]


def deletar_cliente(id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admissao WHERE id = ?", (id,))
    conn.commit()
    conn.close()


# def atualizar_cliente(id: int, nome: str, email: str):
#     conn = get_conn()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", (nome, email, id))
#     conn.commit()
#     updated = cursor.rowcount > 0
#     conn.close()
#     return updated