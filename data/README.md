# Dados locais

Esta pasta é usada para os documentos que alimentam a camada de RAG e para os índices gerados pela aplicação.

## Estrutura

```text
data/
├── source_documents/
│   ├── articles/
│   └── books/
└── indexes/
```

Coloque em `source_documents/` somente documentos que você tem permissão para utilizar. Os PDFs e os índices vetoriais são ignorados pelo Git para evitar a publicação acidental de conteúdo protegido ou arquivos gerados localmente.

Depois de adicionar os documentos, execute:

```bash
python scripts/build_indexes.py
```

Os índices serão criados automaticamente em `data/indexes/articles/` e `data/indexes/books/`.
