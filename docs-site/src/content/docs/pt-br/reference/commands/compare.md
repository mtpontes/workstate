---
title: compare
description: Compara detalhadamente o estado local com um backup no S3.
---

O `compare` vai além do `status`, permitindo que você compare seu ambiente local com *qualquer* backup específico armazenado no S3.

## Uso

```bash
workstate compare [ID_OU_NOME]
```

## O que é verificado?

- **Existência**: Arquivos presentes localmente vs S3.
- **Conteúdo**: Hashes de arquivos para detectar mudanças bit-a-bit.
- **Metadados**: Datas de modificação e tamanhos.

## Exemplos

```bash
# Compara local com um backup específico
workstate compare b2d1

# Compara local com o backup mais recente (interativo)
workstate compare
```

:::tip[Dica]
Use o `compare` antes de um `download --force` para ter certeza absoluta do que será perdido ou ganho na restauração.
:::
