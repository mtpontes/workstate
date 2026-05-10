---
title: Guia Rápido
description: Comece a usar o Workstate em menos de 5 minutos.
---

O Workstate ajuda você a capturar e restaurar seu ambiente de desenvolvimento. Este guia cobre o fluxo essencial: Configuração, Inicialização, Verificação e Salvamento.

## 1. Configurar AWS
Antes de tudo, você precisa dizer ao Workstate onde armazenar seus snapshots:

```bash
workstate configure
```
*Você será solicitado a inserir sua Access Key, Secret Key, Região AWS e o nome do bucket S3.*

## 2. Inicializar o Projeto
Vá até o diretório raiz do seu projeto e inicialize-o:

```bash
workstate init
```

Isso cria um arquivo `.workstateinclude` com padrões minimalistas. Diferente de um "ignore", **apenas os arquivos listados aqui serão capturados.**

## 3. Verificar o que será capturado
Como usamos uma abordagem de inclusão explícita (whitelist), é uma boa prática verificar o que o Workstate está "vendo":

```bash
workstate status
```
*Este comando lista todos os arquivos que serão incluídos no próximo snapshot.*

## 4. Salvar seu Estado
Capture seu ambiente atual e faça o upload para o S3:

```bash
workstate save "v1-config-inicial"
```

## 5. Listar e Restaurar
Para ver seus estados armazenados e baixar um deles:

```bash
workstate list
workstate download
```

## Próximos Passos
- Entenda melhor o que é [O que é capturado](/workstate/pt-br/foundations/what-is-captured/) (Inclusão vs Exclusão).
- Explore a [Referência de Comandos](/workstate/pt-br/reference/commands/save/) para flags avançadas como `--include` e `--encrypt`.
