# Sistema Multiagente para Pesquisa Científica

Aplicação em Python voltada à pesquisa e consulta de artigos científicos utilizando **CrewAI**, **LlamaIndex**, **RAG** e modelos de linguagem.

O projeto combina agentes especializados para buscar artigos no arXiv, pesquisar documentos na web, validar resultados e consultar bases documentais indexadas.

## Principais funcionalidades

- Busca de artigos científicos no **arXiv**.
- Pesquisa complementar na web com **Tavily**.
- Coordenação de múltiplos agentes com **CrewAI**.
- Processo hierárquico com agente gerente.
- Recuperação de informações em bases documentais com **LlamaIndex**.
- Arquitetura **RAG** para consultas sobre documentos indexados.
- Embeddings com **Hugging Face**.
- Integração com modelos de linguagem via **Groq** e **NVIDIA NIM**.
- Interface interativa desenvolvida com **Gradio**.

## Arquitetura

O sistema possui agentes com responsabilidades distintas:

1. **Agente de pesquisa:** busca artigos relacionados ao tema informado utilizando o arXiv.
2. **Agente de pesquisa web:** procura documentos científicos na web.
3. **Agente de verificação:** valida os documentos encontrados.
4. **Agente gerente:** coordena a execução da equipe de forma hierárquica.

Além da pesquisa de artigos, a aplicação disponibiliza um agente baseado em **ReAct** para consultar duas bases documentais persistidas utilizando mecanismos de busca semântica.

## Tecnologias

- Python
- CrewAI
- LlamaIndex
- RAG
- Groq
- NVIDIA NIM
- Hugging Face Embeddings
- Tavily
- arXiv
- Gradio

## Estrutura do projeto

```text
llamaindex-agents/
├── README.md
└── llamaindex-agentes-main/
    ├── app/
    │   ├── app.py
    │   ├── artigo/
    │   ├── livro/
    │   └── requirements.txt
    ├── dados/
    └── thumb.png
```

## Como executar

1. Clone o repositório.
2. Entre na pasta da aplicação:

```bash
cd llamaindex-agentes-main/app
```

3. Crie e ative um ambiente virtual.
4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente utilizadas pela aplicação:

```env
GROQ_API_KEY=sua_chave
nvidia=sua_chave
TAVILY=sua_chave
```

> Observação: no código atual, a variável da Tavily é lida como `tavily`. Ajuste o nome no `.env` ou padronize a variável no código antes da execução.

6. Execute:

```bash
python app.py
```

## Objetivo do projeto

Este projeto foi desenvolvido para explorar o uso de **agentes de IA**, ferramentas externas e recuperação aumentada por geração em um fluxo de pesquisa científica, combinando busca, validação e consulta de conhecimento em uma única aplicação.

---

Projeto desenvolvido para fins de estudo e portfólio em **Inteligência Artificial Generativa** e **Sistemas Multiagentes**.