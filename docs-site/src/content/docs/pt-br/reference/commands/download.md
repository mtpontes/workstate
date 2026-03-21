---
title: download
description: Restaura um estado específico do S3 para o diretório local.
---

O comando `download` é o principal meio de restaurar seu ambiente em uma nova máquina ou branch.

## Uso

```bash
workstate download [OPTIONS] [ID_OU_NOME]
```

## Funcionamento

Se você não fornecer um `ID_OU_NOME`, o Workstate entrará no **Modo Interativo**, exibindo uma lista dos backups mais recentes da sua branch atual para você escolher.

### Regra de Sobrescrita
O Workstate protege seu trabalho local. Se você tentar baixar um estado que contenha arquivos diferentes dos locais, ele perguntará se você deseja:
1. Sobrescrever tudo.
2. Manter arquivos locais mais novos.
3. Abortar a operação.

## Opções

- `--force`: Sobrescreve arquivos locais sem perguntar. **Use com cautela.**
- `--id ID`: Especifica diretamente o ID do backup.

## Exemplos

### Seleção Interativa
```bash
workstate download
```

### Download por ID
```bash
workstate download e4f1
```

### Download por Nome
```bash
workstate download "ambiente-estavel"
```

:::warning[Criptografia]
Se o backup foi salvo com `--encrypt`, o Workstate pedirá a senha durante o download.
:::
