<p align="center">
<pre>
██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗████████╗ █████╗ ████████╗███████╗
██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝
██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗   ██║   ███████║   ██║   █████╗  
██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║   ██║   ██╔══██║   ██║   ██╔══╝  
╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║   ██║   ██║  ██║   ██║   ███████╗
╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝
            🏠 Dev Environment ──▶ ☁️ AWS S3 ──▶ 🌍 Anywhere
</pre>
</p>

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
- **Interface Interativa**: CLI amigável com formatação rica e menus interativos
- **Restauração Seletiva**: Baixe estados sem descompactar ou restaure ambientes completos
- **Integração AWS S3**: Armazenamento seguro na nuvem para seus estados de desenvolvimento
- **Compartilhamento**: Compartilhe/importe estados utilizando URLs pré-assinadas temporárias do AWS S3
- **Templates Pré-construídos**: Vem com templates otimizados para ferramentas de desenvolvimento populares (Python, Node.js, Java, React, Angular, etc.)
- **Multiplataforma**: Funciona no Windows, macOS e Linux

## 📋 O Que É Capturado
Você é quem manda o que será capturado, mas a solução foi pensada para capturar tudo que o controle de versão tradicional ignora.

Exemplos:
- **Variáveis de Ambiente**: `.env`, `.env.local`, arquivos de configuração
- **Configurações de IDE**: `.vscode/`, `.idea/`, configurações de editores
- **Scripts locais**: Arquivos de teste, exemplos, scripts de seed, arquivos de contexto (llms) 
- **Bancos de Dados Locais**: Arquivos SQLite, dumps de bancos locais
- **Containers de Desenvolvimento**: Arquivos docker-compose, volumes de containers
- **Artefatos de Build**: Arquivos compilados, dependências
- **Configurações Locais**: Configurações específicas de ferramentas e preferências
- **Dados de Desenvolvimento**: Dados de teste, arquivos mock, assets locais

<details>
  <summary><h2>🔧 Instalação</h2></summary>

Se você for utilizar o `workstate.exe` ignore esse tópico.

### Pré-requisitos

- Python 3.8+
- Conta AWS com acesso ao S3
- pip

### Dependências

- **typer**: Framework para CLIs
- **rich**: Formatação de terminal
- **boto3**: SDK AWS para Python

### Arquivos de Configuração

- **`.workstateignore`**: Define arquivos/diretórios a serem incluídos/excluídos
- **`~/.workstate/config.json`**: Armazena credenciais AWS


### Instalar do Código-fonte (somente via Python)

```bash
git clone https://github.com/seuusuario/workstate.git
cd workstate
pip install -r requirements.txt
```

</details>


<details>
  <summary><h2>⚙️ Configuração AWS e Permissões</h2></summary>

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
</details>

<details>
  <summary><h2>🎯 Início Rápido</h2></summary>

### 1. Configurar Credenciais AWS

```bash
workstate configure
```

Isso solicitará:
- **AWS Access Key ID**: A chave de acesso do seu usuário IAM
- **AWS Secret Access Key**: A chave secreta do seu usuário IAM  
- **AWS Region**: A região onde seu bucket S3 está localizado (ex: `us-east-1`, `sa-east-1`)
- **S3 Bucket Name**: O nome do seu bucket S3

Configuração não-interativa alternativa:
```bash
workstate configure --access-key-id AKIA... --secret-access-key xxx --region us-east-1 --bucket-name meu-bucket --no-interactive
```

### 2. Inicializar Seu Projeto

```bash
# Inicializar com um template específico
workstate init --tool python

# Ou usar o template padrão
workstate init
```

Isso cria um arquivo `.workstateignore` otimizado para sua stack de desenvolvimento.

### 3. Verificar O Que Será Salvo

```bash
workstate status
```

Isso mostra todos os arquivos e diretórios que serão incluídos no snapshot do seu estado.

### 4. Salvar Seu Estado Atual

```bash
workstate save "meu-projeto-v1"
```
Isso compacta todos os arquivos mapeados (os mesmos listados no comando de status) em .zip e carrega para o AWS S3.

### 5. Listar Estados Disponíveis

```bash
workstate list
```
Lista todos os zips no AWS S3 do Workstate.

### 6. Restaurar um Estado
Baixa um estado e descompacta localmente. Caso haja repetição de arquivos, os arquivos repetidos do zip serão salvos 
como duplicatas seguindo o padrão (numero_da_duplicata), por exemplo: arquivo.txt, arquivo (1).txt, arquivo (2).txt.
```bash
workstate download
```
Caso queira apenas baixar o estado sem restaura-lo diretamente, use a opção `--download-only`, o zip será baixado e 
armazenado numa pasta `downloads` no diretório atual.
```bash
workstate download --download-only
```
</details>


<details>
  <summary><h2>📖 Referência de Comandos</h2></summary>

### Comandos Disponíveis

| Comando | Descrição | Argumentos | Opções |
|---------|-----------|------------|--------|
| `config` | Exibe configuração atual do Workstate | - | - |
| `configure` | Configura credenciais AWS | - | `--access-key-id, -a`, `--secret-access-key, -s`, `--region, -r`, `--bucket-name, -b`, `--interactive, -i` |
| `init` | Inicializa um novo projeto Workstate com arquivo `.workstateignore` | - | `--tool, -t`: Tipo de ferramenta (padrão: `generic`) |
| `status` | Mostra arquivos rastreados pelo Workstate | - | - |
| `save` | Salva o estado atual do projeto no AWS S3 | `state_name`: Nome único para o estado | - |
| `download` | Restaura um estado salvo do AWS S3 | - | `--only-download`: Apenas baixa sem extrair |
| `delete` | Exclui um estado salvo no AWS S3 | - | - |
| `list` | Lista todos os estados disponíveis no AWS S3 | - | - |
| `download-pre-signed` | Restaura um estado salvo do AWS S3 a partir de uma URL pré-assinada | `base_url`, `signature`, `expires`: Componentes da URL pré-assinada | `--no-extract`, `--output, -o` |
| `share` | Gera uma URL pré-assinada do AWS S3 para permitir o download de um estado sem necessidade de autenticação | - | `--expiration, -e`: Horas até a URL expirar (padrão: 24) |

### Detalhamento dos Comandos

### `config`
**Funcionalidade:** Exibe configuração AWS atual sem revelar informações sensíveis.

**Informações exibidas:**
- Access Key ID (mascarado)
- Região AWS
- Nome do bucket
- Status da configuração


### `configure`
**Funcionalidade:** Configura credenciais AWS (armazenadas em `~/.workstate/config.json`).

**Opções:**
| Opção | Abreviação | Descrição |
|-------|------------|-----------|
| `--access-key-id` | `-a` | AWS Access Key ID |
| `--secret-access-key` | `-s` | AWS Secret Access Key |
| `--region` | `-r` | Região AWS (ex: us-east-1, sa-east-1) |
| `--bucket-name` | `-b` | Nome do bucket S3 |
| `--interactive` | `-i` | Modo interativo (padrão: true) |

**Exemplos:**
```bash
# Modo interativo
workstate configure

# Modo não-interativo
workstate configure --access-key-id AKIA... --secret-access-key xxx --region us-east-1 --bucket-name my-bucket

# Modo misto
workstate configure --region sa-east-1 --bucket-name my-workstate-bucket
```

### `init`
**Funcionalidade:** Cria arquivo `.workstateignore` com template otimizado para a ferramenta especificada.

**Ferramentas válidas:** `python`, `node`, `java`, `go`, `generic`

**Exemplos:**
```bash
workstate init --tool python
workstate init -t node
workstate init  # usa template generic
```

### `status`
**Funcionalidade:** Visualiza arquivos que serão incluídos no próximo backup.

**Informações exibidas:**
- Caminhos de arquivos/diretórios
- Tamanhos individuais
- Total de arquivos e tamanho


### `save`
**Funcionalidade:** Comprime arquivos selecionados e faz upload para S3.

**Processo:**
1. Analisa `.workstateignore`
2. Cria ZIP temporário
3. Upload para S3
4. Remove arquivo temporário

**Exemplos:**
```bash
workstate save my-django-project
workstate save "projeto com espaços"
```

### `download`
**Funcionalidade:** Interface interativa para restaurar estados salvos.

**Processo:**
1. Lista estados disponíveis
2. Seleção interativa
3. Download do ZIP
4. Extração (opcional)
5. Limpeza de arquivos temporários

**Opções:**
| Opção | Descrição |
|-------|-----------|
| `--only-download` | Baixa apenas o ZIP sem extrair |


### `delete`
**Funcionalidade:** Exclui um estado salvo no AWS S3 de forma interativa.

**Processo:**
1. Lista estados disponíveis
2. Seleção interativa do estado a ser excluído
3. Confirmação da exclusão
4. Remoção do arquivo do S3


### `share`
**Funcionalidade:** Gera uma URL pré-assinada para compartilhar um estado do projeto sem necessidade de credenciais AWS.

**Processo:**
1. Lista estados disponíveis
2. Seleção interativa do estado
3. Geração da URL pré-assinada
4. Exibição da URL e instruções de uso

**Opções:**
| Opção | Abreviação | Descrição |
|-------|------------|-----------|
| `--expiration` | `-e` | Horas até a URL expirar (padrão: 24) |

**Exemplos:**
```bash
# URL válida por 24 horas (padrão)
workstate share

# URL válida por 48 horas
workstate share --expiration 48
workstate share -e 48
```


### `download-pre-signed`
**Funcionalidade:** Baixa e restaura um estado do projeto usando uma URL pré-assinada compartilhada.

**Argumentos:**
| Argumento | Descrição |
|-----------|-----------|
| `base_url` | URL base sem assinatura ou expiração |
| `signature` | Parte da assinatura da URL pré-assinada |
| `expires` | Timestamp de expiração da URL pré-assinada |

**Opções:**
| Opção | Abreviação | Descrição |
|-------|------------|-----------|
| `--no-extract` | - | Não extrai o arquivo ZIP após o download |
| `--output` | `-o` | Caminho personalizado para o arquivo baixado |

**Exemplos:**
```bash
# Download e extração automática
workstate download-pre-signed "https://bucket.s3.region.amazonaws.com/file.zip" "signature123" "1234567890"

# Apenas download sem extração
workstate download-pre-signed "https://bucket.s3.region.amazonaws.com/file.zip" "signature123" "1234567890" --no-extract

# Download para caminho específico
workstate download-pre-signed "https://bucket.s3.region.amazonaws.com/file.zip" "signature123" "1234567890" --output ./downloads/project.zip
```


### `list`
**Funcionalidade:** Lista estados salvos no S3 com informações detalhadas.

**Informações exibidas:**
- Nome do arquivo
- Tamanho
- Data de modificação
- Ordenação por data (mais recente primeiro)

</details>

<details>
  <summary><h2>📁 Arquivo .workstateignore</h2></summary>

O arquivo `.workstateignore` funciona de forma similar ao `.gitignore`, mas define o que **ignorado** no snapshot do seu estado.
A ideia é ignorar tudo que for referente ao repositório. Ele suporta:

- **Padrões glob**: `*.env`, `config/*`, `!.jar`
- **Inclusão de diretórios**: `/.vscode/`
- **Arquivos específicos**: `database.sqlite3`
- **Comentários**: Linhas começando com `#`

### Exemplo .workstateignore para Python:

```gitignore
# Ignora arquivos do repositório e mantém arquivos de desenvolvimento local de um projeto Python
src/
.ruff_cache/
__pycache__
venv
.venv
requirements.txt
pyproject.*
.git
.gitignore
LICENSE
README.md
main.py
logs/
```

</details>

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


<details>
  <summary><h2>🆘 Solução de Problemas</h2></summary>

### Problemas Comuns

**Erros de "Access Denied":**
- Verifique se suas credenciais AWS estão corretas
- Verifique se seu usuário IAM tem permissões S3
- Certifique-se de que o bucket S3 existe e está acessível

**"Arquivo .workstateignore não encontrado":**
- Execute `workstate init` para criar um
- Certifique-se de estar no diretório correto do projeto

**Tempos de upload longos:**
- Verifique seu arquivo `.workstateignore` para arquivos grandes desnecessários
- Considere a velocidade da sua conexão com a internet
- Use `workstate status` para revisar o que está sendo carregado

**Problemas de configuração:**
- Use `workstate config` para verificar suas configurações atuais
- Re-execute `workstate configure` para atualizar credenciais

</details>


## ⭐ Apoie o Projeto

Se este projeto foi útil para você ou para sua equipe, considere deixar uma **estrela** no repositório do GitHub! Isso ajuda outras pessoas a descobrirem o Workstate e me motiva a continuar melhorando a ferramenta.
