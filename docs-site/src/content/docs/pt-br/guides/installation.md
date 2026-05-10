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

## Verificando a Instalação

Após a instalação, execute o comando abaixo para verificar a versão:

```bash
workstate --version
```

### Validando a Configuração (Comando Doctor)

Para garantir que tudo esteja configurado corretamente — incluindo suas credenciais AWS e permissões do S3 — use o comando **doctor**:

```bash
workstate doctor
```

Este comando irá:
1. Verificar se o arquivo de configuração existe.
2. Validar suas chaves de acesso AWS.
3. Testar a conectividade e permissões no bucket S3 configurado.

Se tudo estiver verde, você está pronto para começar!
