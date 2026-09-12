import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="company_documents"
)


def store_chunks(chunks, embeddings, file_id):

    ids = [
        f"{file_id}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"file_id": file_id}
            for _ in chunks
        ]
    )


def search_documents(query, n_results=5):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]