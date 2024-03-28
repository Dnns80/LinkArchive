import psycopg2
import os
import logging


class VectorDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(f"{os.getenv('DATABASE_URL')}")

    def insert_into_db(self, embedding, link, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO embeddings (user_id, embedding, link) VALUES (%s, %s, %s);",
                (user_id, embedding, link)
            )
            self.conn.commit()
            cur.close()
        except Exception as e:
            logging.error(e)

    def query_from_db(self, query_embedding, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                SELECT link
                FROM embeddings
                WHERE user_id = %s
                AND ABS(embedding <#> %s::vector) >= 0.5
                ORDER BY embedding <#> %s::vector
                LIMIT 5;
                """,
                (user_id, query_embedding, query_embedding,)
            )
            self.conn.commit()
            similar_text = cur.fetchall()
            links = [link[0] for link in similar_text]
            cur.close()
            return '\n'.join(links)
        except Exception as e:
            logging.error(e)

    def query_all(self, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                SELECT link
                FROM embeddings
                WHERE user_id = %s
                """,
                (user_id,)
            )
            self.conn.commit()
            links = cur.fetchall()
            links = [link[0] for link in links]
            cur.close()
            return '\n'.join(links)
        except Exception as e:
            logging.error(e)
