"""Gera os índices vetoriais usados pela camada de RAG.

Coloque documentos permitidos para uso em:
- data/source_documents/articles/
- data/source_documents/books/

Depois execute: python scripts/build_indexes.py
"""

from pathlib import Path
import sys

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.config import DATA_DIR, INDEXES_DIR  # noqa: E402


EMBEDDING_MODEL = "intfloat/multilingual-e5-large"


def build_index(source_dir: Path, destination_dir: Path) -> None:
    files = [path for path in source_dir.rglob("*") if path.is_file()]
    if not files:
        print(f"[AVISO] Nenhum documento encontrado em {source_dir}")
        return

    print(f"[INFO] Carregando {len(files)} arquivo(s) de {source_dir}...")
    documents = SimpleDirectoryReader(
        input_dir=str(source_dir),
        recursive=True,
    ).load_data()

    print(f"[INFO] Criando índice com {len(documents)} documento(s)...")
    index = VectorStoreIndex.from_documents(documents, show_progress=True)

    destination_dir.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(destination_dir))
    print(f"[OK] Índice salvo em {destination_dir}")


def main() -> None:
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

    source_root = DATA_DIR / "source_documents"
    INDEXES_DIR.mkdir(parents=True, exist_ok=True)

    build_index(source_root / "articles", INDEXES_DIR / "articles")
    build_index(source_root / "books", INDEXES_DIR / "books")


if __name__ == "__main__":
    main()
