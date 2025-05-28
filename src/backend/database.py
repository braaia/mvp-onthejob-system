import sqlite3

def init_db():
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()

    # Tabela admissao
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admissao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador TEXT NOT NULL,
            cpf TEXT NOT NULL,
            data_adm TEXT NOT NULL,
            cargo TEXT NOT NULL,
            departamento TEXT NOT NULL,
            nome_gestor TEXT NOT NULL,
            cargo_gestor TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    
    # Tabela atividades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            comentario_colaborador TEXT,
            status TEXT NOT NULL,
            assinatura_colab TEXT,
            assinatura_gestor TEXT,
            data TEXT NOT NULL,
            FOREIGN KEY (colaborador_id) REFERENCES admissao(id)
        )
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL     
        )
    """)
    conn.commit()
    conn.close()