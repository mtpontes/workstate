---
title: O que é capturado
description: Entenda como o Workstate utiliza o sistema de inclusão explícita para gerenciar seu estado.
---

O Workstate segue um **modelo de inclusão estrita** (whitelist). Em vez de tentar adivinhar o que deve ser ignorado, ele captura apenas o que você autoriza explicitamente. Essa abordagem garante que seus backups sejam leves, seguros e previsíveis.

## O Arquivo `.workstateinclude`

O coração do motor de seleção do Workstate é o arquivo `.workstateinclude`. Ele funciona de forma similar ao `.gitignore`, mas ao contrário: **apenas os caminhos e padrões listados aqui serão capturados.**

### Inclusões Padrão
Ao executar `workstate init`, um arquivo `.workstateinclude` minimalista é criado com padrões sensatos:

- `.workstateinclude` (sempre rastreia sua própria configuração)
- `src/` (código-fonte principal)
- `pyproject.toml` / `package.json` (definições de dependências)
- `README.md`

### Por que usar Whitelist?
1. **Segurança**: Você nunca faz backup acidental de logs sensíveis ou binários que não deveriam ser compartilhados.
2. **Performance**: Snapshots menores significam uploads e downloads mais rápidos.
3. **Controle**: Você sabe exatamente o que compõe o seu "estado de trabalho".

## Auto-Inclusão de Arquivos Críticos

Mesmo que não estejam listados explicitamente, o Workstate garante que os seguintes itens sejam tratados corretamente:
- **Configuração**: O próprio arquivo `.workstateinclude` é sempre incluído.
- **Metadados**: Metadados internos usados para restauração são gerenciados automaticamente.

## Suporte Legado (Blacklist)

Se você tem um projeto existente usando `.workstateignore`, o Workstate ainda o respeitará como fallback. No entanto, **novos projetos sempre utilizam o `.workstateinclude`**, e recomendamos fortemente a migração de projetos legados para o modelo de inclusão.

:::caution[Atenção]
Se ambos os arquivos existirem, o `.workstateinclude` terá precedência e o arquivo de ignore será ignorado.
:::
