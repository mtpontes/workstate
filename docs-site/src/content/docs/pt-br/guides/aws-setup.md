---
title: Configuração AWS
description: Passo-a-passo para configurar o bucket S3 e as permissões de acesso necessárias.
---

O Workstate utiliza o Amazon S3 para armazenar o estado do seu ambiente. Para isso, você precisa de um bucket e um usuário IAM configurados corretamente.

## 1. Criar um Bucket S3

1. Acesse o [Console AWS S3](https://s3.console.aws.io/).
2. Clique em **Create bucket**.
3. Escolha um nome descritivo (ex: `workstate-seu-projeto`).
4. Selecione uma região estável e de baixo custo, como `us-east-1` ou `us-east-2`.
5. Mantenha as configurações padrão (bloqueio de acesso público é recomendado).

## 2. Configurar Permissões (IAM)

O usuário que executará o comando `workstate` precisa de permissões para ler, listar e escrever no bucket.

### Política Recomendada (JSON)

Crie uma política IAM no console AWS e anexe-a ao seu usuário. Essas permissões permitem que o Workstate gerencie arquivos, metadados e tags (usados para rastreamento de branch e sistema).

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:GetObjectTagging",
                "s3:PutObjectTagging"
            ],
            "Resource": [
                "arn:aws:s3:::seu-bucket-workstate",
                "arn:aws:s3:::seu-bucket-workstate/*"
            ]
        }
    ]
}
```

:::warning[Importante]
Substitua `seu-bucket-workstate` pelo nome real do bucket que você criou.
:::

## 3. Credenciais Locais

O Workstate utilizará as credenciais configuradas na sua máquina (via `aws configure` ou variáveis de ambiente).

1. Execute `workstate configure` no seu projeto.
2. Informe o **Bucket name** e a **Região** quando solicitado.

:::tip[Dica]
Se você já configurou a AWS CLI antes, o Workstate detectará automaticamente seu perfil padrão.
:::

## 4. Resolução de Problemas com Doctor

Se você encontrar problemas com permissões ou conectividade, execute:

```bash
workstate doctor
```

O comando **doctor** fornece um relatório detalhado do seu ambiente local e da conectividade AWS, destacando exatamente o que pode estar mal configurado.
