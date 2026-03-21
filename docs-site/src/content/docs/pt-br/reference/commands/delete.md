---
title: delete
description: Remove permanentemente backups do seu bucket S3.
---

O comando `delete` permite manter seu bucket limpo, removendo estados que não são mais necessários.

## Uso

```bash
workstate delete [ID_OU_NOME] [OPTIONS]
```

## Regras de Segurança

1. **Proteção**: O Workstate impedirá a deleção de qualquer backup marcado como protegido (🔒). Você deve remover a proteção primeiro com o comando `protect --remove`.
2. **Confirmação**: Por padrão, o comando solicitará uma confirmação manual.

## Opções

- `--force`: Remove o backup sem solicitar confirmação (respeita a proteção).
- `--older-than DAYS`: Deleta todos os backups não-protegidos anteriores à quantidade de dias especificada.

## Exemplos

### Deletar um Backup Específico
```bash
workstate delete e4f1
```

### Limpeza de Backups Antigos
```bash
# Deleta backups com mais de 30 dias que não estejam protegidos
workstate delete --older-than 30
```

:::caution[Cuidado]
A operação de deleção é irreversível no S3 (a menos que você tenha versionamento de bucket ativado na AWS).
:::
