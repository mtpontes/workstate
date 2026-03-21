---
title: inspect
description: Exibe metadados detalhados de um backup ou arquivo específico no S3.
---

O comando `inspect` é uma ferramenta de depuração e inspeção que permite olhar para "dentro" de um backup sem precisar baixá-lo.

## Uso

```bash
workstate inspect [ID_OU_NOME] [OPTIONS]
```

## Informações Extraídas

- **ID e Hash**: Identificadores únicos do backup.
- **Autor e Máquina**: Qual usuário e máquina geraram o backup.
- **Árvore de Arquivos**: Lista todos os arquivos contidos no backup e seus tamanhos individuais.
- **Configurações**: Se está criptografado e qual versão do Workstate foi usada.

## Opções

- `--files`: Lista apenas a árvore de arquivos contida no backup.
- `--meta`: Exibe apenas os metadados de sistema.

## Exemplos

```bash
# Inspeciona um backup por ID
workstate inspect e4f1

# Inspeciona um backup pelo nome
workstate inspect "pos-setup-inicial"
```

:::tip[Dica]
Use `inspect --files` para verificar se um arquivo específico que você precisa está contido em um backup antes de baixá-lo.
:::
