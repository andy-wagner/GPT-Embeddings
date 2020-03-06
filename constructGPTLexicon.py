import string

def getTokens(cur_text):
    cur_text = cur_text.replace("&", " ")
    return cur_text.split()

def writeGraph(graph, out_file):
    result = ""
    for cur_key in graph.keys():
        result = result + cur_key + " "
        cur_val_list = list(graph[cur_key])
        for cur_val in cur_val_list:
            result = result + cur_val + " "
        result = result.strip() + "\n"

    with open(out_file, "w") as f:
        f.write(result)

if __name__ == "__main__":

    #Config:
    taxonomy_file = "files/product_taxonomy.txt"
    f_obj = open(taxonomy_file, "r")

    gpt_graph = dict()

    for cur_line in f_obj:
        cur_line = cur_line.lower()
        tokens_list = cur_line.split(">")

        prev_token = ""
        cur_token = ""
        for token in tokens_list:
            if len(prev_token)==0:
                prev_token = token.strip()
                continue

            cur_token = token.strip()
            prev_tokens_list = getTokens(prev_token)
            cur_tokens_list = getTokens(cur_token)

            for p_token in prev_tokens_list:
                for c_token in cur_tokens_list:

                    if not gpt_graph.get(p_token):
                        gpt_graph[p_token] = set()

                    if not gpt_graph.get(c_token):
                        gpt_graph[c_token] = set()

                    gpt_graph[p_token].add(c_token)
                    gpt_graph[c_token].add(p_token)


            prev_token = cur_token


    writeGraph(gpt_graph, "files/gpt_lexicon.txt")