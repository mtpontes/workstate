---
title: init
description: Inicializa o rastreamento do Workstate em um novo diretório.
---

O comando `init` prepara o diretório atual para ser gerenciado pelo Workstate, criando os arquivos de controle necessários.

## Uso

```bash
workstate init
```

## O que acontece?

Ao rodar o `init`, o Workstate cria uma subpasta oculta chamada `.workstate/`. Esta pasta contém:
- Metadados sobre o estado local.
- Cache de sincronização.
- Logs de operações.

:::important[Importante]
A pasta `.workstate/` **deve ser adicionada ao seu `.gitignore`**. O Workstate gerencia o que o Git não gerencia, e você não quer "versionar o versionador" dentro do Git.
:::

## Exemplos

```bash
# Navegue até o seu projeto
cd meu-projeto-novo

# Inicialize o Workstate
workstate init
```
