# 🚀 Guia de Deploy - Help Alphaclin

## Deploy no Render.com

### Pré-requisitos

1. **Conta no Render.com**: [render.com](https://render.com)
2. **Repositório GitHub**: Código deve estar no GitHub
3. **Configurações**: Arquivos de deploy já configurados

### Passo a Passo

#### 1. Preparação do Repositório

Verifique se os seguintes arquivos estão presentes:

```bash
helpAlpha/
├── render.yaml          # ✅ Configuração do Render
├── gunicorn.conf.py     # ✅ Configuração do Gunicorn
├── Procfile            # ✅ Comando de inicialização
├── requirements.txt    # ✅ Dependências Python
├── run.py             # ✅ Arquivo de execução
└── VERSION            # ✅ Versão do sistema
```

#### 2. Deploy no Render.com

1. **Acesse o Render.com**
   - Faça login em [render.com](https://render.com)

2. **Crie um novo Blueprint**
   - Clique em "New +"
   - Selecione "Blueprint"

3. **Conecte o Repositório**
   - Conecte sua conta GitHub
   - Selecione o repositório `help-alphaclin`

4. **Configure o Deploy**
   - O Render detectará automaticamente o `render.yaml`
   - Verifique as configurações:
     - **Nome**: `help-alphaclin`
     - **Plano**: `Free`
     - **Região**: Mais próxima do Brasil

5. **Inicie o Deploy**
   - Clique em "Apply"
   - Aguarde o build (5-10 minutos)

#### 3. Configuração Pós-Deploy

Após o deploy ser concluído:

1. **Acesse o Painel Administrativo**
   ```
   https://seu-app.onrender.com/admin/login
   ```

2. **Credenciais Padrão**
   - **Usuário**: `admin`
   - **Senha**: Verificar logs do Render (gerada automaticamente)

3. **Configure o Google Maps**
   - Acesse `/admin/configuracoes`
   - Adicione a URL do iframe do Google Maps

4. **Importe os Dados**
   - Use o upload em massa para importar exames
   - Ou adicione manualmente

### Configurações Importantes

#### Variáveis de Ambiente (Automáticas)

O `render.yaml` configura automaticamente:

```yaml
envVars:
  - key: FLASK_ENV
    value: production
  - key: SECRET_KEY
    generateValue: true
  - key: DATABASE_URL
    fromDatabase:
      name: help-alphaclin-db
      property: connectionString
  - key: ADMIN_USERNAME
    value: admin
  - key: ADMIN_EMAIL
    value: admin@helpalphaclin.com
  - key: ADMIN_PASSWORD
    generateValue: true
```

#### Banco de Dados PostgreSQL

- **Configurado automaticamente** pelo Render
- **Backup automático** diário
- **SSL habilitado** por padrão

### Monitoramento

#### Logs

Acesse os logs no painel do Render:
- **Build Logs**: Durante o deploy
- **Runtime Logs**: Durante a execução

#### Métricas

- **Uptime**: Monitoramento automático
- **Performance**: Métricas de resposta
- **Erros**: Alertas automáticos

### Troubleshooting

#### Problemas Comuns

1. **Build Falha**
   ```bash
   # Verificar requirements.txt
   # Verificar sintaxe Python
   # Verificar dependências
   ```

2. **Aplicação Não Inicia**
   ```bash
   # Verificar logs do Gunicorn
   # Verificar variáveis de ambiente
   # Verificar configuração do banco
   ```

3. **Erro de Banco de Dados**
   ```bash
   # Verificar DATABASE_URL
   # Verificar conectividade
   # Verificar permissões
   ```

#### Comandos Úteis

```bash
# Verificar status
curl https://seu-app.onrender.com/health

# Verificar logs
# Acesse o painel do Render > Logs

# Reiniciar aplicação
# Render > Dashboard > Seu App > Manual Deploy
```

### Segurança

#### Configurações Automáticas

- **HTTPS**: Habilitado automaticamente
- **Headers de Segurança**: Configurados
- **Rate Limiting**: Ativo
- **CSP**: Content Security Policy

#### Recomendações

1. **Altere a senha do admin** após o primeiro login
2. **Configure Google Maps** corretamente
3. **Monitore os logs** regularmente
4. **Faça backup** dos dados importantes

### Performance

#### Otimizações Automáticas

- **Gunicorn**: Configurado para produção
- **Workers**: Otimizados para CPU
- **Timeout**: Configurado adequadamente
- **Keep-alive**: Habilitado

#### Monitoramento

- **Response Time**: < 500ms
- **Uptime**: > 99.9%
- **Memory**: Otimizado
- **CPU**: Eficiente

### Backup e Recuperação

#### Banco de Dados

- **Backup automático**: Diário
- **Retenção**: 7 dias
- **Recuperação**: Via painel do Render

#### Código

- **Versionamento**: Git
- **Rollback**: Via Render
- **Deploy**: Automático

### Suporte

#### Render.com

- **Documentação**: [docs.render.com](https://docs.render.com)
- **Status**: [status.render.com](https://status.render.com)
- **Suporte**: Via chat/email

#### PageUp Sistemas

- **Email**: pageupsistemas@gmail.com
- **WhatsApp**: (69) 99388-2222
- **GitHub**: [@pgup-sistemas](https://github.com/pgup-sistemas)

---

**Última atualização**: Janeiro 2025  
**Versão do Deploy**: v1.0.0 