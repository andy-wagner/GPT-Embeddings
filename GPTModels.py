import numpy as np

class GPTTreeModelV2:
    def __init__(self, gpt_taxonomy_file):
        self.gpt_taxonomy_file = gpt_taxonomy_file
        self.gpt_graph = self.constructGraph(gpt_taxonomy_file)

    def constructGraph(self, gpt_taxonomy_file):
        cur_graph = dict()
        with open(gpt_taxonomy_file, "r") as f:
            for cur_line in f:
                token_list = cur_line.split(">")
                prev_token = ""
                for cur_token in token_list:
                    cur_token = cur_token.lower().strip()
                    if len(prev_token)==0:
                        prev_token = cur_token
                        continue

                    if cur_graph.get(prev_token) is None:
                        cur_graph[prev_token] = set()

                    if cur_graph.get(cur_token) is None:
                        cur_graph[cur_token] = set()

                    cur_graph[cur_token].add(prev_token)
                    cur_graph[prev_token].add(cur_token)
                    prev_token = cur_token
        return cur_graph

    def most_similar(self, input_text, topk):
        result_set = []
        for cur_key, cur_val in self.gpt_graph.items():
            if input_text in cur_key:
                result_set = result_set + list(cur_val)

        result_set = list(set(result_set))
        # result_set.sort()
        num_neighbors = len(result_set)

        # If you want all the neighbors.
        if topk == -1:
            return result_set

        if topk >= num_neighbors:
            return result_set
        else:
            return result_set[:topk]


class GPTTreeModel:
    def __init__(self, gpt_taxonomy_file):
        self.gpt_taxonomy_file = gpt_taxonomy_file
        self.gpt_graph = self.constructGraph(gpt_taxonomy_file)

    def getTokens(self, cur_text):
        cur_text = cur_text.replace("&", " ")
        return cur_text.split()

    def constructGraph(self, gpt_taxonomy_file):
        cur_graph = dict()
        with open(gpt_taxonomy_file, "r") as f:
            for cur_line in f:
                token_list = cur_line.split(">")
                prev_token = ""
                for cur_token in token_list:
                    cur_token = cur_token.lower().strip()
                    if len(prev_token)==0:
                        prev_token = cur_token
                        continue

                    prev_tokens_list = self.getTokens(prev_token)
                    cur_tokens_list = self.getTokens(cur_token)

                    for p_token in prev_tokens_list:
                        for c_token in cur_tokens_list:

                            if cur_graph.get(p_token) is None:
                                cur_graph[p_token] = set()

                            if cur_graph.get(c_token) is None:
                                cur_graph[c_token] = set()

                            cur_graph[p_token].add(c_token)
                            cur_graph[c_token].add(p_token)

                    prev_token = cur_token
        return cur_graph

    def most_similar(self, input_text, topk):
        input_text = input_text.lower()
        result_set = []

        if self.gpt_graph.get(input_text) is None:
            return result_set

        result_set = list(self.gpt_graph.get(input_text))
        # result_set.sort()
        num_neighbors = len(result_set)

        # If you want all the neighbors.
        if topk == -1:
            return result_set

        if topk >= num_neighbors:
            return result_set
        else:
            return result_set[:topk]

if __name__ == "__main__":

    gpt_taxonomy_file_name = "files/product_taxonomy.txt"
    model = GPTTreeModel(gpt_taxonomy_file_name)
    print(model.most_similar("wallet", 5))
    model2 = GPTTreeModelV2(gpt_taxonomy_file_name)
    print(model2.most_similar("wallet", 5))
