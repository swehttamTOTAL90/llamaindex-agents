"""Camada de RAG para consulta das bases documentais."""

from functools import lru_cache
from pathlib import Path

from llama_index.core import Settings as LlamaSettings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

from .config import AppConfig


def _configure_llamaindex(config: AppConfig) -> None:
    LlamaSettings.llm = Groq(
        model=config.groq_model,
        api_key=config.groq_api_key,
    )
    LlamaSettings.embed_model = HuggingFaceEmbedding(
        model_name=config.embedding_model
    )


def _load_engine(index_dir: Path, *, name: str, description: str):
    if not index_dir.exists() or not any(index_dir.iterdir()):
        raise FileNotFoundError(
            f"Índice não encontrado em {index_dir}. "
            "Execute `python scripts/build_indexes.py` antes de iniciar a aplicação."
        )

    storage_context = StorageContext.from_defaults(persist_dir=str(index_dir))
    index = load_index_from_storage(storage_context)
    engine = index.as_query_engine(similarity_top_k=3)

    return QueryEngineTool(
        query_engine=engine,
        metadata=ToolMetadata(name=name, description=description),
    )


def build_query_tools(config: AppConfig):
    """Carrega os índices persistidos e cria as ferramentas de consulta."""
    _configure_llamaindex(config)

    return [
        _load_engine(
            config.articles_index_dir,
            name="articles_engine",
            description=(
                "Consulta a base de artigos científicos indexados. Use perguntas "
                "detalhadas em linguagem natural."
            ),
        ),
        _load_engine(
            config.books_index_dir,
            name="books_engine",
            description=(
                "Consulta a base de livros e documentos de referência indexados. "
                "Use perguntas detalhadas em linguagem natural."
            ),
        ),
    ]


def answer_document_question(question: str, config: AppConfig) -> str:
    """Responde uma pergunta usando um agente ReAct sobre as bases locais."""
    question = question.strip()
    if not question:
        return "Digite uma pergunta para consultar a base documental."

    tools = build_query_tools(config)
    agent = ReActAgent.from_tools(tools, verbose=True)
    response = agent.chat(question)
    return str(response)
