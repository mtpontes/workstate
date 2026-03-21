---
title: Instalação
description: Como instalar o Workstate no seu ambiente.
---

O Workstate pode ser instalado via `pip` ou baixando os binários pré-compilados (apenas Windows por enquanto).

## Pré-requisitos

- Python 3.8+
- Conta AWS com acesso ao S3
- pip (gerenciador de pacotes do Python)

## Instalação via pip (Recomendado)

Esta é a maneira mais fácil de manter o Workstate atualizado:

```bash
pip install workstate
```

## Instalação via Código Fonte

Se você preferir rodar a versão de desenvolvimento:

```bash
git clone https://github.com/mtpontes/workstate.git
cd workstate
pip install -r requirements.txt
```

## Configuração da AWS

Para que o Workstate funcione, você precisará de um bucket S3 e um usuário IAM com as permissões corretas.

### Permissões Necessárias (IAM)

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
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::seu-bucket-workstate",
                "arn:aws:s3:::seu-bucket-workstate/*"
            ]
        }
    ]
}
```
