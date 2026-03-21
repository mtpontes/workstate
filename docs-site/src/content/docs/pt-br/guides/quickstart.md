---
title: Guia Rápido
description: Como usar o Workstate em 5 minutos.
---

Este guia ajudará você a configurar o Workstate e fazer seu primeiro backup em poucos minutos.

## 1. Configurar Credenciais AWS

O comando `configure` configura suas chaves AWS, região e o bucket S3:

```bash
workstate configure
```

## 2. Inicializar Projeto

Use o comando `init` para criar um arquivo `.workstateignore` padrão para seu projeto:

```bash
workstate init --tool python
```

## 3. Verificar Arquivos

Veja quais arquivos serão incluídos no snapshot:

```bash
workstate status
```

## 4. Salvar Estado

Dê um nome ao seu estado atual e envie-o para o S3:

```bash
workstate save "v1.0-meu-projeto"
```

## 5. Listar e Restaurar

Para ver os estados disponíveis e baixar um deles:

```bash
workstate list
workstate download
```
