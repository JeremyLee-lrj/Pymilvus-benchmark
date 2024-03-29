import json

from pymilvus import model

ef = model.DefaultEmbeddingFunction()

with open("D:/Download/dqs_address.json","r", encoding="utf-8") as file:
    data = json.load(file)

# docs = [
#     "Artificial intelligence was founded as an academic discipline in 1956.",
#     "Alan Turing was the first person to conduct substantial research in AI.",
#     "Born in Maida Vale, London, Turing was raised in southern England.",
# ]

docs = data

embeddings = ef.encode_documents(docs)

print(type(embeddings))
print("length of Embeddings:", len(embeddings))
print("Dim:", ef.dim, embeddings[0].shape)
print("type for one dimension:", type(embeddings[0][0]))

embeddings_list = []
for embedding in embeddings:
    embeddings_list.append(embedding.tolist())

with open("D:/Download/dqs_address_embeddings.json","w", encoding="utf-8") as file:
    json.dump(embeddings_list, file)