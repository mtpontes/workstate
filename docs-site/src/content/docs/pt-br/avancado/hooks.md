---
title: Hooks e Automação
description: Automatize seu workflow com scripts pós-restauração e integração nativa com o Git.
---

O Workstate permite automatizar tarefas repetitivas após a restauração do ambiente e integrar-se profundamente ao seu fluxo Git.

## Scripts Pós-Restauração (`.workstate-hooks`)

Você pode criar scripts personalizados para serem executados imediatamente após um `download` ou `sync`. Isso é ideal para:
- Reinstalar dependências (`npm install`, `pip install`).
- Reiniciar serviços locais.
- Configurar variáveis de ambiente.

Crie um script chamado `.workstate-hooks/post-sync.sh` na raiz do seu projeto.

:::warning[Importante]
Como o Workstate agora utiliza um modelo de **whitelist** (inclusão explícita), você deve garantir que a pasta `.workstate-hooks/` esteja listada no seu arquivo `.workstateinclude`. Caso contrário, os scripts não serão incluídos nos seus snapshots e não estarão disponíveis quando você restaurar o ambiente em outra máquina.
:::

## Integração com Git

O Workstate detecta automaticamente se o diretório atual é um repositório Git e captura o estado da branch e o hash do commit no momento do `save`.

### Vantagens:
- Ao listar backups (`list`), você verá exatamente de qual branch cada estado veio.
- O comando `sync` prioriza backups da sua branch atual.

## Git Hooks Nativos

O Workstate oferece uma maneira fácil de instalar lembretes de sincronização via Git Hooks nativos.

### Instalando Lembretes
Execute o comando abaixo para instalar hooks de `post-checkout` e `pre-push`:

```bash
workstate git-hook install
```

- **Post-checkout:** Lembra você de rodar `workstate sync` ao mudar de branch.
- **Pre-push:** Lembra você de rodar `workstate save` antes de enviar seu código para o repositório remoto.

Para remover os hooks:
```bash
workstate git-hook uninstall
```
