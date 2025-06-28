# 🩺 Help Alpha - Sistema de Consulta de Exames

## 📋 Descrição

O **Help Alpha** é um sistema web desenvolvido com **Flask (Python)** e **Bulma (CSS)** que oferece aos pacientes uma plataforma simples, responsiva e profissional para consulta de informações sobre exames laboratoriais e de imagem.

## ✨ Funcionalidades

### 🎯 Público
- 🔍 **Busca de Exames**: Campo de busca por nome do exame
- 📋 **Lista Responsiva**: Visualização em cards de todos os exames disponíveis
- 📄 **Detalhes Completos**: Informações detalhadas de cada exame
- 📱 **Design Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- 🎨 **Interface Moderna**: Design profissional com Bulma CSS
- 🏥 **Informações das Unidades**: Contatos e horários atualizados

### 🔧 Administrativo (CRUD Completo)
- 🔐 **Sistema de Login**: Autenticação segura para administradores
- 📊 **Dashboard**: Estatísticas e visão geral do sistema
- ➕ **Adicionar Exames**: Formulário completo para cadastro de novos exames
- ✏️ **Editar Exames**: Modificação de exames existentes
- 🗑️ **Excluir Exames**: Remoção segura com confirmação
- 📋 **Gerenciar Exames**: Lista administrativa com todas as ações
- 👁️ **Preview em Tempo Real**: Visualização instantânea das alterações
- 📤 **Upload em Massa**: Importação de exames via arquivo Excel
- 📥 **Template Excel**: Download de modelo para preenchimento
- 🔄 **Processamento Inteligente**: Validação automática de dados Excel

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python + Flask
- **Frontend**: Bulma CSS Framework + Font Awesome
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF + WTForms
- **Dados**: JSON (estrutura simples e escalável)
- **Excel**: pandas + openpyxl + xlrd
- **Hospedagem**: Compatível com Render, Railway, Heroku, etc.

## 📦 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd helpAlpha
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python run.py
   ```

5. **Acesse no navegador**
   ```
   Site público: http://localhost:5000
   Painel admin: http://localhost:5000/admin/login
   ```

## 🔧 Configuração do Ambiente

### Ambiente Virtual Ativo
O projeto já possui um ambiente virtual configurado com todas as dependências instaladas:

```bash
# Ativar o ambiente virtual
venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
venv\Scripts\activate.bat  # Windows CMD
```

### Dependências Instaladas
- **Flask** (3.1.1) - Framework web
- **Flask-Login** (0.6.3) - Autenticação
- **Flask-WTF** (1.2.2) - Formulários
- **WTForms** (3.2.1) - Validação de formulários
- **pandas** (2.3.0) - Manipulação de dados
- **openpyxl** (3.1.5) - Arquivos Excel (.xlsx)
- **xlrd** (2.0.2) - Arquivos Excel (.xls)
- **numpy** (2.3.1) - Dependência do pandas

## 📁 Estrutura do Projeto

```
helpAlpha/
│
├── app/
│   ├── __init__.py          # Inicialização da aplicação Flask
│   ├── routes.py            # Rotas públicas
│   ├── admin_routes.py      # Rotas administrativas (CRUD + Upload)
│   ├── models.py            # Modelo de usuário
│   ├── forms.py             # Formulários (login, exames, upload)
│   ├── templates/           # Templates HTML
│   │   ├── base.html        # Template base público
│   │   ├── index.html       # Página inicial
│   │   ├── exame.html       # Página de detalhes
│   │   ├── 404.html         # Página de erro
│   │   └── admin/           # Templates administrativos
│   │       ├── base.html    # Template base admin
│   │       ├── login.html   # Página de login
│   │       ├── dashboard.html # Dashboard administrativo
│   │       ├── exames.html  # Lista de exames admin
│   │       ├── exame_form.html # Formulário de exames
│   │       └── upload_excel.html # Upload em massa
│   └── static/
│       └── css/
│           └── bulma.min.css # Framework CSS
│
├── data/
│   └── exames.json          # Base de dados dos exames
│
├── venv/                    # Ambiente virtual Python
├── config.py                # Configurações da aplicação
├── run.py                   # Arquivo principal para execução
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🗂️ Estrutura dos Dados

### Formato JSON
Os exames são armazenados no arquivo `data/exames.json` com a seguinte estrutura:

```json
[
  {
    "nome": "Nome do Exame",
    "descricao": "Descrição detalhada do exame",
    "preparo": "Instruções de preparo",
    "documentos": "Documentos necessários",
    "pos_exame": "Cuidados após o exame",
    "tempo": "Duração estimada"
  }
]
```

### Formato Excel para Upload
Para upload em massa, utilize o template Excel com as seguintes colunas:

| Coluna | Descrição | Obrigatório |
|--------|-----------|-------------|
| nome | Nome do exame | ✅ |
| descricao | Descrição detalhada | ✅ |
| preparo | Instruções de preparo | ✅ |
| documentos | Documentos necessários | ❌ |
| pos_exame | Cuidados pós-exame | ❌ |
| tempo | Duração estimada | ❌ |

## 🏥 Informações das Unidades

### Unidade Central
**Endereço:** Av. Calama 2215, São João Bosco  
**Telefones:** (69) 3223-0132, (69) 3223-0133, (69) 3223-0136

**Horário de Funcionamento:**
- Segunda a Sexta: das 6h30 às 21h30 (coleta de exames até às 16h)
- Sábado: das 6h30 às 17h* (coleta de exames até às 11:00)

**Vacinação:**
- Segunda a Sexta: 08h às 18h00
- Sábado: 8h às 12h00

### Zona Sul
**Endereço:** Av. Jatuarana 4184, Conceição  
**Telefones:** (69) 3227-9311, (69) 98129-0005 (WhatsApp)

**Horário de Funcionamento:**
- Segunda a Sexta: das 6h30 às 17h (coleta de exames 6h30 às 15h)
- Sábado: das 6h30 às 11h (coleta de exames das 6h30 às 9h)

**Vacinação:**
- Segunda a Sexta: Horário agendado
- Sábado: Horário agendado

## 🚀 Funcionalidades Principais

### Página Inicial (`/`)
- Campo de busca por nome do exame
- Lista responsiva de todos os exames
- Estatísticas rápidas
- Design mobile-first

### Página de Detalhes (`/exame/<nome>`)
- Informações completas do exame
- Preparo necessário
- Documentos exigidos
- Cuidados pós-exame
- Informações de contato das unidades

### API de Busca (`/api/search?q=<termo>`)
- Endpoint para busca via AJAX
- Retorna resultados em JSON
- Busca parcial por nome

### Painel Administrativo (`/admin/login`)
- **Login**: admin / admin123
- **Dashboard**: Estatísticas e visão geral
- **Gerenciar Exames**: Lista com ações CRUD
- **Adicionar Exame**: Formulário completo
- **Editar Exame**: Modificação com preview
- **Excluir Exame**: Confirmação segura
- **Upload Excel**: Importação em massa
- **Download Template**: Modelo Excel para preenchimento

## 🔐 Acesso Administrativo

### Credenciais Padrão
- **Usuário**: `admin`
- **Senha**: `admin123`

### URLs Administrativas
- **Login**: `/admin/login`
- **Dashboard**: `/admin`
- **Gerenciar Exames**: `/admin/exames`
- **Adicionar Exame**: `/admin/exames/add`
- **Editar Exame**: `/admin/exames/edit/<nome>`
- **Upload Excel**: `/admin/upload-excel`
- **Download Template**: `/admin/download-template`

## 📤 Sistema de Upload em Massa

### Funcionalidades
- **Upload de Arquivos Excel**: Suporte para .xlsx e .xls
- **Validação Automática**: Verificação de campos obrigatórios
- **Processamento Inteligente**: Tratamento de dados vazios
- **Feedback Visual**: Mensagens de sucesso e erro
- **Template Download**: Modelo Excel para preenchimento

### Como Usar
1. Acesse o painel administrativo
2. Vá para "Upload Excel"
3. Faça download do template
4. Preencha com os dados dos exames
5. Faça upload do arquivo
6. Confirme a importação

### Validações
- Campos obrigatórios: nome, descrição, preparo
- Dados vazios são preenchidos com valores padrão
- Verificação de duplicatas por nome
- Tratamento de caracteres especiais

## 🎨 Personalização

### Cores e Estilo
O sistema utiliza o framework Bulma CSS com personalizações:
- Gradiente azul no header
- Cards com sombras suaves
- Botões com hover effects
- Responsividade completa

### Componentes Customizados
- Cards de exames com hover
- Formulários com validação visual
- Sidebar administrativa
- Dashboard com estatísticas

## 🔧 Configurações

### Variáveis de Ambiente
```python
SECRET_KEY = 'dev-secret-key-help-alpha-2024'
DEBUG = True
WTF_CSRF_ENABLED = True
```

### Configurações de Upload
- **Tipos permitidos**: .xlsx, .xls
- **Tamanho máximo**: 16MB
- **Pasta de upload**: Temporária (processamento em memória)

## 🚀 Deploy

### Plataformas Suportadas
- **Render**: Compatível com Python
- **Railway**: Deploy automático
- **Heroku**: Configuração simples
- **VPS**: Qualquer servidor Linux

### Variáveis de Produção
```bash
SECRET_KEY=sua-chave-secreta-producao
DEBUG=False
FLASK_ENV=production
```

## 📊 Estatísticas do Sistema

### Métricas Disponíveis
- Total de exames cadastrados
- Exames laboratoriais vs. imagem
- Últimos exames adicionados
- Estatísticas de uso

### Dashboard Administrativo
- Visão geral em tempo real
- Gráficos de distribuição
- Ações rápidas
- Navegação intuitiva

## 🛡️ Segurança

### Medidas Implementadas
- Autenticação segura com Flask-Login
- Proteção CSRF em formulários
- Validação de entrada de dados
- Sanitização de arquivos Excel
- Sessões seguras

### Boas Práticas
- Senhas hasheadas com Werkzeug
- Validação de tipos de arquivo
- Tratamento de erros
- Logs de segurança

## 🔄 Manutenção

### Backup de Dados
- Arquivo `data/exames.json` deve ser backupado regularmente
- Versionamento com Git recomendado
- Backup automático em produção

### Atualizações
- Manter dependências atualizadas
- Verificar compatibilidade
- Testes antes de deploy

## 📞 Suporte

### Contatos
- **Desenvolvimento**: PageUp sistemas Oézios Normando
- **Clínica**: Unidades Central e Zona Sul

### Documentação Técnica
- Especificação completa: `documento spec.md.txt`
- Código comentado
- Estrutura modular

---

## ✅ Status do Projeto

- ✅ **Estrutura Base**: Implementada
- ✅ **Sistema CRUD**: Completo
- ✅ **Upload Excel**: Funcional
- ✅ **Interface Responsiva**: Finalizada
- ✅ **Autenticação**: Segura
- ✅ **Ambiente Virtual**: Configurado
- ✅ **Documentação**: Atualizada

**🎯 Sistema 100% Funcional e Pronto para Uso!**

---

**Desenvolvido por PageUp sistemas Oézios Normando** 