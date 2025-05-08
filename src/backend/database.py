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