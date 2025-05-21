import psycopg2
import os

def get_conn():
    return psycopg2.connect(
        "postgresql://on_the_job_user:umOYBWCxNvuwnHP6m1gKhCPpfeDgPfg7@dpg-d0mrs0umcj7s739j98v0-a/on_the_job"
    )

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    # Tabela admissao
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admissao (
            id SERIAL PRIMARY KEY,
            colaborador TEXT NOT NULL,
            cpf TEXT NOT NULL,
            data_adm TEXT NOT NULL,
            cargo TEXT NOT NULL,
            departamento TEXT NOT NULL,
            nome_gestor TEXT NOT NULL,
            cargo_gestor TEXT NOT NULL
        )
    """)
    # Tabela atividades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id SERIAL PRIMARY KEY,
            colaborador_id INTEGER NOT NULL REFERENCES admissao(id) ON DELETE CASCADE,
            descricao TEXT NOT NULL,
            comentario_colaborador TEXT,
            status TEXT,
            data TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            "user" TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()