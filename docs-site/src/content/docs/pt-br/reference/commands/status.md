---
title: status
description: Veja quais arquivos estão sendo rastreados e incluídos para snapshots.
---

O comando `status` lista todos os arquivos no seu projeto que coincidem com as regras no seu `.workstateinclude` (whitelist) ou `.workstateignore` (blacklist legado). É a melhor forma de verificar o que será enviado antes de rodar o `save`.

## Uso

```bash
workstate status
```

## Informações Exibidas

- **Arquivos Incluídos**: Uma lista de todos os arquivos que o Workstate está rastreando no momento.
- **Tamanho Total**: A soma do tamanho de todos os arquivos rastreados.
- **Contexto do Projeto**: Informações sobre o nome do projeto atual e o bucket AWS configurado.

## Exemplos

```bash
$ workstate status
🔍 Analisando estado do projeto...

Projeto atual: workstate
Bucket S3: meu-bucket-backups

Arquivos rastreados (Modo Whitelist):
- .workstateinclude
- src/main.py
- src/services/file_service.py
- README.md

Total: 4 arquivos (145.2 KB)
```
