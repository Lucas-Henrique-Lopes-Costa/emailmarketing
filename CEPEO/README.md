# 📧 Sistema de Email Marketing - CEPEO

Sistema automatizado para envio de emails marketing personalizados com template HTML profissional, desenvolvido em Python.

## 🎯 Características

- ✅ Leitura automática de contatos do arquivo CSV
- ✅ Template HTML responsivo e profissional
- ✅ Imagens incorporadas (inline) no email
- ✅ Personalização com nome do destinatário
- ✅ CTAs destacados para conversão
- ✅ Credenciais seguras via arquivo .env
- ✅ Relatório detalhado de envios
- ✅ Modo de teste para validação

## 📁 Estrutura do Projeto

```
emailmarketing/
├── enviar_emails.py       # Script principal
├── email.html             # Template HTML do email
├── contato.csv            # Lista de contatos
├── .env                   # Credenciais (não versionar!)
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos ignorados pelo git
├── requirements.txt       # Dependências Python
├── README.md              # Este arquivo
└── arquivos/
    ├── logo_cepeo.jpeg    # Logo da CEPEO
    ├── produto-1.jpeg     # Imagem do produto 1
    └── produto-2.jpeg     # Imagem do produto 2
```

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configurar o arquivo .env

Abra o arquivo `.env` e preencha com suas credenciais de email:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app

FROM_NAME=CEPEO
FROM_EMAIL=seu_email@gmail.com

EMAIL_SUBJECT=CEPEO - Produtos em Destaque
```

### 2. Configuração para Gmail

Se você usar Gmail, precisará gerar uma **Senha de App**:

1. Acesse: <https://myaccount.google.com/security>
2. Ative a **Verificação em duas etapas**
3. Vá em **Senhas de app**
4. Gere uma senha para "Email" ou "Outro (Nome personalizado)"
5. Use essa senha no campo `EMAIL_PASSWORD` do arquivo `.env`

### 3. Outros provedores de email

Para outros provedores, configure o SMTP adequado:

**Outlook/Hotmail:**

```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**

```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Provedor personalizado:**
Consulte a documentação do seu provedor de email.

## 📝 Preparação dos Arquivos

### 1. Arquivo contato.csv

Certifique-se de que o arquivo `contato.csv` está no formato correto:

```csv
Nome;Email
Empresa ABC;contato@empresaabc.com.br
João Silva;joao@empresa.com
```

- Separador: ponto e vírgula (`;`)
- Primeira linha: cabeçalho (`Nome;Email`)
- Emails inválidos são automaticamente ignorados

### 2. Template HTML (email.html)

O template já está pronto e inclui:

- Logo da CEPEO
- 2 produtos em destaque com imagens
- Botões CTA (Call-to-Action)
- Design responsivo
- Footer com informações de contato

**Personalize os links dos produtos** editando o arquivo `email.html`:

- `https://www.cepeo.com.br/produto-1`
- `https://www.cepeo.com.br/produto-2`
- `https://www.cepeo.com.br/contato`

### 3. Imagens

Coloque as imagens na pasta `arquivos/`:

- `logo_cepeo.jpeg` - Logo da empresa
- `produto-1.jpeg` - Imagem do primeiro produto
- `produto-2.jpeg` - Imagem do segundo produto

## 🎮 Como Usar

### Modo Teste (Recomendado)

Para enviar apenas para os primeiros 5 contatos (teste):

```bash
python enviar_emails.py
```

No código, edite a linha 243:

```python
email_system.enviar_campanha(limite=5)  # Envia para 5 contatos apenas
```

### Modo Produção

Para enviar para todos os contatos do CSV:

```bash
python enviar_emails.py
```

No código, use:

```python
email_system.enviar_campanha()  # Envia para todos
```

### Parâmetros Opcionais

```python
# Enviar para 10 contatos com delay de 2 segundos entre envios
email_system.enviar_campanha(limite=10, delay=2)
```

- **limite**: Número máximo de emails a enviar
- **delay**: Tempo de espera (em segundos) entre cada envio

## 📊 Exemplo de Saída

```
============================================================
📧 SISTEMA DE EMAIL MARKETING - CEPEO
============================================================

✅ 3818 contatos válidos carregados do CSV

📊 Resumo da campanha:
   - Total de destinatários: 3818
   - Servidor SMTP: smtp.gmail.com
   - Remetente: CEPEO <seu_email@gmail.com>
   - Assunto: CEPEO - Produtos em Destaque

Deseja continuar com o envio? (s/n): s

🚀 Iniciando envio de emails...

[1/3818] Enviando para: 4 BIO MEDICAMENTOS (juliana.gomes@4bio.com.br)... ✅ Sucesso!
[2/3818] Enviando para: A & E CENTRO DE MEDICINA (cmaavancada@outlook.com)... ✅ Sucesso!
...

============================================================
📊 RELATÓRIO FINAL
============================================================
✅ Emails enviados com sucesso: 3815
❌ Falhas no envio: 3
📈 Taxa de sucesso: 99.9%
============================================================
```

## 🔒 Segurança

- ✅ O arquivo `.env` está no `.gitignore` (não será commitado)
- ✅ Use senhas de aplicativo, não sua senha principal
- ✅ Nunca compartilhe suas credenciais
- ✅ Revise o arquivo `.env` antes de commitar

## ⚠️ Avisos Importantes

### Limites de Envio

- **Gmail**: ~500 emails/dia (contas gratuitas)
- **Gmail Workspace**: ~2000 emails/dia
- Outros provedores: consulte a documentação

### Boas Práticas

1. **Sempre teste primeiro** com poucos contatos
2. **Use delay entre envios** (evita ser marcado como spam)
3. **Valide seus contatos** (remova emails inválidos)
4. **Respeite a LGPD** (tenha consentimento para envio)
5. **Ofereça opção de descadastro**

## 🐛 Resolução de Problemas

### Erro: "Username and Password not accepted"

- Verifique se ativou a verificação em 2 etapas
- Use uma senha de aplicativo, não sua senha normal
- Verifique se o email está correto no .env

### Erro: "SMTPAuthenticationError"

- Credenciais incorretas no arquivo .env
- Verifique o servidor SMTP e porta

### Emails indo para spam

- Adicione SPF/DKIM ao seu domínio
- Reduza a frequência de envio
- Peça aos destinatários para adicionar aos contatos

### Timeout ou conexão recusada

- Verifique sua conexão com a internet
- Alguns provedores bloqueiam porta 587 - tente 465
- Firewall pode estar bloqueando

## 📞 Suporte

Para dúvidas ou problemas:

- 📧 Email: <cepeodireto@cepeo.com.br>
- 📞 0800 071 23 31
- 📱 (71) 3341-9312 | (71) 99729-6088
- 📍 R. Coronel Alm Rehem, 82 - Caminho Árvores, 1° andar - Salvador, BA - 41820-768
- 🌐 Website: <https://www.cepeo.com.br>

## 📄 Licença

Este projeto é de uso interno da CEPEO.

---

**Desenvolvido com ❤️ para CEPEO**
