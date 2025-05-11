import sqlite3
from backend.schemas import ColaOut, AtividadeCreate, AtividadeOut
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.hash import bcrypt
from datetime import datetime, timedelta

SECRET_KEY = "segredo-supersecreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_conn():
    return sqlite3.connect("on_the_job.db")

def criar_colaborador(nome: str, cpf: str, data_adm: str, cargo: str, depart: str, nome_gestor: str, cargo_gestor: str):
    """Insere um novo colaborador no banco de dados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO admissao (
                colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, cpf, data_adm, cargo, depart, nome_gestor, cargo_gestor),
        )
        conn.commit()
        cid = cursor.lastrowid
        return ColaOut(
            id=cid,
            colaborador=nome,
            cpf=cpf,
            data_adm=data_adm,
            cargo=cargo,
            departamento=depart,
            nome_gestor=nome_gestor,
            cargo_gestor=cargo_gestor,
            atividades=[]
        )
    finally:
        conn.close()

def listar_colaborador():
    """Retorna uma lista de todos os colaboradores cadastrados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor FROM admissao")
        rows = cursor.fetchall()
        return [
            ColaOut(
                id=row[0],
                colaborador=row[1],
                cpf=row[2],
                data_adm=row[3],
                cargo=row[4],
                departamento=row[5],
                nome_gestor=row[6],
                cargo_gestor=row[7],
                atividades=listar_atividades_por_colaborador(row[0])
            )
            for row in rows
        ]
    finally:
        conn.close()

def listar_colaborador_individual(colab_id: int):
    """Retorna uma lista de todos os colaboradores cadastrados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT id, colaborador, cpf, data_adm, cargo, departamento, nome_gestor, cargo_gestor 
            FROM admissao 
            WHERE id = ?
            """,
            (colab_id,),
        )
        rows = cursor.fetchall()
        return [
            ColaOut(
                id=row[0],
                colaborador=row[1],
                cpf=row[2],
                data_adm=row[3],
                cargo=row[4],
                departamento=row[5],
                nome_gestor=row[6],
                cargo_gestor=row[7],
                atividades=listar_atividades_por_colaborador(row[0])
            )
            for row in rows
        ]
    finally:
        conn.close()

def adicionar_atividade(atividade: AtividadeCreate):
    """Adiciona uma atividade ao banco de dados."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividades (colaborador_id, descricao, comentario_colaborador, comentario_gestor, status, data)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (atividade.colaborador_id, atividade.descricao, atividade.comentario_colaborador, atividade.comentario_gestor, atividade.status, atividade.data),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def listar_atividades_por_colaborador(colaborador_id: int):
    """Retorna todas as atividades associadas a um colaborador."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, colaborador_id, descricao, comentario_colaborador, comentario_gestor, status, data
            FROM atividades
            WHERE colaborador_id = ?
            """,
            (colaborador_id,),
        )
        rows = cursor.fetchall()
        return [
            AtividadeOut(
                id=row[0],
                colaborador_id=row[1],
                descricao=row[2],
                comentario_colaborador=row[3],
                comentario_gestor=row[4],
                status=row[5],
                data=row[6]
            )
            for row in rows
        ]
    finally:
        conn.close()

def atualizar_colaborador(id: int, nome: str, cpf: str, data_adm: str, cargo: str, depart: str, nome_gestor: str, cargo_gestor: str):
    """Atualiza os dados de um colaborador pelo ID."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE admissao
            SET colaborador = ?, cpf = ?, data_adm = ?, cargo = ?, departamento = ?, nome_gestor = ?, cargo_gestor = ?
            WHERE id = ?
            """,
            (nome, cpf, data_adm, cargo, depart, nome_gestor, cargo_gestor, id),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_user(email: str):
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(email, senha, cargo):
    if get_user(email):
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()
    senha_hash = bcrypt.hash(senha)
    cursor.execute("INSERT INTO users (email, senha, cargo) VALUES (?, ?, ?)",
                   (email, senha_hash, cargo))
    conn.commit()
    conn.close()

def authenticate_user(email, senha):
    user = get_user(email)
    if not user:
        return False
    return bcrypt.verify(senha, user[2])

def create_token(email, cargo):
    payload = {
        "sub": email,
        "cargo": cargo,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")