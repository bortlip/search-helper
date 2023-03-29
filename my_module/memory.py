print("loading sentence_transformers")
from sentence_transformers import SentenceTransformer, util

import torch
import json
from nltk.tokenize import word_tokenize

MODEL_NAME = 'all-MiniLM-L6-v2'

class memory:
    def __init__(self):
        print("Loading model")
        self.embedder = SentenceTransformer(MODEL_NAME)
        self.next_id = 1
        self.memory = {}
        self.diry = True

    def add(self, sentence):
        self.memory[self.next_id] = sentence
        self.next_id += 1
        self.diry = True

    def search_topx(self, query, topx=5):
        text = list(self.memory.values())
        if self.diry:
            self.memory_embedding = self.embedder.encode(text, convert_to_tensor=True)
            self.diry = False

        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.memory_embedding)[0]

        top_k = min(topx, len(self.memory.keys()))
        top_results = torch.topk(cos_scores, k=top_k)

#        return [(text[idx], score) for score, idx in zip(top_results[0], top_results[1])]
        return [text[idx] for idx in top_results[1]]

    def search_word_length(self, query, word_length):
        text = list(self.memory.values())
        if self.diry:
            self.memory_embedding = self.embedder.encode(text, convert_to_tensor=True)
            self.diry = False

        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.memory_embedding)[0]

        top_k = min(1000, len(self.memory.keys()))
        top_results = torch.topk(cos_scores, k=top_k)

        results = []
        results_word_count = 0
        for idx in top_results[1]:
            result = text[idx]
            result_word_count = len(word_tokenize(result))
            if results_word_count + result_word_count <= word_length:
                results.append(result)
                results_word_count += result_word_count
            else:
                break
        return results

#        return [(text[idx], score) for score, idx in zip(top_results[0], top_results[1])]
#        return [text[idx] for idx in top_results[1]]


    def save(self, filename):
        with open(filename, "w") as file:
            json.dump(self.memory, file)

    def load(self, filename):
        with open(filename, "r") as file:
            self.memory = json.load(file)
            self.next_id = int(max(self.memory.keys())) + 1
