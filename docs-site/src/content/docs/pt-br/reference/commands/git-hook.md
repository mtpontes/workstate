---
title: git-hook
description: Instala ou remove scripts de integração nativa com o Git.
---

O `git-hook` estende o poder do Workstate para dentro do fluxo nativo do seu repositório Git, automatizando lembretes de sincronização.

## Uso

```bash
workstate git-hook [COMMAND]
```

## Sub-comandos

### `install`
Instala os hooks de `post-checkout` e `pre-push` no diretório `.git/hooks/` do seu projeto.
- **post-checkout**: Dispara ao mudar de branch, sugerindo um `workstate sync`.
- **pre-push**: Dispara ao tentar enviar código, sugerindo um `workstate save`.

### `uninstall`
Remove permanentemente os hooks instalados pelo Workstate. Não afeta hooks que você criou manualmente.

## Funcionamento

Os hooks do Workstate são inteligentes:
- Eles não bloqueiam sua operação Git se o Workstate falhar ou não estiver configurado.
- Eles são executados rapidamente para não atrasar seu workflow.

## Exemplos

```bash
# Ativa a integração no seu projeto
workstate git-hook install

# Desativa a integração
workstate git-hook uninstall
```
