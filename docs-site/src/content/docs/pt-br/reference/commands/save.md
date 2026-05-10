---
title: save
description: Captura e faz o upload do estado atual para o S3.
---

O comando `save` cria um "snapshot" (foto) do seu ambiente e o armazena com segurança na nuvem. Ele segue as regras de inclusão definidas no seu arquivo `.workstateinclude`.

## Uso

```bash
workstate save [NAME] [OPTIONS]
```

## Opções

- `-i, --include PATH`: Adiciona arquivos ou padrões extras apenas para este snapshot (inclusão ad-hoc).
- `--encrypt`: Criptografa o backup localmente antes do upload.
- `-p, --protect`: Marca o estado como "protegido" para evitar deleção acidental.
- `-m, --description TEXT`: Adiciona uma nota descritiva ou motivo ao backup.
- `--tag KEY=VALUE`: Aplica tags customizadas ao objeto no S3 para facilitar a filtragem.
- `--dry-run`: Simula o processo e lista os arquivos que seriam capturados, sem fazer o upload.

## Exemplos

```bash
# Salvamento simples usando as regras do .workstateinclude
workstate save "setup-base"

# Salvamento com inclusão ad-hoc (ex: um log específico)
workstate save "sessao-debug" --include "logs/error.log"

# Inclusão de múltiplos padrões
workstate save "estado-completo" -i "config/*.yaml" -i "data/*.csv"

# Salvamento criptografado e protegido com descrição
workstate save "ambiente-prod" --encrypt --protect -m "Sincronização inicial de produção"
```

:::tip[Dica de Pro]
Use `workstate status` antes de salvar para verificar exatamente quais arquivos estão sendo selecionados pela sua whitelist.
:::

:::caution[Importante]
Se você usar `--encrypt`, será solicitada uma senha. **Nós não armazenamos suas senhas.** Se você perdê-la, o estado não poderá ser restaurado.
:::
