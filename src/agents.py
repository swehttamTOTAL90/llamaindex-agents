"""Construção e execução da equipe multiagente."""

from crewai import Agent, Crew, LLM, Process, Task

from .config import AppConfig
from .tools import build_research_tools


def run_scientific_research(topic: str, config: AppConfig) -> str:
    """Executa a equipe de agentes para pesquisar e validar artigos científicos."""
    topic = topic.strip()
    if not topic:
        return "Informe um tema para iniciar a pesquisa."

    tools = build_research_tools(config)
    llm = LLM(model=config.crewai_model, api_key=config.nvidia_api_key)

    arxiv_agent = Agent(
        role="Agente de pesquisa no arXiv",
        goal="Encontrar artigos científicos relevantes sobre o tema informado.",
        backstory=(
            "Especialista em pesquisa científica que utiliza o arXiv para localizar "
            "trabalhos acadêmicos e suas referências."
        ),
        tools=[tools["arxiv"], tools["download"]],
        llm=llm,
    )

    web_agent = Agent(
        role="Agente de pesquisa científica na web",
        goal="Encontrar documentos científicos relevantes disponíveis na web.",
        backstory=(
            "Pesquisador especializado em localizar fontes científicas e documentos "
            "acadêmicos em mecanismos de busca."
        ),
        tools=tools["web"],
        llm=llm,
    )

    verification_agent = Agent(
        role="Agente de verificação",
        goal="Validar se os resultados encontrados são realmente artigos científicos.",
        backstory=(
            "Revisor de fontes acadêmicas responsável por filtrar resultados e manter "
            "somente documentos compatíveis com a pesquisa científica."
        ),
        tools=tools["web"],
        llm=llm,
    )

    manager = Agent(
        role="Gerente da pesquisa",
        goal="Coordenar os agentes e consolidar os melhores resultados.",
        backstory=(
            "Gerente de pesquisa responsável por organizar a execução da equipe, "
            "delegar atividades e garantir uma resposta final coerente."
        ),
        allow_delegation=True,
        llm=llm,
    )

    tasks = [
        Task(
            description=f"Busque no arXiv artigos científicos relevantes sobre: {topic}.",
            expected_output="Até 5 artigos relevantes com título e link.",
            agent=arxiv_agent,
        ),
        Task(
            description=f"Busque na web artigos científicos relevantes sobre: {topic}.",
            expected_output="Até 5 artigos relevantes com título e link.",
            agent=web_agent,
        ),
        Task(
            description=(
                "Verifique os documentos encontrados pela equipe e mantenha somente "
                "resultados que sejam artigos ou fontes acadêmicas válidas."
            ),
            expected_output=(
                "Lista consolidada de até 5 artigos científicos validados, com título, "
                "link e uma breve justificativa de relevância."
            ),
            agent=verification_agent,
        ),
    ]

    crew = Crew(
        agents=[arxiv_agent, web_agent, verification_agent],
        tasks=tasks,
        manager_agent=manager,
        process=Process.hierarchical,
        verbose=True,
    )

    return str(crew.kickoff())
