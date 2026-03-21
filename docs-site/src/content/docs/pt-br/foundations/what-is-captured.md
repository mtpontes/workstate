---
title: O Que é Capturado
description: Entenda quais arquivos e configurações o Workstate preserva e restaura entre ambientes.
---

O Workstate foi projetado para capturar o "estado" do seu ambiente que normalmente não é versionado no Git. Isso inclui arquivos de configuração local, segredos de desenvolvimento e bases de dados voláteis.

## Categorias de Captura

### 1. Variáveis de Ambiente e Segredos
Arquivos que contêm chaves de API, tokens e configurações específicas da sua máquina.
- **Exemplos:** `.env`, `.env.local`, `.flaskenv`, `.netrc`.

### 2. Configurações de IDE e Ferramentas
Suas preferências de workspace e extensões recomendadas que facilitam o retorno ao trabalho.
- **Exemplos:** `.vscode/`, `.idea/`, `.settings/`, `.tool-versions`.

### 3. Bancos de Dados Local
Arquivos de dados usados para testes e desenvolvimento local que você não quer perder ao trocar de branch ou máquina.
- **Exemplos:** `development.sqlite3`, dumps de banco, diretórios de dados temporários.

### 4. Dependências Dinâmicas
Embora nem sempre recomendado para projetos gigantes, o Workstate pode capturar diretórios de bibliotecas se necessário.
- **Exemplos:** `.venv/` (Python), `vendor/` (PHP/Go), dependências compiladas localmente.

## Por que focar no que o Git ignora?

O Git é excelente para código-fonte, mas falha em preservar o estado operacional. O Workstate preenche essa lacuna garantindo que:
- Você não precise re-configurar sua AWS CLI ou venv toda vez.
- Seus segredos locais estejam seguros e versionados (se usado com `--encrypt`).
- O "contexto mental" do seu ambiente seja restaurado instantaneamente.

:::tip[Dica de Segurança]
Sempre use a flag `--encrypt` ao capturar arquivos que contenham segredos ou informações sensíveis.
:::
