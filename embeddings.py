import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import torch.nn.functional as F
import logging


class Embedding:

    def __init__(self, tokenizer_name='bert-base-uncased', model_name='nomic-ai/nomic-embed-text-v1.5'):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True, safe_serialization=True)

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_embeddings(self, text):
        try:
            encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
            matryoshka_dim = 512

            with torch.no_grad():
                model_output = self.model(**encoded_input)

            embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
            embeddings = F.layer_norm(embeddings, normalized_shape=(embeddings.shape[1],))
            embeddings = embeddings[:, :matryoshka_dim]
            embeddings = F.normalize(embeddings, p=2, dim=1)
            embeddings = embeddings.numpy().tolist()[0]

            return embeddings
        except Exception as e:
            logging.error(e)
