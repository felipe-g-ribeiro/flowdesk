# FlowDesk

## Introdução

O FlowDesk é um sistema ERP web desenvolvido com Django para apoiar o
gerenciamento de produtos, categorias, clientes, vendas e estoque. A
aplicação possui um dashboard com indicadores gerais e interfaces baseadas em
Bootstrap, com uso de HTMX para interações dinâmicas.

Esta documentação apresenta a estrutura atual do projeto, seus principais
fluxos e as tecnologias utilizadas.

## Objetivo

O objetivo do FlowDesk é fornecer uma aplicação de gestão empresarial que
permita:

- Cadastrar, consultar, editar e excluir produtos.
- Organizar produtos por categorias.
- Cadastrar e gerenciar clientes.
- Registrar vendas vinculadas a clientes e produtos.
- Atualizar o estoque automaticamente após uma venda.
- Exibir indicadores resumidos no dashboard.
- Restringir áreas internas a usuários autenticados.
- Praticar desenvolvimento web com Django, HTMX, Bootstrap e testes
  automatizados.

## Tecnologias

- **Python**: linguagem principal da aplicação.
- **Django**: framework web, ORM, templates, autenticação e testes.
- **Bootstrap**: componentes e estilos da interface.
- **HTMX**: busca dinâmica de produtos sem recarregar toda a página.
- **PostgreSQL**: banco de dados utilizado pelo projeto.
- **Git e GitHub**: versionamento e hospedagem do código.

Os estilos personalizados utilizam, entre outras regras, a remoção do
sublinear dos links e a estilização das tabelas:

```css
a {
    text-decoration: none;
    color: #464feb;
}

tr th,
tr td {
    border: 1px solid #e6e6e6;
}

tr th {
    background-color: #f5f5f5;
}
```

## Estrutura do projeto

O projeto segue a estrutura padrão do Django:

```text
C:\Estagio\flowdesk\
├── README.md
├── DOCUMENTACAO.md
└── flowdesk\
    ├── manage.py
    ├── flowdesk\
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── core\
    │   ├── views.py
    │   ├── urls.py
    │   ├── tests.py
    │   └── templates\
    ├── products\
    │   ├── models.py
    │   ├── forms.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── tests.py
    │   └── templates\
    ├── customers\
    │   ├── models.py
    │   ├── forms.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── tests.py
    │   └── templates\
    ├── sales\
    │   ├── models.py
    │   ├── forms.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── tests.py
    │   └── templates\
    └── static\
        └── css\
```

Os comandos de gerenciamento devem ser executados no diretório que contém o
arquivo `manage.py`:

```powershell
cd C:\Estagio\flowdesk\flowdesk
python manage.py runserver
```

## Modelagem do banco

### Category

Representa uma categoria de produtos.

- `name`: nome único da categoria.

### Product

Representa um produto comercializado.

- `name`: nome do produto.
- `category`: chave estrangeira para `Category`.
- `price`: preço decimal do produto.
- `stock`: quantidade disponível em estoque.
- `created_at`: data de criação.

Uma categoria pode possuir vários produtos. O relacionamento é acessado pelo
nome relacionado `products`.

### Customer

Representa um cliente.

- `name`: nome do cliente.
- `email`: e-mail, opcional.
- `phone`: telefone, opcional.
- `created_at`: data de criação.

### Sale

Representa uma venda.

- `customer`: chave estrangeira para `Customer`.
- `product`: chave estrangeira para `Product`.
- `quantity`: quantidade vendida.
- `total`: valor total da venda.
- `created_at`: data de criação.

Cada venda está relacionada a um cliente e a um produto.

## Funcionalidades

### Dashboard

O dashboard está disponível na rota `/` e apresenta a quantidade total de:

- Produtos.
- Categorias.
- Clientes.
- Vendas.

### Produtos

O módulo de produtos oferece:

- Listagem em `/products/`.
- Cadastro em `/products/novo/`.
- Edição em `/products/editar/<id>/`.
- Exclusão em `/products/excluir/<id>/`.
- Busca por nome.
- Associação com categorias.
- Exibição de preço e estoque.

### Categorias

O módulo de categorias oferece:

- Listagem em `/products/categorias/`.
- Cadastro em `/products/categorias/nova/`.
- Edição em `/products/categorias/editar/<id>/`.
- Exclusão em `/products/categorias/excluir/<id>/`.

### Clientes

O módulo de clientes oferece:

- Listagem em `/customers/`.
- Cadastro em `/customers/novo/`.
- Edição em `/customers/editar/<id>/`.
- Exclusão em `/customers/excluir/<id>/`.

### Vendas

O módulo de vendas oferece:

- Listagem em `/sales/`.
- Cadastro em `/sales/nova/`.
- Edição em `/sales/editar/<id>/`.
- Exclusão em `/sales/excluir/<id>/`.

## Fluxo de vendas

O fluxo de criação de uma venda ocorre da seguinte forma:

1. O usuário autenticado acessa o formulário de nova venda.
2. Seleciona um cliente.
3. Seleciona um produto.
4. Informa a quantidade.
5. O sistema calcula o total multiplicando o preço do produto pela quantidade.
6. O sistema verifica se há estoque suficiente.
7. Se houver estoque, a venda é salva.
8. O estoque do produto é reduzido pela quantidade vendida.
9. O usuário é redirecionado para a lista de vendas.

Quando a quantidade solicitada é maior que o estoque disponível, a venda não é
salva e o formulário informa:

```text
Estoque insuficiente.
```

## Controle de estoque

O estoque é armazenado no campo `stock` do model `Product`.

No cadastro de uma venda, a aplicação:

```python
sale.total = sale.product.price * sale.quantity
product.stock -= sale.quantity
product.save()
```

O fluxo também valida a disponibilidade antes de alterar o estoque. Assim,
vendas com quantidade superior ao estoque atual são rejeitadas.

## Autenticação

O projeto utiliza o sistema de autenticação nativo do Django.

Rotas disponíveis:

- `/login/`: tela de login.
- `/logout/`: encerramento da sessão por requisição POST.

As páginas internas utilizam `@login_required`, incluindo:

- Dashboard.
- Produtos.
- Categorias.
- Clientes.
- Vendas.

Usuários não autenticados são redirecionados para a página de login com o
parâmetro `next`, que identifica a página originalmente solicitada.

Para criar um usuário administrador:

```powershell
python manage.py createsuperuser
```

## HTMX

O HTMX é utilizado na busca de produtos.

Ao digitar no campo de busca, o navegador envia automaticamente uma requisição
para a listagem com o parâmetro `search`. A requisição utiliza um atraso para
evitar chamadas a cada tecla:

```html
hx-get="{% url 'product_list' %}"
hx-trigger="input changed delay:500ms"
hx-target="#product-table"
hx-swap="outerHTML"
```

A view filtra os produtos pelo nome usando `icontains`. Quando a requisição é
HTMX, somente o partial da tabela é retornado:

```text
products/templates/products/partials/product_table.html
```

Essa abordagem atualiza apenas a tabela, sem recarregar a página inteira.

## PostgreSQL

O FlowDesk já está configurado para utilizar PostgreSQL como banco de dados.
A configuração está definida em `flowdesk/settings.py` com o backend
`django.db.backends.postgresql`, utilizando uma instância PostgreSQL local.

As migrações do banco são executadas com:

```powershell
python manage.py migrate
```

As credenciais do banco devem permanecer fora da documentação e, em ambientes
de produção, ser fornecidas por variáveis de ambiente ou outro mecanismo
seguro de configuração.

## Testes automatizados

Os testes foram implementados com `django.test.TestCase` nos seguintes
arquivos:

- `products/tests.py`
- `customers/tests.py`
- `sales/tests.py`
- `core/tests.py`

Os testes validam:

- Criação de produtos, categorias e clientes.
- Relacionamento entre categorias e produtos.
- Relacionamento entre vendas, clientes e produtos.
- Cadastro, edição e exclusão por meio das views.
- Cálculo do total da venda.
- Atualização do estoque.
- Rejeição de venda sem estoque suficiente.
- Login válido e inválido.
- Logout.
- Acesso autenticado ao dashboard.
- Redirecionamento de usuários anônimos.

Para executar os testes:

```powershell
cd C:\Estagio\flowdesk\flowdesk
python manage.py test products customers sales core
```

Suíte validada:

```text
Ran 20 tests
OK
```

## Conclusão

O FlowDesk possui uma base funcional de ERP com dashboard, autenticação,
cadastros de produtos, categorias e clientes, registro de vendas e controle de
estoque. A aplicação também conta com busca dinâmica via HTMX e testes
automatizados para os principais fluxos.

As próximas evoluções recomendadas são o aprimoramento da configuração segura
do PostgreSQL, o aprimoramento da exclusão para utilizar exclusivamente POST
com confirmação, a ampliação da cobertura de testes e o refinamento da
interface e das regras de negócio.
