from embeddings import Embedding
from url_to_content import url_to_content, is_valid_url
from vector_database import VectorDatabase
from image_to_text import image_to_text
import logging
from discord import Message


class Response:
    def __init__(self, db: VectorDatabase, embedding: Embedding, message: Message):
        self.db = db
        self.embedding = embedding
        self.message = message
        self.user_id = message.author.id

    def get_response(self):
        try:
            user_input = str(self.message.content)

            if len(self.message.attachments) > 0:
                image_url = self.message.attachments[0].url
                content = image_to_text(image_url)
                return self.embed_and_insert(content, image_url)

            if is_valid_url(user_input):
                content = url_to_content(user_input)
                return self.embed_and_insert(content, user_input)
            elif user_input.lower() == '!help':
                return ('If you want to to save a link, just copy paste it. \n If you want to lookup certain use "?" followed by your search terms. \n '
                        'Use "!all" to get all your saved links.')
            elif user_input[0] == '?':
                query_embedding = self.embedding.get_embeddings(user_input)
                result = self.db.query_from_db(query_embedding, self.user_id)
                return result
            elif user_input.lower() == '!all':
                return self.db.query_all(self.user_id)
            else:
                return 'Something went wrong, try !help for instructions'
        except Exception as e:
            logging.error(e)
            return 'Something went wrong, try !help for'

    def embed_and_insert(self, content, url):
        if content is not None and content != "":
            embedding = self.embedding.get_embeddings(content)
            self.db.insert_into_db(embedding, url, self.user_id)
            return 'Succesfully saved your link'
