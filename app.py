"""Interface Gradio do sistema multiagente."""

import gradio as gr

from src.agents import run_scientific_research
from src.config import load_config
from src.rag import answer_document_question


def build_app():
    config = load_config()

    def research(topic: str) -> str:
        try:
            return run_scientific_research(topic, config)
        except Exception as exc:
            return f"Erro durante a pesquisa: {exc}"

    def ask_documents(question: str) -> str:
        try:
            return answer_document_question(question, config)
        except Exception as exc:
            return f"Erro durante a consulta: {exc}"

    with gr.Blocks(theme=gr.themes.Glass(), title="AI Scientific Research Assistant") as demo:
        gr.Markdown(
            "# Sistema Multiagente para Pesquisa Científica\n"
            "Pesquise artigos científicos e consulte bases documentais com agentes de IA."
        )

        with gr.Tab("Pesquisa de artigos"):
            topic = gr.Textbox(
                label="Tema da pesquisa",
                placeholder="Ex.: uso de inteligência artificial na detecção de doenças",
            )
            research_button = gr.Button("Pesquisar")
            research_output = gr.Textbox(label="Resultados", lines=18)
            research_button.click(research, inputs=topic, outputs=research_output)

        with gr.Tab("Consulta documental"):
            question = gr.Textbox(
                label="Pergunta",
                placeholder="Faça uma pergunta sobre as bases indexadas...",
            )
            ask_button = gr.Button("Consultar")
            answer_output = gr.Textbox(label="Resposta", lines=16)
            ask_button.click(ask_documents, inputs=question, outputs=answer_output)

    return demo


if __name__ == "__main__":
    build_app().launch()
