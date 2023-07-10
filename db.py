import sqlite3


class Database:
    """Conexión con la DB"""

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

        # creamos la DB
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS
            preguntas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia INTEGER,
                tema INTEGER,
                pregunta TEXT NOT NULL,
                respuesta TEXT NOT NULL
            );
        """)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS
            materias(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia TEXT NOT NULL
            );
        """)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS
            temas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tema TEXT NOT NULL,
                materia_id INTEGER
            );
        """)

    def obtener_materias(self):
        return self.c.execute('SELECT * FROM materias').fetchall()

    def obtener_temas(self, materia_str):
        """Obtenemos los temas basados en la materia"""
        return self.c.execute("""
            SELECT t.id, t.tema FROM temas t 
            INNER JOIN materias m 
            ON m.id = t.materia_id
            WHERE m.materia = ?
            """, (materia_str, )).fetchall()

    def seleccionar_pregunta(self, id):
        pregunta = self.c.execute(
            'SELECT * FROM preguntas WHERE id = ?', (id, )).fetchone()
        return pregunta

    def eliminar_pregunta(self, id):
        self.c.execute('DELETE FROM preguntas WHERE id = ?', (id, ))
        self.conn.commit()

    def insertar_pregunta(self, materia, tema, pregunta, respuesta):
        # tomamos los ID de materia y tema
        materia_id = self.c.execute(
            'SELECT id FROM materias WHERE materia = ?', (materia, )).fetchone()
        tema_id = self.c.execute(
            'SELECT id FROM temas WHERE tema = ?', (tema, )).fetchone()

        print(materia_id)
        print(tema_id)

        # insertamos la pregunta
        self.c.execute("INSERT INTO preguntas (materia, tema, pregunta, respuesta) VALUES (?, ?, ?, ?)", (int(materia_id[0]), int(tema_id[0]), str(
            pregunta), str(respuesta)))
        self.conn.commit()
        print("Pregunta agregada correctamente.")
        self.mostrar_preguntas()

    def mostrar_preguntas(self):
        """Devuelve ID, id_Materia, Materia, id_Tema, Tema, Pregunta, Respuesta"""
        rows = self.c.execute("""
            SELECT p.id, m.id, m.materia, t.id, t.tema, p.pregunta, p.respuesta 
            FROM preguntas p
            INNER JOIN temas t
            ON t.id = p.tema
            INNER JOIN materias m
            ON m.id = p.materia
            """).fetchall()

        # las mostramos por consola
        # for row in rows:
        #    print(row)

        # retornamos el array
        return rows


# testing
pruebas_db = Database('preguntas_pruebas.db')
print(pruebas_db.obtener_temas('Traumato'))
