---
title: Desenvolvimento
description: Guia para contribuidores interessados em buildar, testar ou expandir o Workstate.
---

Se você deseja contribuir para o Workstate ou testar mudanças no código-fonte, este guia detalha como configurar seu ambiente de desenvolvimento.

## Build e Instalação Local

Utilizamos o [Hatch](https://hatch.pypa.io/) como build backend e gerenciador de ambientes.

### 1. Configurar Ambiente
```bash
git clone https://github.com/mtpontes/workstate.git
cd workstate
pip install -r requirements.txt
```

### 2. Comandos de Conveniência (Hatch)
Adicionamos atalhos no `pyproject.toml` para as tarefas mais comuns:

- **Build e Reinstalação:**
  ```bash
  hatch run build-local
  ```
  *(Limpa builds anteriores, gera o .whl e instala via pip com --force-reinstall)*.

- **Limpeza:**
  ```bash
  hatch run clean
  ```

## Desenvolvimento da Documentação

A documentação é construída com [Starlight (Astro)](https://starlight.astro.build/).

### Pré-requisitos
- Node.js v22 (Recomendado o uso de [NVM](https://github.com/coreybutler/nvm-windows)).

### Rodar Docs Localmente
Você pode usar o atalho do Hatch para subir o servidor de desenvolvimento:

```bash
hatch run docs-serve
```

Este comando entra no diretório `docs-site/`, seleciona a versão correta do Node via `nvm use 22` e inicia o servidor Astro.

Para buildar a documentação (estáticos):
```bash
cd docs-site
npm run build
```

## Estrutura do Projeto

- `src/cli/`: Interface de linha de comando (Typer).
- `src/core/`: Lógica de gerenciamento de estado e compressão.
- `src/services/`: Integração com AWS S3 e configuração.
- `docs-site/`: Código-fonte da documentação Starlight.
