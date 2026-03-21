---
title: update
description: Verifica se há novas versões do Workstate e realiza a atualização.
---

O comando `update` garante que você esteja sempre utilizando a versão mais recente do Workstate, com todas as correções de bugs e novas funcionalidades.

## Uso

```bash
workstate update [OPTIONS]
```

## Como funciona?

O Workstate se conecta ao repositório oficial (PyPI ou GitHub) para comparar a sua versão instalada com a última versão estável disponível.

## Opções

- `--check-only`: Apenas verifica se há atualizações, sem baixar nada.
- `--force`: Força a reinstalação da versão atual (útil para reparos).

## Exemplos

```bash
# Verifica e instala atualizações
workstate update

# Apenas avisa se há algo novo
workstate update --check-only
```

:::note[Nota]
Se você instalou o Workstate via `pip`, o comando `update` executará internamente o `pip install --upgrade workstate`.
:::
