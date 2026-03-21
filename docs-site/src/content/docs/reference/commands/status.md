---
title: status
description: Exibe as diferenças entre o estado local e o último backup no S3.
---

O comando `status` permite que você veja o que mudou no seu ambiente desde a última vez que você salvou ou baixou um estado.

## Uso

```bash
workstate status
```

## Informações Exibidas

O comando realiza uma comparação rápida (usando hashes de arquivos) e reporta:
- **Arquivos Novos**: Arquivos locais que ainda não estão no S3.
- **Arquivos Modificados**: Arquivos que existem em ambos, mas têm conteúdos diferentes.
- **Arquivos Deletados**: Arquivos que estão no S3 mas foram removidos localmente.

## Exemplos

```bash
$ workstate status
🔍 Verificando estado do ambiente...

[MODIFICADO] .env
[NOVO]       .vscode/settings.json
[DELETADO]   temp_log.db

O ambiente está divergente do S3. Use 'workstate save' para subir as mudanças.
```
