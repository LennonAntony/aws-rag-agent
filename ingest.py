import boto3
import pdfplumber
import io
from pymilvus import Collection
from vector_store import connect
from embeddings import embed


def chunk_text(text, chunk_size=800):
    """
    Divide o texto em pedaços menores (chunks)
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


def ingest():
    connect()
    collection = Collection("knowledge_base")

    s3 = boto3.client("s3")
    bucket = "rag-agent-documents"

    objects = s3.list_objects_v2(Bucket=bucket)

    if "Contents" not in objects:
        print("Bucket vazio.")
        return

    for obj in objects["Contents"]:

        # Processar apenas PDFs
        if not obj["Key"].lower().endswith(".pdf"):
            continue

        print(f"Processando: {obj['Key']}")

        file = s3.get_object(Bucket=bucket, Key=obj["Key"])
        pdf_bytes = file["Body"].read()

        # Extrair texto do PDF
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            print("PDF sem texto extraível.")
            continue

        # Dividir em chunks
        chunks = chunk_text(text)

        for chunk in chunks:
            vector = embed(chunk)

            collection.insert([
                [vector],     # campo de vetor
                [chunk]       # campo de texto
            ])

    collection.flush()
    print("Ingestão concluída com sucesso.")


if __name__ == "__main__":
    ingest()