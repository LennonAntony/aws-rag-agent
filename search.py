from vector_store import connect
from embeddings import embed


def search_similar(question, top_k=3):
    # conectar no Milvus
    connect()
    collection = Collection("knowledge_base")

    # verificar se o campo de vetor existe
    vector_field = next((f for f in collection.describe()["fields"] if f["name"] == "embedding"), None)
    if vector_field is None:
        raise ValueError("Campo 'embedding' não encontrado na coleção.")

    # garantir que usamos COSINE, pois a coleção foi criada com COSINE
    metric_type = "COSINE"

    # gerar embedding da pergunta
    query_vector = embed(question)

    # buscar no Milvus
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param={"metric_type": metric_type, "params": {"nprobe": 10}},
        limit=top_k,
        output_fields=["text"]
    )

    # montar o contexto com os textos encontrados
    context = ""
    for hit in results[0]:
        context += hit.entity.get("text") + "\n\n"

    return context
