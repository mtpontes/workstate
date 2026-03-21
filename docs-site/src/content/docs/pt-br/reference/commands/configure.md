---
title: configure
description: Configura as credenciais AWS e o bucket S3 para o Workstate.
---

O comando `configure` é o primeiro passo para utilizar o Workstate. Ele estabelece a conexão com a sua infraestrutura AWS.

## Uso

```bash
workstate configure [OPTIONS]
```

## Opções

- `--global`: Define as configurações globalmente para o usuário atual (armazenado em `~/.workstate_config`).
- `--local`: Define as configurações apenas para o projeto atual (armazenado no diretório atual).

## Funcionamento

Ao executar o comando, o Workstate solicitará interativamente:
1. **AWS Access Key ID**: Sua chave de acesso IAM.
2. **AWS Secret Access Key**: Sua chave secreta IAM.
3. **Region**: A região AWS onde o bucket está localizado (ex: `us-east-1`).
4. **Bucket Name**: O nome do bucket S3 que será usado para armazenar os backups.

:::tip[Dica]
Se você já possui a [AWS CLI](https://aws.amazon.com/cli/) instalada e configurada, o Workstate tentará carregar as credenciais do seu perfil padrão se você deixar os campos em branco.
:::

## Exemplos

### Configuração Global
Útil para definir o bucket padrão que você usará em vários projetos.
```bash
workstate configure --global
```

### Configuração de Projeto Específico
Útil quando um projeto específico precisa usar um bucket ou credenciais diferentes.
```bash
workstate configure --local
```
