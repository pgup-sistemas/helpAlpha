# 📋 Documentação do Sistema de Usuários - Help Alphaclin

## 🎯 Visão Geral

O sistema Help Alphaclin implementa um controle de acesso baseado em **3 níveis de usuário** com permissões específicas para cada função. O sistema é **simples, prático e seguro**, permitindo que diferentes pessoas tenham acesso adequado às funcionalidades do sistema.

---

## 👥 Níveis de Usuário

### 1. 👑 **Administrador (Admin)**
**Descrição**: Acesso total ao sistema, incluindo gerenciamento de usuários e configurações avançadas.

**Permissões**:
- ✅ **Editar conteúdo**: Exames, unidades, avisos
- ✅ **Deletar conteúdo**: Exames, unidades, avisos
- ✅ **Gerenciar usuários**: Criar, editar, deletar usuários
- ✅ **Visualizar estatísticas**: Relatórios e logs
- ✅ **Configurações do sistema**: Todas as configurações
- ✅ **Upload em massa**: Importar exames via Excel
- ✅ **Acesso total**: Todas as funcionalidades

**Usuário padrão**: `admin` / `admin123`

---

### 2. ✏️ **Editor**
**Descrição**: Pode editar conteúdo do sistema, mas não pode gerenciar usuários ou deletar conteúdo.

**Permissões**:
- ✅ **Editar conteúdo**: Exames, unidades, avisos
- ❌ **Deletar conteúdo**: Não pode deletar
- ❌ **Gerenciar usuários**: Não pode gerenciar usuários
- ✅ **Visualizar estatísticas**: Relatórios e logs
- ❌ **Configurações do sistema**: Acesso limitado
- ✅ **Upload em massa**: Importar exames via Excel
- ❌ **Acesso total**: Limitado às funções de edição

**Usuário padrão**: `editor` / `editor123`

---

### 3. 👁️ **Visualizador (Viewer)**
**Descrição**: Apenas visualização de estatísticas e relatórios, sem permissão para editar conteúdo.

**Permissões**:
- ❌ **Editar conteúdo**: Não pode editar
- ❌ **Deletar conteúdo**: Não pode deletar
- ❌ **Gerenciar usuários**: Não pode gerenciar usuários
- ✅ **Visualizar estatísticas**: Relatórios e logs
- ❌ **Configurações do sistema**: Sem acesso
- ❌ **Upload em massa**: Sem acesso
- ❌ **Acesso total**: Apenas visualização

**Usuário padrão**: `viewer` / `viewer123`

---

## 🔐 Detalhamento de Permissões por Funcionalidade

### **Dashboard**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Visualizar estatísticas gerais | ✅ | ✅ | ✅ |
| Ver usuários ativos | ✅ | ✅ | ✅ |
| Ver acessos recentes | ✅ | ✅ | ✅ |

### **Gerenciamento de Exames**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Listar exames | ✅ | ✅ | ✅ |
| Adicionar exame | ✅ | ✅ | ❌ |
| Editar exame | ✅ | ✅ | ❌ |
| Deletar exame | ✅ | ❌ | ❌ |
| Upload em massa | ✅ | ✅ | ❌ |
| Download template | ✅ | ✅ | ❌ |

### **Gerenciamento de Unidades**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Listar unidades | ✅ | ✅ | ✅ |
| Adicionar unidade | ✅ | ✅ | ❌ |
| Editar unidade | ✅ | ✅ | ❌ |
| Deletar unidade | ✅ | ❌ | ❌ |

### **Gerenciamento de Avisos**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Listar avisos | ✅ | ✅ | ✅ |
| Adicionar aviso | ✅ | ✅ | ❌ |
| Editar aviso | ✅ | ✅ | ❌ |
| Deletar aviso | ✅ | ❌ | ❌ |

### **Gerenciamento de Usuários**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Listar usuários | ✅ | ❌ | ❌ |
| Adicionar usuário | ✅ | ❌ | ❌ |
| Editar usuário | ✅ | ❌ | ❌ |
| Deletar usuário | ✅ | ❌ | ❌ |

### **Relatórios e Estatísticas**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Estatísticas gerais | ✅ | ✅ | ✅ |
| Logs de acesso | ✅ | ✅ | ✅ |
| Exportar relatórios | ✅ | ✅ | ✅ |
| Gráficos de uso | ✅ | ✅ | ✅ |

### **Configurações do Sistema**
| Funcionalidade | Admin | Editor | Viewer |
|----------------|-------|--------|--------|
| Configurações básicas | ✅ | ❌ | ❌ |
| Endereços | ✅ | ❌ | ❌ |
| Redes sociais | ✅ | ❌ | ❌ |
| Horários | ✅ | ❌ | ❌ |
| Informações importantes | ✅ | ❌ | ❌ |

---

## 🛡️ Segurança e Controles

### **Proteções Implementadas**
- **Decoradores de permissão**: Verificação automática de acesso
- **Validação de formulários**: Prevenção de dados inválidos
- **Controle de sessão**: Logout automático por inatividade
- **Rate limiting**: Proteção contra ataques de força bruta
- **Sanitização de dados**: Prevenção de XSS e injeção SQL

### **Regras de Negócio**
- **Não é possível deletar o próprio usuário**
- **Não é possível deletar o último administrador**
- **Usuários inativos não podem fazer login**
- **Permissões são definidas automaticamente baseadas no role**

---

## 🔧 Como Gerenciar Usuários

### **Acessando o Gerenciamento**
1. Faça login como administrador
2. Acesse o menu lateral → "Usuários"
3. Ou acesse diretamente: `/admin/usuarios`

### **Criando um Novo Usuário**
1. Clique em "Adicionar Usuário"
2. Preencha os dados obrigatórios:
   - **Nome de usuário**: Único no sistema
   - **Email**: Único no sistema
   - **Senha**: Mínimo 6 caracteres
   - **Nível de acesso**: Selecione o role apropriado
3. As permissões são definidas automaticamente
4. Clique em "Salvar Usuário"

### **Editando um Usuário**
1. Na lista de usuários, clique no ícone de editar
2. Modifique os dados necessários
3. Para alterar a senha, preencha o campo "Senha"
4. Para manter a senha atual, deixe o campo em branco
5. Clique em "Salvar Usuário"

### **Deletando um Usuário**
1. Na lista de usuários, clique no ícone de deletar
2. Confirme a ação
3. **Restrições**:
   - Não é possível deletar o próprio usuário
   - Não é possível deletar o último administrador

---

## 📊 Monitoramento de Atividade

### **Informações Rastreadas**
- **Última atividade**: Data/hora do último acesso
- **Último login**: Data/hora do último login
- **IP de acesso**: Endereço IP do usuário
- **Páginas acessadas**: Log de navegação
- **Ações realizadas**: Log de operações

### **Dashboard de Atividade**
- **Usuários ativos recentemente**: Últimos 7 dias
- **Acessos recentes**: Últimos 10 acessos
- **Estatísticas de uso**: Por usuário e por período

---

## 🚀 Melhores Práticas

### **Para Administradores**
- **Crie usuários com permissões mínimas** necessárias
- **Monitore regularmente** a atividade dos usuários
- **Altere senhas padrão** após o primeiro acesso
- **Desative usuários** que não estão mais ativos
- **Faça backup regular** do banco de dados

### **Para Editores**
- **Use o upload em massa** para adicionar muitos exames
- **Valide dados** antes de salvar
- **Mantenha informações atualizadas** de unidades e avisos
- **Consulte estatísticas** para entender o uso do sistema

### **Para Visualizadores**
- **Acesse relatórios** para acompanhar o uso
- **Monitore acessos** para identificar tendências
- **Exporte dados** quando necessário para análise

---

## 🔄 Migração e Atualizações

### **Migração Automática**
O sistema inclui migração automática que:
- Adiciona novos campos ao banco de dados
- Atualiza usuários existentes
- Define permissões baseadas no role atual
- Cria usuários de exemplo para teste

### **Atualizações Futuras**
Para adicionar novas permissões:
1. Atualize o modelo `User` em `app/models.py`
2. Adicione decoradores nas rotas em `app/admin_routes.py`
3. Atualize os templates conforme necessário
4. Execute migração se necessário

---

## 📞 Suporte

### **Em caso de problemas**
- **Email**: suporte@helpalphaclin.com
- **WhatsApp**: (69) 98129-0005
- **Telefone**: (69) 3223-0132

### **Desenvolvido por**
- **PageUp Sistemas**
- **Responsável**: Oézios Normando
- **Versão**: 1.0.0

---

*Esta documentação foi atualizada em: 28/06/2025* 