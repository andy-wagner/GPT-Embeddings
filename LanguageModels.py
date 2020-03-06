import numpy as np
import io

class FastTextEmbeddingsModel:
    def __init__(self, embeddings_file_name, embeddings_dimensions):
        self.embeddings_file = embeddings_file_name
        self.embeddings_model = self.__load_vectors()
        self.num_dims = embeddings_dimensions

    def __load_vectors(self):
        f = io.open(self.embeddings_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
        e_model = {}
        for line in f:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            e_model[word] = embedding
        print("Done.", len(e_model), " words loaded!")
        return e_model

    # Generate word embeddings for each word in the sentence:
    def __getWordEmbeddings(self, tokens_list):
        word_embeddings = []
        for word in tokens_list:
            try:
                word_embeddings.append(list(self.embeddings_model[word]))
            except:
                error_word = word
            # print("Key error :", error_word)
        if len(word_embeddings) == 0:
            word_embeddings.append(list(np.random.uniform(size=(self.num_dims))))
        return np.array(word_embeddings)

    # Compute the sentence embeddings using the individual word embeddings:
    def __getSentenceEmbeddings(self, word_embeddings):
        avg_sent_embeddings = np.mean(word_embeddings, axis=0)
        return avg_sent_embeddings

    def getEmbeddingsForSentence(self, query_sentence):
        cur_sentence_tokens = query_sentence.split()
        word_embeddings_list = self.__getWordEmbeddings(cur_sentence_tokens)
        sentence_embeddings = self.__getSentenceEmbeddings(word_embeddings_list)
        return sentence_embeddings

    def getEmbeddingsForTokenList(self, query_token_list):
        word_embeddings_list = self.__getWordEmbeddings(query_token_list)
        sentence_embeddings = self.__getSentenceEmbeddings(word_embeddings_list)
        return sentence_embeddings

if __name__ == "__main__":
    embeddings_file = "fasttext_word_vectors_wiki_news.vec"
    embeddings_dims = 300
    embeddings_model = FastTextEmbeddingsModel(embeddings_file, embeddings_dims)
    sample_sentence = "This men s dress is blue in color"
    temp = embeddings_model.getEmbeddingsForSentence(sample_sentence)
    print(temp)