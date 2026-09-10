"""Construção e execução da equipe multiagente."""

from crewai import Agent, Crew, LLM, Process, Task

from .config import AppConfig
from .tools import build_research_tools


MAX_AGENT_ITERATIONS = 4


def run_scientific_research(topic: str, config: AppConfig) -> str:
    """Executa uma equipe de agentes em fluxo sequencial para pesquisar e validar artigos."""
    topic = topic.strip()
    if not topic:
        return "Informe um tema para iniciar a pesquisa."

    tools = build_research_tools(config)
    llm = LLM(model=config.crewai_model, api_key=config.nvidia_api_key)

    arxiv_agent = Agent(
        role="Agente de pesquisa no arXiv",
        goal="Encontrar artigos científicos realmente relacionados ao tema informado.",
        backstory=(
            "Especialista em pesquisa acadêmica no arXiv. Antes de usar a ferramenta, "
            "transforma o tema em uma consulta curta com palavras-chave científicas em inglês."
        ),
        tools=[tools["arxiv"]],
        llm=llm,
        allow_delegation=False,
        max_iter=MAX_AGENT_ITERATIONS,
        verbose=True,
    )

    web_agent = Agent(
        role="Agente de pesquisa científica na web",
        goal="Encontrar fontes acadêmicas complementares e relevantes para o tema.",
        backstory=(
            "Pesquisador especializado em localizar artigos e fontes acadêmicas confiáveis "
            "na web, usando consultas objetivas e evitando buscas desnecessárias."
        ),
        tools=tools["web"],
        llm=llm,
        allow_delegation=False,
        max_iter=MAX_AGENT_ITERATIONS,
        verbose=True,
    )

    verification_agent = Agent(
        role="Agente de verificação",
        goal="Consolidar e filtrar os resultados encontrados pelos pesquisadores.",
        backstory=(
            "Revisor acadêmico responsável por remover resultados fora do tema, duplicados "
            "ou claramente não científicos e produzir uma resposta final objetiva."
        ),
        llm=llm,
        allow_delegation=False,
        max_iter=MAX_AGENT_ITERATIONS,
        verbose=True,
    )

    arxiv_task = Task(
        description=(
            f"Pesquise no arXiv artigos científicos relevantes sobre: {topic}. "
            "Antes de chamar a ferramenta, converta o tema para uma consulta curta em inglês, "
            "com 3 a 8 palavras-chave científicas. Use a ferramenta search_arxiv no máximo uma "
            "vez, passando somente os argumentos topic e max_results=5. Não coloque explicações "
            "no nome da ação. Descarte resultados claramente fora do tema."
        ),
        expected_output=(
            "Até 5 artigos relevantes do arXiv com título, link e uma frase explicando a relação "
            "com o tema."
        ),
        agent=arxiv_agent,
    )

    web_task = Task(
        description=(
            f"Faça uma pesquisa complementar na web sobre: {topic}. Procure principalmente "
            "artigos científicos, preprints, páginas de periódicos ou instituições acadêmicas. "
            "Faça no máximo duas chamadas de busca e priorize relevância sobre quantidade."
        ),
        expected_output=(
            "Até 5 fontes acadêmicas relevantes com título, link e uma frase de relevância."
        ),
        agent=web_agent,
    )

    verification_task = Task(
        description=(
            "Revise os resultados produzidos pelos dois pesquisadores. Use apenas o conteúdo "
            "recebido das tarefas anteriores, sem realizar novas buscas. Remova itens fora do "
            "tema, duplicados ou sem caráter acadêmico. Responda em português."
        ),
        expected_output=(
            "Lista final de até 5 artigos ou fontes acadêmicas validadas, com título, origem, "
            "link e uma breve justificativa de relevância."
        ),
        agent=verification_agent,
    )

    crew = Crew(
        agents=[arxiv_agent, web_agent, verification_agent],
        tasks=[arxiv_task, web_task, verification_task],
        process=Process.sequential,
        verbose=True,
    )

    return str(crew.kickoff())
