import sqlite3


def init_db():
    conn = sqlite3.connect("on_the_job.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admissao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador TEXT,
            cpf TEXT,
            data_adm TEXT,
            cargo TEXT,
            departamento TEXT,
            nome_gestor TEXT,
            cargo_gestor TEXT
        )
    """)
    conn.commit()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        formulario_id INTEGER,
        atividade TEXT,
        comentario_colaborador TEXT,
        comentario_gestor TEXT,
        status TEXT,
        data TEXT,
        FOREIGN KEY (formulario_id) REFERENCES formularios(id)
        )
    """)
    conn.commit()