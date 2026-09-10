"""Configuração central da aplicação."""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
INDEXES_DIR = DATA_DIR / "indexes"
DOWNLOADS_DIR = ROOT_DIR / "downloads"


@dataclass(frozen=True)
class AppConfig:
    groq_api_key: str
    nvidia_api_key: str
    tavily_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    crewai_model: str = "nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"
    embedding_model: str = "intfloat/multilingual-e5-large"

    @property
    def articles_index_dir(self) -> Path:
        return INDEXES_DIR / "articles"

    @property
    def books_index_dir(self) -> Path:
        return INDEXES_DIR / "books"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Variável de ambiente {name} não configurada. "
            "Copie .env.example para .env e preencha as chaves necessárias."
        )
    return value


def load_config() -> AppConfig:
    """Carrega e valida as configurações da aplicação."""
    load_dotenv(ROOT_DIR / ".env")

    return AppConfig(
        groq_api_key=_required_env("GROQ_API_KEY"),
        nvidia_api_key=_required_env("NVIDIA_API_KEY"),
        tavily_api_key=_required_env("TAVILY_API_KEY"),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        crewai_model=os.getenv(
            "CREWAI_MODEL", "nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"
        ),
        embedding_model=os.getenv(
            "EMBEDDING_MODEL", "intfloat/multilingual-e5-large"
        ),
    )
