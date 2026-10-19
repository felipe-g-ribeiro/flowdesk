# flowdesk

Sistema ERP web desenvolvido com Django, HTMX e Bootstrap para gerenciamento de produtos, clientes, vendas e estoque.

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale o Django:
   ```bash
   pip install "django~=5.2"
   ```
3. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
4. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

Acesse `http://127.0.0.1:8000/`.
