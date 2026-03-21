---
title: save
description: Captura e faz o upload do estado atual para o S3.
---

O `save` é o comando principal para preservar seu trabalho. Ele empacota, opcionalmente criptografa e envia seu ambiente para a nuvem.

## Uso

```bash
workstate save [OPTIONS] [NAME]
```

## Argumentos

- `NAME`: (Opcional) Um nome amigável para o backup (ex: `pos-setup-inicial`). Se não fornecido, o Workstate gera um nome baseado na data e hora.

## Opções

- `--encrypt`: Ativa a criptografia AES no lado do cliente. Você será solicitado a criar ou digitar uma senha.
- `--dry-run`: Simula a operação. Mostra exatamente quais arquivos seriam incluídos no pacote sem fazer upload.
- `--protect`: Marca o backup como protegido. Ele não poderá ser deletado automaticamente por políticas de retenção ou pelo comando `delete` (a menos que a proteção seja removida).
- `--retention DAYS`: (Avançado) Define uma data de expiração personalizada para este backup específico.

## Exemplos

### Salvamento Simples
```bash
workstate save
```

### Salvamento com Nome e Criptografia
```bash
workstate save --encrypt "snapshot-ambiente-estavel"
```

### Apenas Verificar o que será salvo
```bash
workstate save --dry-run
```

:::caution[Segurança]
Ao usar `--encrypt`, **não perca sua senha**. O Workstate não armazena sua senha de criptografia e os arquivos não poderão ser recuperados sem ela.
:::
