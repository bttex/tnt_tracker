# Rastreamento de Encomendas com TNT Brasil

Este projeto automatiza a consulta de status de encomendas no portal da TNT Brasil, extrai as informações mais recentes e envia um email com os dados rastreados usando um email iCloud.

## Funcionalidades

- Automação de navegação no site da TNT Brasil usando Playwright.
- Extração de informações relevantes da tabela de rastreamento.
- Envio de notificações por email com os detalhes do rastreamento.

## Requisitos

- Python 3.7+
- Playwright
- Biblioteca `python-dotenv`
- Uma conta iCloud com senha específica para apps (App-Specific Password).

## Configuração

1. **Instalar Dependências:**
   ```bash
   pip install playwright python-dotenv
   playwright install
   ```

2. **Configurar Variáveis de Ambiente:**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   EMAIL=<seu_email_icloud>
   APP_PASSWORD=<sua_senha_especifica_para_apps>
   CPF=<cpf_utilizado_para_rastreamento>
   NOTA=<nota_fiscal_utilizada_para_rastreamento>
   ```

   - **EMAIL:** Seu endereço de email do iCloud.
   - **APP_PASSWORD:** Senha específica para aplicativos, gerada em sua conta Apple ID.
   - **CPF:** CPF utilizado para a consulta no site da TNT Brasil.
   - **NOTA:** Número da nota fiscal para a consulta.

## Uso

Execute o script principal para realizar o rastreamento e envio das informações:

```bash
python tnt_tracking.py
```

## Fluxo de Operação

1. O script acessa o site da TNT Brasil.
2. Preenche os campos necessários (CPF e Nota Fiscal) para realizar a busca.
3. Aguarda o carregamento da tabela de rastreamento.
4. Extrai as informações mais recentes (Data, Status e Local).
5. Envia essas informações por email para o endereço configurado.

## Exemplo de Email Enviado

```
Assunto: TNT Tracking Update - 2024-12-10 15:30

Últimas informações de rastreamento:

Data: 2024-12-10
Status: Entregue
Local: Centro de Distribuição - São Paulo
```

## Estrutura do Projeto

```
.
├── tnt_tracking.py  # Script principal
├── .env             # Arquivo de configuração com variáveis de ambiente
├── requirements.txt # Dependências do projeto
```

## Notas

- Certifique-se de usar uma senha específica para apps em sua conta iCloud para maior segurança.
- O script usa Playwright em modo headless para automação do navegador, o que significa que a interface do navegador não será exibida durante a execução.

## Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Envie um Pull Request para revisão.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

