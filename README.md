# Workstate

**Ferramenta de Gerenciamento de Ambiente de Desenvolvimento Portátil**

Workstate é uma poderosa ferramenta CLI que permite aos desenvolvedores preservar e restaurar o estado completo de seus ambientes de desenvolvimento em diferentes máquinas. Diferentemente dos sistemas de controle de versão que focam no código-fonte, o Workstate captura tudo que torna seu ambiente de desenvolvimento único - configurações, bancos de dados locais, configurações de IDEs, variáveis de ambiente e muito mais.

## 🎯 Qual Problema Resolve?

Você já precisou:
- Continuar trabalhando em um projeto de uma máquina diferente com exatamente a mesma configuração?
- Preservar bancos de dados de desenvolvimento locais, arquivos de configuração e configurações de IDE?
- Compartilhar um ambiente de desenvolvimento completo com membros da equipe?
- Fazer backup do seu estado de desenvolvimento incluindo arquivos que não devem ir para o controle de versão?

O Workstate resolve esses problemas criando snapshots comprimidos do seu ambiente de desenvolvimento e armazenando-os de forma segura no AWS S3.

## 🚀 Principais Funcionalidades

- **Seleção Inteligente de Arquivos**: Usa arquivos `.workstateignore` (similar ao `.gitignore`) para definir o que deve ser incluído no snapshot do ambiente
- **Templates Pré-construídos**: Vem com templates otimizados para ferramentas de desenvolvimento populares (Python, Node.js, Java, React, Angular, etc.)
- **Integração AWS S3**: Armazenamento seguro na nuvem para seus estados de desenvolvimento
- **Interface Interativa**: CLI amigável com formatação rica e menus interativos
- **Multiplataforma**: Funciona no Windows, macOS e Linux
- **Restauração Seletiva**: Baixe estados sem descompactar ou restaure ambientes completos

## 📋 O Que É Capturado

O Workstate é projetado para capturar tudo que o controle de versão tradicional ignora:

- **Variáveis de Ambiente**: `.env`, `.env.local`, arquivos de configuração
- **Configurações de IDE**: `.vscode/`, `.idea/`, configurações de editores
- **Bancos de Dados Locais**: Arquivos SQLite, dumps de bancos locais
- **Containers de Desenvolvimento**: Configurações Docker, volumes
- **Artefatos de Build**: Arquivos compilados, dependências
- **Configurações Locais**: Configurações específicas de ferramentas e preferências
- **Dados de Desenvolvimento**: Dados de teste, arquivos mock, assets locais

## 🔧 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Conta AWS com acesso ao S3
- pip (instalador de pacotes Python)

### Instalar do Código-fonte

```bash
git clone https://github.com/seuusuario/workstate.git
cd workstate
pip install -r requirements.txt
```

## ⚙️ Configuração AWS e Permissões

### 1. Criar uma Conta AWS

Se você não tem uma conta AWS, crie uma em [aws.amazon.com](https://aws.amazon.com).

### 2. Criar um Usuário IAM

1. Vá para o Console AWS IAM
2. Crie um novo usuário para o Workstate
3. Anexe a política **AmazonS3FullAccess** ou crie uma política personalizada com as seguintes permissões:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::seu-bucket-workstate",
                "arn:aws:s3:::seu-bucket-workstate/*"
            ]
        }
    ]
}
```

### 3. Obter Chaves de Acesso

1. No console IAM, selecione seu usuário
2. Vá para a aba "Credenciais de segurança"
3. Crie chaves de acesso para CLI
4. **Importante**: Salve o Access Key ID e Secret Access Key de forma segura

### 4. Criar um Bucket S3

1. Vá para o Console AWS S3
2. Crie um novo bucket com um nome único (ex: `meu-bucket-workstate-12345`)
3. Escolha sua região preferida
4. Mantenha as configurações padrão de segurança

## 🎯 Início Rápido

### 1. Configurar Credenciais AWS

```bash
python main.py configure
```

Isso solicitará:
- **AWS Access Key ID**: A chave de acesso do seu usuário IAM
- **AWS Secret Access Key**: A chave secreta do seu usuário IAM  
- **AWS Region**: A região onde seu bucket S3 está localizado (ex: `us-east-1`, `sa-east-1`)
- **S3 Bucket Name**: O nome do seu bucket S3

Configuração não-interativa alternativa:
```bash
python main.py configure --access-key-id AKIA... --secret-access-key xxx --region us-east-1 --bucket-name meu-bucket --no-interactive
```

### 2. Inicializar Seu Projeto

```bash
# Inicializar com um template específico
python main.py init --tool python

# Ou usar o template padrão
python main.py init
```

Isso cria um arquivo `.workstateignore` otimizado para sua stack de desenvolvimento.

### 3. Verificar O Que Será Salvo

```bash
python main.py status
```

Isso mostra todos os arquivos e diretórios que serão incluídos no snapshot do seu estado.

### 4. Salvar Seu Estado Atual

```bash
python main.py save "meu-projeto-v1"
```
Isso compacta todos os arquivos mapeados (os mesmos listados no comando de status) em .zip e carrega para o AWS S3.

### 5. Listar Estados Disponíveis

```bash
python main.py list
```
Lista todos os zips no AWS S3 do Workstate.

### 6. Restaurar um Estado
Baixa um estado e descompacta localmente. Caso haja repetição de arquivos, os arquivos repetidos do zip serão salvos 
como duplicatas seguindo o padrão (numero_da_duplicata), por exemplo: arquivo.txt, arquivo (1).txt, arquivo (2).txt.
```bash
python main.py download
```
Caso queira apenas baixar o estado sem restaura-lo diretamente, use a opção `--download-only`, o zip será baixado e 
armazenado numa pasta `downloads` no diretório atual.
```bash
python main.py download --download-only
```


## 📖 Referência de Comandos

### `init` - Inicializar Projeto

Cria um arquivo `.workstateignore` com um template otimizado para sua ferramenta de desenvolvimento.

```bash
python main.py init [OPÇÕES]
```

**Opções:**
- `--tool, -t`: Tipo de ferramenta de desenvolvimento (padrão: `default`)
- **Ferramentas válidas**: `python`, `node`, `react`, `angular`, `java`, `c`, `c++`, `c#`, `php`, `default`

**Exemplos:**
```bash
python main.py init --tool python
python main.py init -t node
python main.py init  # usa template padrão
```

### `save` - Salvar Estado Atual

Cria um snapshot comprimido do seu ambiente de desenvolvimento e o carrega no S3.

```bash
python main.py save <NOME_DO_ESTADO>
```

**Argumentos:**
- `NOME_DO_ESTADO`: Identificador único para o snapshot do seu estado

**Exemplos:**
```bash
python main.py save "feature-autenticacao-usuario"
python main.py save "antes-refatoracao"
python main.py save "hotfix-producao"
```

### `list` - Listar Estados Disponíveis

Mostra todos os estados salvos no seu bucket S3 com detalhes.

```bash
python main.py list
```

**Saída inclui:**
- Nome do estado
- Tamanho do arquivo
- Data da última modificação
- Ordenado por data de modificação (mais recente primeiro)

### `download` - Restaurar Estado

Restauração interativa de um estado de desenvolvimento salvo.

```bash
python main.py download [OPÇÕES]
```

**Opções:**
- `--only-download`: Baixar o arquivo ZIP sem extraí-lo

**Exemplos:**
```bash
python main.py download                    # Restauração interativa
python main.py download --only-download    # Apenas baixar
```

### `status` - Mostrar Arquivos Rastreados

Exibe todos os arquivos e diretórios que serão incluídos na próxima operação de salvamento.

```bash
python main.py status
```

**Saída inclui:**
- Caminhos de arquivos/diretórios
- Tamanhos de arquivos individuais
- Contagem total e tamanho

### `configure` - Configuração AWS

Configurar ou atualizar credenciais AWS para o Workstate.

```bash
python main.py configure [OPÇÕES]
```

**Opções:**
- `--access-key-id, -a`: AWS Access Key ID
- `--secret-access-key, -s`: AWS Secret Access Key  
- `--region, -r`: Região AWS
- `--bucket-name, -b`: Nome do bucket S3
- `--interactive/--no-interactive, -i`: Usar modo interativo (padrão: true)

**Exemplos:**
```bash
# Modo interativo (padrão)
python main.py configure

# Modo não-interativo
python main.py configure --access-key-id AKIA... --secret-access-key xxx --region us-east-1 --bucket-name meu-bucket --no-interactive

# Modo misto (alguns argumentos fornecidos)
python main.py configure --region sa-east-1 --bucket-name meu-bucket-workstate
```

### `config` - Mostrar Configuração Atual

Exibe a configuração AWS atual (sem revelar informações sensíveis).

```bash
python main.py config
```

## 📁 Arquivo .workstateignore

O arquivo `.workstateignore` funciona de forma similar ao `.gitignore`, mas define o que **deve ser incluído** no snapshot do seu estado. Ele suporta:

- **Padrões glob**: `*.env`, `config/*`
- **Inclusão de diretórios**: `/.vscode/`
- **Arquivos específicos**: `database.sqlite3`
- **Comentários**: Linhas começando com `#`

### Exemplo .workstateignore para Python:

```gitignore
# Arquivos de ambiente
.env
.env.local
.env.production

# Configurações de IDE
/.vscode/
/.idea/

# Bancos de dados locais  
*.sqlite3
*.db

# Containers de desenvolvimento
docker-compose.override.yml
/.devcontainer/

# Configuração local
local_settings.py
config/local.json

# Dados de desenvolvimento
/fixtures/
/test_data/
```

## 🔐 Considerações de Segurança

### Armazenamento de Credenciais
- Credenciais são armazenadas localmente em `~/.workstate/config.json`
- Nunca commite este arquivo no controle de versão
- Use as melhores práticas do AWS IAM para gerenciamento de credenciais
- Considere usar políticas de rotação de credenciais da AWS

### Segurança de Dados
- Todos os dados são armazenados no seu bucket S3 privado
- Use políticas de bucket S3 para restringir acesso
- Considere habilitar criptografia em repouso no S3
- Revise regularmente os logs de acesso do S3

### Melhores Práticas
- Use contas AWS separadas para diferentes projetos
- Implemente políticas de acesso de menor privilégio
- Audite regularmente estados salvos e remova os desnecessários
- Seja consciente sobre dados sensíveis no seu ambiente de desenvolvimento

## 🌍 Variáveis de Ambiente

O Workstate suporta configuração via variáveis de ambiente como alternativa à configuração interativa:

```bash
# Credenciais AWS obrigatórias
export WORKSTATE_AWS_ACCESS_KEY_ID="sua-chave-de-acesso"
export WORKSTATE_AWS_SECRET_ACCESS_KEY="sua-chave-secreta"
export WORK_STATE_AWS_REGION="us-east-1"
export WORKSTATE_S3_BUCKET_NAME="nome-do-seu-bucket"

# Nomes alternativos de credenciais AWS (também suportados)
export AWS_ACCESS_KEY_ID="sua-chave-de-acesso"  
export AWS_SECRET_ACCESS_KEY="sua-chave-secreta"
```

## ⚠️ Notas Importantes

### O Que NÃO Incluir

Tenha cuidado para não incluir no seu `.workstateignore`:
- Arquivos binários grandes que mudam com frequência
- Arquivos temporários do sistema
- Arquivos específicos do SO (`.DS_Store`, `Thumbs.db`)
- Credenciais pessoais que devem permanecer específicas da máquina

### Limites de Tamanho de Arquivo

- O S3 tem um limite de objeto único de 5TB
- Considere as implicações de custo de armazenar estados de desenvolvimento grandes
- Limpe regularmente estados antigos que você não precisa mais

### Compatibilidade Multiplataforma

- Caminhos de arquivos são tratados usando `pathlib` do Python para compatibilidade multiplataforma
- Diferenças de terminação de linha são preservadas como estão
- Links simbólicos podem não funcionar entre diferentes sistemas operacionais

## 🆘 Solução de Problemas

### Problemas Comuns

**Erros de "Access Denied":**
- Verifique se suas credenciais AWS estão corretas
- Verifique se seu usuário IAM tem permissões S3
- Certifique-se de que o bucket S3 existe e está acessível

**"Arquivo .workstateignore não encontrado":**
- Execute `python main.py init` para criar um
- Certifique-se de estar no diretório correto do projeto

**Tempos de upload longos:**
- Verifique seu arquivo `.workstateignore` para arquivos grandes desnecessários
- Considere a velocidade da sua conexão com a internet
- Use `python main.py status` para revisar o que está sendo carregado

**Problemas de configuração:**
- Use `python main.py config` para verificar suas configurações atuais
- Re-execute `python main.py configure` para atualizar credenciais

---

## ⭐ Apoie o Projeto

Se este projeto foi útil para você ou para sua equipe, considere deixar uma **estrela** no repositório do GitHub! Isso ajuda outras pessoas a descobrirem o Workstate e me motiva a continuar melhorando a ferramenta.
