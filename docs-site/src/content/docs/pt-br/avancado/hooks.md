---
title: Hooks e Automação
description: Automatize seu workflow com scripts pós-restauração e integração nativa com o Git.
---

O Workstate permite automatizar tarefas repetitivas após a restauração do ambiente e integrar-se profundamente ao seu fluxo Git.

## scripts Pós-Restauração (`.workstate-hooks`)

Você pode criar um arquivo chamado `.workstate-hooks` na raiz do seu projeto para executar comandos automaticamente após cada `download` ou `sync` bem-sucedido.

### Exemplo de `.workstate-hooks`:

```bash
# Reinstala dependências se o ambiente mudou
pip install -r requirements.txt

# Limpa caches temporários
python manage.py clean_cache

# Notifica o time
echo "Ambiente Workstate restaurado com sucesso!"
```

:::warning[Permissões]
Em sistemas Linux/macOS, certifique-se de que o script tem permissão de execução (`chmod +x .workstate-hooks`). No Windows, ele é executado via PowerShell/CMD.
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
