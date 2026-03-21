---
title: sync
description: Sincroniza o ambiente com a última versão disponível de forma automática.
---

O `sync` é a versão "mãos livres" do `download`. Ele é ideal para fluxos de automação onde a interatividade não é possível ou desejada.

## Uso

```bash
workstate sync [OPTIONS]
```

## Como funciona?

O Workstate busca o backup mais recente que:
1. Corresponda à sua branch Git atual.
2. Se não houver nenhum na branch, busca o mais recente do projeto globalmente.

Diferente do `download`, o `sync` assume que você quer a versão mais nova e procederá automaticamente.

## Opções

- `--force`: Ignora avisos de sobrescrita e aplica o estado de forma agressiva.
- `--branch NAME`: Sincroniza com a versão mais recente de uma branch específica, ignorando a branch local.

## Exemplos

### Uso em Hooks de Checkout
Cole o seguinte script no seu hook de `post-checkout` do Git:
```bash
# Sincroniza o ambiente automaticamente ao trocar de branch
workstate sync
```

### Uso em CI/CD
```bash
workstate sync --force
```
