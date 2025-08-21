# 🩺 Help Alphaclin - Sistema de Consulta de Exames

## 📋 Descrição

O **Help Alphaclin** é um sistema web desenvolvido com **Flask (Python)** e **Bulma (CSS)** que oferece aos pacientes uma plataforma simples, responsiva e profissional para consulta de informações sobre exames laboratoriais e de imagem.

## 🚀 Funcionalidades

### Para Usuários
- **Busca de Exames**: Interface de busca intuitiva
- **Detalhes Completos**: Informações sobre preparo, documentos necessários, duração e cuidados pós-exame
- **Paginação**: Navegação eficiente com paginação
- **Design Responsivo**: Interface adaptável para diferentes dispositivos

### Para Administradores
- **Autenticação Segura**: Sistema de login com tokens de redefinição de senha
- **Gestão de Exames**: CRUD completo de exames
- **Upload em Massa**: Importação de exames via arquivo Excel
- **Dashboard**: Estatísticas e visão geral do sistema
- **Paginação Administrativa**: Gerenciamento eficiente de grandes volumes de dados

## 🛠️ Tecnologias

- **Backend**: Flask 3.0.0
- **Banco de Dados**: SQLite com SQLAlchemy
- **Autenticação**: Flask-Login
- **Frontend**: Bulma CSS Framework
- **Processamento**: Pandas para arquivos Excel
- **Formulários**: WTForms com validação

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd helpalphaclinclinclin
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   python migrate_data.py
   ```

5. **Execute a aplicação**
   ```bash
   python run.py
   ```

6. **Acesse a aplicação**
   - Frontend: http://localhost:5000
   - Admin: http://localhost:5000/admin/login

## 🔐 Sistema de Usuários e Credenciais

### 👥 Níveis de Acesso

O sistema implementa **3 níveis de usuário** com permissões específicas:

| Nível | Usuário | Senha | Acesso |
|-------|---------|-------|--------|
| 👑 **Admin** | `admin` | `admin123` | **Total** |
| ✏️ **Editor** | `editor` | `editor123` | **Edição** |
| 👁️ **Viewer** | `viewer` | `viewer123` | **Visualização** |

### 📋 Permissões por Nível

**👑 Administrador**: Acesso total a todas as funcionalidades, incluindo gerenciamento de usuários e configurações do sistema.

**✏️ Editor**: Pode editar conteúdo (exames, unidades, avisos) e fazer upload em massa, mas não pode deletar conteúdo ou gerenciar usuários.

**👁️ Visualizador**: Apenas visualização de estatísticas e relatórios, sem permissão para editar conteúdo.

### 🔧 Gerenciamento de Usuários

1. **Acesse** `/admin/usuarios` (apenas administradores)
2. **Crie** novos usuários com níveis apropriados
3. **Edite** usuários existentes
4. **Monitore** atividade dos usuários

**⚠️ Importante**: Altere as credenciais padrão após o primeiro acesso!

### 📖 Documentação Completa

- **Documentação detalhada**: `DOCUMENTACAO_USUARIOS.md`
- **Resumo executivo**: `RESUMO_PERMISSOES.md`

## 🔑 Redefinição de Senha

O sistema inclui funcionalidade de redefinição de senha por token:

1. Acesse `/admin/reset-password`
2. Digite seu nome de usuário
3. Um token será gerado e exibido na tela
4. Use o token para acessar a página de redefinição
5. O token é válido por 24 horas e pode ser usado apenas uma vez

## 📊 Estrutura do Projeto

```
helpalphaclinclinclin/
├── app/
│   ├── __init__.py          # Configuração da aplicação
│   ├── models.py            # Modelos do banco de dados
│   ├── forms.py             # Formulários
│   ├── routes.py            # Rotas públicas
│   ├── admin_routes.py      # Rotas administrativas
│   ├── static/              # Arquivos estáticos
│   ├── templates/           # Templates HTML
│   ├── uploads/             # Arquivos de upload
│   └── downloads/           # Arquivos para download
├── data/
│   └── exames.json          # Dados iniciais (migrados para SQLite)
├── config.py                # Configurações
├── requirements.txt         # Dependências
├── run.py                   # Script de execução
├── migrate_data.py          # Script de migração
└── helpalphaclinclinclin.db             # Banco de dados SQLite (criado automaticamente)
```

## 📝 Uso

### Acessando como Usuário
1. Acesse a página inicial
2. Use a barra de busca para encontrar exames
3. Clique em "Ver Detalhes" para informações completas
4. Navegue pelas páginas usando a paginação

### Acessando como Administrador
1. Acesse `/admin/login`
2. Use as credenciais padrão ou suas credenciais personalizadas
3. Gerencie exames através do dashboard
4. Use o upload em massa para adicionar múltiplos exames

### Upload em Massa
1. Baixe o template Excel em `/admin/upload-excel`
2. Preencha com seus dados seguindo o formato
3. Faça upload do arquivo
4. O sistema processará e importará os exames automaticamente

## 🔧 Configuração

### Variáveis de Ambiente
- `SECRET_KEY`: Chave secreta para sessões (padrão: dev-secret-key-change-in-production)
- `DATABASE_URL`: URL do banco de dados (padrão: sqlite:///helpalphaclinclinclinclin.db)

### Configurações de Paginação
- `EXAMES_PER_PAGE`: Exames por página no frontend (padrão: 9)
- `ADMIN_EXAMES_PER_PAGE`: Exames por página no admin (padrão: 15)

## 🚀 Deploy

### Desenvolvimento
```bash
python run.py
```

### Produção

Para configurar o ambiente de produção:

1. **Execute o configurador de produção**
```bash
python setup_production.py
```

2. **Configure as variáveis de ambiente**
- Edite o arquivo `.env` gerado
- Configure `DATABASE_URL` para seu banco de produção
- Ajuste outras configurações conforme necessário

3. **Verifique os requisitos**
```bash
python setup_production.py check
```

4. **Configure o servidor web**
- Use Gunicorn, uWSGI ou similar
- Configure proxy reverso (Nginx/Apache)
- Configure SSL/TLS

### Configuração de Produção

#### Variáveis de Ambiente Críticas

| Variável | Descrição | Obrigatória |
|----------|-----------|-------------|
| `FLASK_ENV` | Ambiente (production) | ✅ |
| `SECRET_KEY` | Chave secreta da aplicação | ✅ |
| `DATABASE_URL` | URL do banco de dados | ✅ |
| `LOG_LEVEL` | Nível de log (WARNING/ERROR) | ❌ |

#### Exemplo de Configuração

```bash
# .env para produção
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
DATABASE_URL=postgresql://user:password@localhost/helpalphaclin
LOG_LEVEL=WARNING
```

#### Servidor Web (Gunicorn)

```bash
# Instalar Gunicorn
pip install gunicorn

# Executar em produção
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

#### Nginx (Proxy Reverso)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Segurança em Produção

- ✅ Use HTTPS/SSL
- ✅ Configure firewall
- ✅ Mantenha dependências atualizadas
- ✅ Faça backup regular do banco
- ✅ Monitore logs de erro
- ✅ Use variáveis de ambiente seguras
- ❌ Nunca use credenciais padrão
- ❌ Não exponha arquivos sensíveis

## 📈 Funcionalidades Futuras

- [ ] Sistema de logs de acesso
- [ ] Backup automático do banco de dados
- [ ] API REST completa
- [ ] Sistema de notificações
- [ ] Relatórios avançados
- [ ] Integração com sistemas externos

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Para suporte, entre em contato através dos canais oficiais ou abra uma issue no repositório.

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
SECRET_KEY = 'dev-secret-key-help-alphaclin-2024'
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

# 🚀 Características

- **Consulta de Exames**: Busca por nome, categoria e descrição
- **Informações Detalhadas**: Preparo, documentos, duração e cuidados pós-exame
- **Markdown**: Suporte completo para formatação rica nos textos
- **Painel Administrativo**: Gerenciamento completo de exames
- **Upload em Massa**: Importação via Excel
- **Responsivo**: Design adaptável para mobile e desktop
- **SEO Otimizado**: Meta tags, sitemap e robots.txt
- **Segurança**: Rate limiting, CSP, headers de segurança
- **Google Maps**: Integração com mapas para localização

## 🛠️ Tecnologias

- **Backend**: Flask 3.0.0
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Frontend**: Bulma CSS + FontAwesome
- **Markdown**: markdown2
- **Segurança**: Flask-Limiter, CSP
- **Produção**: Gunicorn

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL (para produção)
- Git

## 🚀 Deploy no Render.com

### 1. Preparação do Repositório

1. Clone o repositório:
```bash
git clone https://github.com/pgup-sistemas/help-alphaclin.git
cd help-alphaclin
```

2. Verifique se os arquivos de deploy estão presentes:
- `render.yaml` - Configuração do Render
- `gunicorn.conf.py` - Configuração do Gunicorn
- `Procfile` - Comando de inicialização
- `requirements.txt` - Dependências Python

### 2. Deploy no Render.com

1. Acesse [render.com](https://render.com) e faça login
2. Clique em "New +" e selecione "Blueprint"
3. Conecte seu repositório GitHub
4. O Render detectará automaticamente o `render.yaml`
5. Clique em "Apply" para iniciar o deploy

### 3. Configuração Pós-Deploy

Após o deploy, acesse o painel administrativo:
```
https://seu-app.onrender.com/admin/login
```

**Credenciais padrão:**
- Usuário: `admin`
- Senha: Gerada automaticamente (verificar logs do Render)

### 4. Configurações Importantes

1. **Google Maps**: Configure no painel administrativo
2. **Banco de Dados**: PostgreSQL configurado automaticamente
3. **Variáveis de Ambiente**: Configuradas no `render.yaml`

## 🏃‍♂️ Desenvolvimento Local

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/pgup-sistemas/help-alphaclin.git
cd help-alphaclin

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados

```bash
# Configure as variáveis de ambiente
cp env_template.txt .env
# Edite o arquivo .env com suas configurações

# Inicialize o banco de dados
flask db init
flask db migrate
flask db upgrade
```

### 3. Executando o Projeto

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute o servidor de desenvolvimento
python run.py
```

Acesse: http://localhost:5000

## 📁 Estrutura do Projeto

```
helpAlpha/
├── app/
│   ├── __init__.py          # Configuração da aplicação
│   ├── models.py            # Modelos do banco de dados
│   ├── routes.py            # Rotas públicas
│   ├── admin_routes.py      # Rotas administrativas
│   ├── forms.py             # Formulários
│   ├── security.py          # Configurações de segurança
│   ├── rate_limiting.py     # Rate limiting
│   ├── extensions.py        # Extensões Flask
│   ├── templates/           # Templates HTML
│   └── static/              # Arquivos estáticos
├── config.py                # Configurações
├── run.py                   # Arquivo de execução
├── requirements.txt         # Dependências
├── render.yaml             # Configuração Render.com
├── gunicorn.conf.py        # Configuração Gunicorn
├── Procfile                # Comando de inicialização
└── VERSION                 # Versão do sistema
```

## 🔧 Configurações

### Variáveis de Ambiente

```bash
# Configurações básicas
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta
DATABASE_URL=postgresql://user:pass@host:port/db

# Configurações do admin
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@exemplo.com
ADMIN_PASSWORD=senha_segura

# Google Maps (opcional)
GOOGLE_MAPS_API_KEY=sua_chave_api
```

### Configurações de Segurança

- **Rate Limiting**: Implementado para todas as rotas
- **CSP**: Content Security Policy configurado
- **Headers de Segurança**: HSTS, X-Frame-Options, etc.
- **Sanitização**: Entrada de dados sanitizada

## 📊 Funcionalidades

### Públicas
- ✅ Busca de exames
- ✅ Visualização detalhada
- ✅ Filtros por categoria
- ✅ Paginação
- ✅ SEO otimizado
- ✅ Sitemap XML
- ✅ Robots.txt

### Administrativas
- ✅ Login seguro
- ✅ CRUD de exames
- ✅ Upload em massa (Excel)
- ✅ Estatísticas
- ✅ Configurações do site
- ✅ Logs de acesso

## 🔒 Segurança

- **Rate Limiting**: Proteção contra ataques de força bruta
- **CSP**: Content Security Policy
- **Headers de Segurança**: Proteção contra ataques comuns
- **Sanitização**: Entrada de dados limpa
- **Autenticação**: Sistema de login seguro

## 📱 Responsividade

- Design mobile-first
- Adaptável para tablets e desktop
- Interface otimizada para touch
- Carregamento rápido

## 🚀 Performance

- **Gunicorn**: Servidor WSGI otimizado
- **Rate Limiting**: Controle de requisições
- **Caching**: Headers de cache configurados
- **Compressão**: Gzip habilitado

## 📈 Monitoramento

- Logs de acesso
- Estatísticas de busca
- Monitoramento de performance
- Alertas de erro

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é desenvolvido pela **PageUp Sistemas** para o **Help Alphaclin**.

## 👨‍💻 Desenvolvimento

**PageUp Sistemas** - Oézios Normando
- GitHub: [@pgup-sistemas](https://github.com/pgup-sistemas)
- Email: contato@pageupsistemas.com

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Email: suporte@helpalphaclin.com
- WhatsApp: (69) 98129-0005

---

**Versão**: v1.0.0  
**Última atualização**: Janeiro 2025  
**Desenvolvido por**: PageUp Sistemas 