# 🐘 Configuração PostgreSQL no Render

Este guia explica como configurar e usar o PostgreSQL no Render para o Help Alphaclin.

## 📋 Pré-requisitos

1. ✅ Conta no Render.com
2. ✅ Projeto conectado ao GitHub
3. ✅ Banco PostgreSQL criado no Render

## 🗄️ Configuração do Banco PostgreSQL

### 1. Criar Banco no Render

1. Acesse o [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `help-alphaclin-db`
   - **Database**: `helpalphaclin`
   - **User**: `helpalphaclin`
   - **Plan**: `Free`
4. Clique em **"Create Database"**

### 2. Configurar Variáveis de Ambiente

O `render.yaml` já está configurado para usar o banco PostgreSQL. As variáveis importantes são:

```yaml
- key: DATABASE_URL
  fromDatabase:
    name: help-alphaclin-db
    property: connectionString
```

## 🚀 Deploy e Migração

### 1. Testar Conexão Localmente

```bash
# Testar se a conexão com PostgreSQL funciona
python test_postgres_connection.py
```

### 2. Migrar Dados

```bash
# Criar tabelas e dados iniciais no PostgreSQL
python migrate_to_postgres.py
```

### 3. Deploy no Render

```bash
# Commit e push para GitHub
git add .
git commit -m "Configuração PostgreSQL"
git push origin main
```

O Render fará deploy automático e conectará ao banco PostgreSQL.

## 🔐 Credenciais de Acesso

Após a migração, você terá acesso com:

- **URL**: `https://seu-app.onrender.com/admin/login`
- **Usuário**: `admin`
- **Senha**: `admin123`

## 📊 Verificação

### 1. Verificar Deploy

1. Acesse o dashboard do Render
2. Verifique se o deploy foi bem-sucedido
3. Acesse a URL do aplicativo

### 2. Verificar Banco

1. No dashboard do Render, vá para o banco PostgreSQL
2. Clique em **"Connect"** → **"External Database"**
3. Use as credenciais para conectar via pgAdmin ou outro cliente

### 3. Testar Funcionalidades

1. Acesse `/admin/login`
2. Faça login com as credenciais admin
3. Teste a criação de usuários
4. Teste a criação de exames

## 🔧 Solução de Problemas

### Erro de Conexão

Se houver erro de conexão:

1. Verifique se o banco PostgreSQL foi criado
2. Verifique se o `render.yaml` está correto
3. Verifique os logs do deploy no Render

### Erro de Módulo

Se houver erro de módulo faltando:

1. Verifique se `psycopg2-binary` está no `requirements.txt`
2. Faça novo deploy no Render

### Erro de Tabelas

Se as tabelas não existirem:

1. Execute o script de migração
2. Verifique se o banco está vazio
3. Verifique os logs de erro

## 📝 Logs Importantes

### Logs do Deploy

```bash
# No dashboard do Render
# Services → help-alphaclin → Logs
```

### Logs do Banco

```bash
# No dashboard do Render
# Databases → help-alphaclin-db → Logs
```

## 🔄 Rollback para SQLite

Se precisar voltar para SQLite:

1. Edite `render.yaml`:
   ```yaml
   - key: DATABASE_URL
     value: sqlite:///helpalphaclin.db
   ```

2. Remova a seção `databases`

3. Remova `psycopg2-binary` do `requirements.txt`

4. Faça novo deploy

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs no Render
2. Teste a conexão localmente
3. Verifique a documentação do Render
4. Consulte os logs de erro do aplicativo 