---
title: init
description: Inicializa o rastreamento do Workstate no diretório atual.
---

O comando `init` prepara a pasta do seu projeto para ser gerenciada pelo Workstate através da criação dos arquivos de configuração necessários.

## Uso

```bash
workstate init
```

## Como funciona

1. **Cria o `.workstateinclude`**: Gera um arquivo de "whitelist" (inclusão) no seu diretório raiz. Apenas os arquivos e padrões listados aqui serão capturados pelo comando `save`.
2. **Popula Padrões**: Adiciona automaticamente padrões minimalistas ao arquivo (ex: `src/`, `README.md`, `pyproject.toml`).
3. **Auto-detecção**: Tenta detectar a stack do seu projeto (Python, Node, etc.) para ajustar a configuração inicial.

## Exemplos

```bash
cd meu-projeto
workstate init
```

:::note[Nota]
Inicializar um projeto não faz o upload de nada para o S3 ainda. Ele apenas prepara a configuração local. Use `workstate save` para criar seu primeiro snapshot.
:::
