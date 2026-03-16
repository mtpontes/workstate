# FEATURE_TRACKER - Workstate

## 9. Gestão Avançada de Metadados

### [x] [9.1] Alertas de Compatibilidade de Ambiente

#### Contexto
→ Leia `docs/feature_context/ALERTAS_COMPATIBILIDADE.md` antes de implementar.

#### Arquivos
- [MODIFY] `src/services/state_service.py` — Adicionar captura de SO no metadado System durante o save — Risco: baixo
- [MODIFY] `src/commands/download_command.py` — Validar metadado System e emitir aviso se houver divergência — Risco: médio
- [MODIFY] `src/utils/system_info.py` — Criar utilitário para extrair informações do ambiente — Risco: baixo

#### Validação
- Executar `workstate save` em um SO (ex: Windows) e `workstate download` em outro (ex: Linux) e verificar se o alerta é exibido.

### [x] [9.2] Filtros Inteligentes na Listagem

#### Contexto
→ Leia `docs/feature_context/FILTROS_LISTAGEM.md` antes de implementar.

#### Arquivos
- [MODIFY] `src/commands/list_command.py` — Adicionar novos argumentos de filtro — Risco: baixo
- [MODIFY] `src/services/state_service.py` — Implementar lógica de filtragem nos metadados retornados pelo S3 — Risco: médio
- [MODIFY] `src/views/list_view.py` — Adaptar a exibição para refletir os filtros aplicados — Risco: baixo

#### Validação
- Executar `workstate list --system Windows` e verificar se apenas backups de Windows aparecem.

### [x] [9.3] Análise de Custos e Ciclo de Vida por Tag

#### Contexto
→ Leia `docs/feature_context/ANALISE_CUSTOS_TAGS.md` antes de implementar.

#### Arquivos
- [MODIFY] `src/services/state_service.py` — Garantir que tags de S3 (Project, Branch) sejam aplicadas corretamente — Risco: médio
- [NEW] `src/commands/report_command.py` — Criar comando para gerar relatório de consumo — Risco: médio
- [NEW] `src/services/report_service.py` — Implementar agregação de dados por tag — Risco: alto

#### Validação
- Executar `workstate report --tags Project,Branch` e validar os valores de tamanho agregado.

### [ ] [9.4] Rastreabilidade de Checkpoints

#### Contexto
→ Leia `docs/feature_context/RASTREABILIDADE_CHECKPOINTS.md` antes de implementar.

#### Arquivos
- [MODIFY] `src/services/state_service.py` — Incluir branch e commit hash nos metadados do S3 — Risco: baixo
- [MODIFY] `src/commands/download_command.py` — Exibir informações de branch/commit após a restauração — Risco: baixo
- [MODIFY] `src/utils/git_utils.py` — Melhorar extração de dados do git local — Risco: baixo

#### Validação
- Salvar um estado em uma branch específica e validar se o download exibe corretamente "Restauração baseada na branch [nome] (commit [hash])".
