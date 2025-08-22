# 🩺 Help Alphaclin - Sistema de Consulta de Exames

## 📋 Sobre o Sistema

O **Help Alphaclin** é um sistema web completo desenvolvido com **Flask (Python)** e **Bulma (CSS)** que oferece uma plataforma moderna, segura e responsiva para consulta de informações sobre exames laboratoriais, de imagem e vacinas.

## ✨ Principais Funcionalidades

### 🔍 Para Usuários Finais
- **Busca Inteligente**: Interface intuitiva com filtros por categoria
- **Informações Detalhadas**: Preparo, documentos, duração e cuidados pós-exame
- **Design Responsivo**: Otimizado para mobile, tablet e desktop
- **SEO Otimizado**: Sitemap, robots.txt e meta tags completas
- **Avisos em Tempo Real**: Banner animado com informações importantes

### 👨‍💼 Para Administradores
- **Sistema de Usuários**: 3 níveis de acesso (Admin, Editor, Viewer)
- **Gestão Completa**: CRUD de exames, unidades e avisos
- **Upload em Massa**: Importação via Excel com validação
- **Dashboard Avançado**: Estatísticas e relatórios em tempo real
- **Configurações Flexíveis**: Personalização completa do site
- **Logs e Auditoria**: Rastreamento de atividades

## 🛠️ Stack Tecnológica

- **Backend**: Flask 3.0.0 + SQLAlchemy
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Frontend**: Bulma CSS + FontAwesome + JavaScript
- **Segurança**: Rate limiting, CSP, headers de segurança
- **Deploy**: Render.com com Gunicorn
- **Processamento**: Pandas para Excel, Markdown2 para formatação

## 🚀 Deploy Rápido (Render.com)

1. **Fork o repositório** no GitHub
2. **Conecte ao Render.com** e selecione o repositório
3. **Deploy automático** - O `render.yaml` configura tudo
4. **Acesse o sistema** em `https://seu-app.onrender.com`

**Credenciais padrão**: `admin` / `admin123`

## 🔧 Desenvolvimento Local

### 📋 Pré-requisitos
- Python 3.8+
- Git
- PostgreSQL (opcional, para produção)

### ⚡ Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/pgup-sistemas/helpAlpha.git
cd helpAlpha

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure banco de dados
python migrate_data.py

# Execute o sistema
python run.py
```

**Acesse**: http://localhost:5000

## 🔐 Sistema de Usuários

### 👥 Níveis de Acesso

| Nível | Usuário | Senha | Permissões |
|-------|---------|-------|------------|
| 👑 **Admin** | `admin` | `admin123` | Acesso total, gerenciar usuários |
| ✏️ **Editor** | `editor` | `editor123` | Editar conteúdo, upload massa |
| 👁️ **Viewer** | `viewer` | `viewer123` | Apenas visualização |

### 🛡️ Segurança Implementada
- Rate limiting por endpoint
- Headers de segurança (CSP, HSTS, etc.)
- Sanitização de entrada de dados
- Autenticação segura com Flask-Login
- Tokens de redefinição de senha

## 📁 Estrutura do Projeto

```
helpAlpha/
├── app/
│   ├── __init__.py          # Configuração da aplicação
│   ├── models.py            # Modelos do banco de dados
│   ├── routes.py            # Rotas públicas
│   ├── admin_routes.py      # Rotas administrativas
│   ├── forms.py             # Formulários WTF
│   ├── security.py          # Headers e sanitização
│   ├── rate_limiting.py     # Controle de requisições
│   ├── extensions.py        # Extensões Flask
│   ├── templates/           # Templates Jinja2
│   └── static/              # CSS, JS, imagens
├── config.py                # Configurações do Flask
├── run.py                   # Arquivo de execução
├── requirements.txt         # Dependências Python
├── render.yaml             # Deploy automático
├── gunicorn.conf.py        # Servidor de produção
└── Procfile                # Comando de inicialização
```

## 🔧 Configuração e Variáveis

### Variáveis de Ambiente Principais

```bash
# Essenciais
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_segura
DATABASE_URL=postgresql://user:pass@host:port/db

# Admin padrão
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@helpalphaclin.com
ADMIN_PASSWORD=senha_gerada_automaticamente
```

## 📊 Funcionalidades Completas

### 🌐 Frontend Público
- ✅ Busca inteligente com filtros
- ✅ Visualização detalhada de exames
- ✅ Design responsivo (mobile-first)
- ✅ SEO otimizado (sitemap, robots.txt)
- ✅ Avisos em tempo real (banner animado)

### 🔧 Painel Administrativo
- ✅ Dashboard com estatísticas
- ✅ CRUD completo (exames, unidades, avisos)
- ✅ Upload em massa via Excel
- ✅ Sistema de usuários (3 níveis)
- ✅ Configurações personalizáveis
- ✅ Logs e auditoria

### 🛡️ Segurança Implementada
- ✅ Rate limiting por endpoint
- ✅ Headers de segurança (CSP, HSTS)
- ✅ Sanitização de entrada
- ✅ Autenticação segura
- ✅ Tokens de redefinição de senha

## 🏥 Informações das Unidades

### Unidade Central
- **Endereço**: Av. Calama 2215, São João Bosco
- **Telefones**: (69) 3223-0132, (69) 3223-0133, (69) 3223-0136
- **Horários**: Seg-Sex 6h30-21h30, Sáb 6h30-17h
- **Vacinação**: Seg-Sex 8h-18h, Sáb 8h-12h

### Zona Sul
- **Endereço**: Av. Jatuarana 4184, Conceição
- **Telefones**: (69) 3227-9311, (69) 98129-0005 (WhatsApp)
- **Horários**: Seg-Sex 6h30-17h, Sáb 6h30-11h
- **Vacinação**: Horário agendado

## 🚀 Performance e Monitoramento

- **Servidor**: Gunicorn com workers otimizados
- **Cache**: Headers configurados para performance
- **Logs**: Sistema completo de auditoria
- **Métricas**: Estatísticas de uso em tempo real
- **Backup**: Configuração automática no PostgreSQL

## 🤝 Contribuição e Suporte

### Desenvolvimento
- **Empresa**: PageUp Sistemas
- **Desenvolvedor**: Oézios Normando
- **GitHub**: [@pgup-sistemas](https://github.com/pgup-sistemas)

### Suporte Técnico
- **Email**: suporte@helpalphaclin.com
- **WhatsApp**: (69) 98129-0005
- **Telefone**: (69) 3223-0132

---

## ✅ Status Final

**🎯 Sistema 100% Funcional e Pronto para Produção!**

- ✅ **Deploy**: Configurado para Render.com
- ✅ **Banco**: PostgreSQL em produção
- ✅ **Segurança**: Implementação completa
- ✅ **Interface**: Responsiva e moderna
- ✅ **Funcionalidades**: Todas implementadas
- ✅ **Documentação**: Completa e atualizada

**Versão**: v1.0.0 | **Desenvolvido por**: PageUp Sistemas | **Janeiro 2025** 