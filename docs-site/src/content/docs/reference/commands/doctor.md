---
title: doctor
description: Verifica a saúde e a integridade da configuração do Workstate.
---

O comando `doctor` é o seu primeiro recurso de suporte. Ele executa uma bateria de testes para garantir que o Workstate possa se comunicar com a AWS e que o ambiente local está saudável.

## Uso

```bash
workstate doctor
```

## Testes Realizados

1. **Credenciais AWS**: Verifica se as chaves de acesso são válidas e têm permissão.
2. **Conectividade S3**: Testa a conexão com o bucket configurado.
3. **IAM Permissions**: Simula operações básicas para garantir que o usuário tem as permissões de leitura/escrita.
4. **Local Config**: Valida o arquivo `.workstate` e a integridade do cache local.
5. **Node/Python Runtime**: Verifica se as dependências do sistema estão presentes.

## Exemplos

```bash
$ workstate doctor
🩺 Diagnóstico do Workstate

[OK] Credenciais AWS encontradas (default profile)
[OK] Conexão com bucket 'workstate-prod' estabelecida
[OK] Permissões de escrita e leitura validadas
[OK] Cache local íntegro

Tudo saudável! Workstate pronto para uso.
```

:::tip[Dica]
Se o `doctor` falhar, ele fornecerá sugestões de comandos para corrigir o problema, como rodar o `workstate configure` novamente.
:::
