---
title: list
description: Lista todos os backups disponíveis no bucket S3.
---

O comando `list` fornece uma visão clara do histórico de estados salvos para o seu projeto.

## Uso

```bash
workstate list [OPTIONS]
```

## Informações Exibidas na Tabela

- **ID**: Identificador curto (ex: `e4f1b2`). Útil para o comando `download`.
- **Name**: O nome amigável definido no `save`.
- **Created At**: Data e hora da criação.
- **Git Branch**: A branch onde o backup foi gerado.
- **Git Hash**: O commit específico daquele estado.
- **Protected**: Ícone de cadeado (🔒) se o backup estiver protegido contra deleção.

## Opções

- `--json`: Retorna a lista em formato JSON (ideal para automações).
- `--all-branches`: Mostra backups de todas as branches, não apenas da branch atual.

## Exemplos

```bash
$ workstate list
ID      NAME                    BRANCH  CREATED AT            PROTECTED
e4f1    setup-win              main     2024-03-10 10:00:00   🔒
b2d1    pos-sync-api           dev      2024-03-12 15:30:00   
```
