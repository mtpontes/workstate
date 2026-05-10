---
title: list
description: Lista os estados de ambiente disponíveis no S3.
---

O comando `list` exibe os estados armazenados no seu bucket S3. Por padrão, ele realiza um **scan global**, mostrando estados de todos os projetos presentes no bucket.

## Uso

```bash
workstate list [OPTIONS]
```

## Opções

- `-p, --project`: Filtra a lista para exibir apenas estados pertencentes ao projeto atual.
- `-s, --system NOME`: Filtra pelo sistema operacional (ex: `Windows`, `Linux`).
- `-b, --branch NOME`: Filtra pelo nome da branch Git.
- `-o, --older-than DURACAO`: Mostra estados mais antigos que uma duração (ex: `30d` para 30 dias, `1y` para 1 ano).
- `-i, --interactive`: Ativa o modo interativo para navegar e selecionar estados usando busca por proximidade (fuzzy search).
- `--no-cache`: Ignora o cache local de metadados e busca a lista atualizada diretamente do S3.

## Exemplos

```bash
# Lista todos os estados de todos os projetos (Padrão)
workstate list

# Mostra apenas estados do projeto atual
workstate list --project

# Busca estados de uma branch específica
workstate list --branch feature/login

# Navegação interativa
workstate list -i

# Limpeza: encontrar estados com mais de 6 meses
workstate list --older-than 6m
```

:::note[Nota]
O Workstate utiliza um cache local para acelerar a listagem. Se você suspeitar que a lista está desatualizada, use a flag `--no-cache`.
:::
