"""Ferramentas externas usadas pelos agentes de pesquisa."""

from pathlib import Path
from urllib.parse import urlparse

import arxiv
import requests
from crewai_tools import LlamaIndexTool
from llama_index.core.tools import FunctionTool
from llama_index.tools.tavily_research import TavilyToolSpec

from .config import AppConfig, DOWNLOADS_DIR


def search_arxiv(topic: str, max_results: int = 5) -> str:
    """Pesquisa artigos relevantes no arXiv e retorna resultados formatados."""
    topic = topic.strip()
    if not topic:
        return "Informe um tema para pesquisar no arXiv."

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    client = arxiv.Client()

    results = []
    for item in client.results(search):
        results.append(
            "\n".join(
                [
                    f"Título: {item.title}",
                    f"Resumo: {item.summary}",
                    f"Categoria: {item.primary_category}",
                    f"Link: {item.entry_id}",
                ]
            )
        )

    return "\n\n".join(results) if results else "Nenhum artigo encontrado."


def _extract_arxiv_id(link: str) -> str:
    """Extrai o identificador de um link abs/pdf do arXiv."""
    parsed = urlparse(link.strip())
    if parsed.netloc not in {"arxiv.org", "www.arxiv.org"}:
        raise ValueError("O link informado não pertence ao arXiv.")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2 or parts[0] not in {"abs", "pdf"}:
        raise ValueError("Use um link de artigo no formato arxiv.org/abs/... ou /pdf/...")

    arxiv_id = parts[1].removesuffix(".pdf")
    if not arxiv_id:
        raise ValueError("Não foi possível identificar o artigo no link informado.")
    return arxiv_id


def download_arxiv_pdf(link: str) -> str:
    """Baixa um artigo do arXiv para a pasta local downloads/."""
    try:
        arxiv_id = _extract_arxiv_id(link)
    except ValueError as exc:
        return str(exc)

    download_dir = Path(DOWNLOADS_DIR)
    download_dir.mkdir(parents=True, exist_ok=True)
    destination = download_dir / f"arxiv_{arxiv_id.replace('/', '_')}.pdf"
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    try:
        with requests.get(pdf_url, stream=True, timeout=30) as response:
            response.raise_for_status()
            with destination.open("wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
    except requests.RequestException as exc:
        return f"Não foi possível baixar o PDF: {exc}"

    return f"PDF salvo em {destination}"


def build_research_tools(config: AppConfig):
    """Cria as ferramentas usadas pelos agentes CrewAI."""
    arxiv_tool = FunctionTool.from_defaults(
        fn=search_arxiv,
        name="search_arxiv",
        description="Busca artigos científicos relevantes no arXiv a partir de um tema.",
    )
    download_tool = FunctionTool.from_defaults(
        fn=download_arxiv_pdf,
        name="download_arxiv_pdf",
        description="Baixa o PDF de um artigo a partir de um link válido do arXiv.",
    )

    tavily_spec = TavilyToolSpec(api_key=config.tavily_api_key)
    tavily_tools = [LlamaIndexTool.from_tool(tool) for tool in tavily_spec.to_tool_list()]

    return {
        "arxiv": LlamaIndexTool.from_tool(arxiv_tool),
        "download": LlamaIndexTool.from_tool(download_tool),
        "web": tavily_tools,
    }
