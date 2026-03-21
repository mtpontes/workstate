---
title: Visão Geral de Comandos
description: Lista completa de comandos disponíveis no Workstate e suas funções básicas.
---

O Workstate possui uma interface CLI intuitiva. Abaixo está o resumo de todos os comandos para referência rápida.

| Comando | Descrição |
| :--- | :--- |
| `configure` | Configura as credenciais AWS e o bucket S3 global ou local. |
| `init` | Inicializa o Workstate no diretório atual (cria o `.workstate`). |
| `status` | Verifica o estado atual do ambiente e arquivos modificados. |
| `save` | Sincroniza e salva o estado local no S3. |
| `list` | Lista todos os backups disponíveis no bucket. |
| `download` | Restaura um estado específico (interativo por padrão). |
| `sync` | Sincroniza o ambiente com a versão mais recente do S3 (ideal para CI/CD). |
| `compare` | Compara o estado local com uma versão no S3. |
| `inspect` | Mostra detalhes de um backup específico no S3. |
| `protect` | Ativa a proteção contra deleção de um backup. |
| `delete` | Remove backups do S3 (respeita a proteção). |
| `git-hook` | Gerencia a integração com Git Hooks (`install`/`uninstall`). |
| `doctor` | Verifica a saúde das configurações e conexões AWS. |
| `update` | Verifica e instala atualizações do Workstate. |
| `version` | Exibe a versão instalada. |

:::tip[Dica]
Você pode ver os argumentos específicos de qualquer comando usando a flag `--help`.  
Exemplo: `workstate save --help`
:::
