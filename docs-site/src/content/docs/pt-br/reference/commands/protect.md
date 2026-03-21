---
title: protect
description: Ativa ou remove a proteção contra deleção de um backup no S3.
---

O `protect` garante que backups importantes não sejam removidos acidentalmente por comandos de limpeza ou por você mesmo sem intenção.

## Uso

```bash
workstate protect [ID_OU_NOME] [OPTIONS]
```

## Como funciona?

Um backup protegido ganha um atributo especial no S3. O comando `delete` falhará se tentar remover um backup protegido.

## Opções

- `--remove`: Remove a proteção de um backup já protegido.
- `--all`: (Use com cautela) Protege todos os backups do projeto atual.

## Exemplos

### Proteger um Backup
```bash
workstate protect e4f1
```

### Remover Proteção
```bash
workstate protect e4f1 --remove
```

:::note[Nota]
Backups marcados com `--protect` durante o comando `save` já nascem protegidos e não precisam deste comando adicional.
:::
