# 🚀 Deploy no Render - Help Alphaclin

## 📋 Pré-requisitos

- Conta no Render.com
- Repositório Git configurado
- Python 3.11.9 (especificado no runtime.txt)

## 🔧 Configuração

### 1. Arquivos de Configuração

O projeto já inclui todos os arquivos necessários para deploy no Render:

- `render.yaml` - Configuração do serviço
- `runtime.txt` - Versão do Python (3.11.9)
- `requirements.txt` - Dependências
- `Procfile` - Comando de inicialização
- `gunicorn.conf.py` - Configuração do servidor

### 2. Variáveis de Ambiente

O Render configurará automaticamente:

- `FLASK_ENV=production`
- `SECRET_KEY` (gerada automaticamente)
- `DATABASE_URL` (do banco PostgreSQL)
- `LOG_LEVEL=WARNING`

### 3. Banco de Dados

O `render.yaml` configura automaticamente um banco PostgreSQL gratuito.

## 🚀 Deploy

### Opção 1: Deploy Automático (Recomendado)

1. **Conecte seu repositório** no Render
2. **Selecione o repositório** `helpAlpha`
3. **Render detectará** o `render.yaml` automaticamente
4. **Clique em "Create New Service"**
5. **Aguarde** o build e deploy

### Opção 2: Deploy Manual

1. **Crie um novo Web Service**
2. **Conecte o repositório**
3. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app --config gunicorn.conf.py`
   - **Python Version:** 3.11.9

## 🔍 Troubleshooting

### Erro de Build

Se houver erro de build:

1. **Verifique a versão do Python** (deve ser 3.11.9)
2. **Atualize as dependências** se necessário
3. **Verifique os logs** de build no Render

### Erro de Runtime

Se houver erro de runtime:

1. **Verifique as variáveis de ambiente**
2. **Confirme a conexão com o banco**
3. **Verifique os logs** de aplicação

### Problemas Comuns

#### Pandas não instala
- **Solução:** Use Python 3.11.9 (não 3.13)
- **Alternativa:** Remova pandas se não for essencial

#### Banco de dados não conecta
- **Verifique:** `DATABASE_URL` está configurada
- **Confirme:** Banco PostgreSQL está ativo

#### Aplicação não inicia
- **Verifique:** `SECRET_KEY` está definida
- **Confirme:** `FLASK_ENV=production`

## 📊 Monitoramento

### Logs

- **Build Logs:** Durante o deploy
- **Runtime Logs:** Durante a execução
- **Access Logs:** Requisições HTTP

### Métricas

- **Uptime:** Disponibilidade do serviço
- **Response Time:** Tempo de resposta
- **Error Rate:** Taxa de erros

## 🔒 Segurança

### Configurações Automáticas

- ✅ HTTPS/SSL automático
- ✅ Headers de segurança
- ✅ Rate limiting
- ✅ CSRF protection

### Recomendações

- 🔐 Altere senhas padrão após deploy
- 📝 Configure backup do banco
- 🔍 Monitore logs regularmente
- 🔄 Mantenha dependências atualizadas

## 📞 Suporte

Se houver problemas:

1. **Verifique os logs** no Render Dashboard
2. **Consulte** a documentação do Render
3. **Entre em contato** com o suporte técnico

---

**Render.com** - Plataforma de deploy recomendada para o Help Alphaclin 