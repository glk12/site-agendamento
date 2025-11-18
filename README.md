# site-agendamento

Aplicação Django para agendar serviços de barbearia, atualmente com fluxo web tradicional (templates) e autenticação por email/senha usando o modelo `User` padrão do Django. O código foi organizado com a intenção de evoluir para uma API REST reutilizável por diferentes barbearias.

## Tecnologias principais
- Python 3.12 (recomendado)
- Django 5.2
- PostgreSQL 16 (configurado como banco padrão)
- django-browser-reload (hot reload para desenvolvimento)
- Bootstrap 5 + Swiper.js para experiência web

## Estrutura do projeto
- `mysite/` – diretório do projeto Django
  - `manage.py` – utilitário principal
  - `mysite/settings.py` – configurações globais (PostgreSQL, templates, estáticos)
  - `mysite/urls.py` – roteamento raiz
  - `polls/` – app com todas as views atuais
    - `views.py` – index, login, register, logout
    - `forms.py` – formulários de autenticação baseados em email
    - `templates/` – páginas HTML (`index`, `login`, `register`, `navbar`)
    - `static/` – CSS, JS e imagens
    - `urls.py` – rotas públicas do app

## Funcionalidades atuais
- Landing page com carrosséis de serviços e equipe (Swiper.js)
- Fluxo de autenticação:
  - Cadastro com email + senha e login automático (`polls/views.register`)
  - Login com email/senha (`polls/views.login`)
  - Logout via POST (`polls/views.logout`)
- Layout responsivo com navbar dinâmica (links mudam conforme autenticação)
- Assets estáticos servidos a partir de `polls/static`

## Configuração e execução local
1. **Clone o repositório**
   ```bash
   git clone https://github.com/glk12/site-agendamento.git
   cd site-agendamento
   ```
2. **Crie um ambiente virtual** (opcional, mas recomendado)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Instale dependências**
   ```bash
   pip install -r mysite/requirements.txt
   ```
4. **Configure o banco**
   - Ajuste as variáveis em `mysite/mysite/settings.py` ou defina variáveis de ambiente (ex.: `DATABASE_URL`).
   - O projeto espera um PostgreSQL acessível em `localhost:5432`, banco `agend_db`, usuário `user`, senha `1234`.
5. **Execute migrações**
   ```bash
   cd mysite
   python manage.py migrate
   ```
6. **Crie um superusuário (opcional para admin)**
   ```bash
   python manage.py createsuperuser
   ```
7. **Inicie o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```
   Acesse em <http://127.0.0.1:8000/>.

## Páginas/URLs
- `/` – Landing page (`polls.views.index`)
- `/login/` – Formulário de login
- `/register/` – Formulário de cadastro
- `/logout/` – Logout (requer POST)
- `/admin/` – Django admin (se superusuário criado)

## Como evoluir para API REST reutilizável
1. **Introduzir Django REST Framework**
   - Adicionar `djangorestframework` ao `requirements.txt`.
   - Registrar `rest_framework` em `INSTALLED_APPS`.
2. **Modelar entidades de barbearia**
   - Criar modelos para `Barbershop`, `Service`, `Professional`, `Booking`, etc., em `polls/models.py`.
   - Adicionar migrações.
3. **Criar serializers**
   - Implementar serializers em `polls/serializers.py` para cada modelo e para autenticação personalizada (se necessário).
4. **Construir viewsets e rotas API**
   - Usar `rest_framework.viewsets.ModelViewSet` ou `APIView` conforme o caso.
   - Configurar roteadores em `polls/api_urls.py` e incluí-los em `mysite/urls.py` sob prefixos como `/api/v1/`.
5. **Autenticação e permissão**
   - Avaliar uso de JWT (ex.: `djangorestframework-simplejwt`) ou token session-based.
   - Configurar `DEFAULT_AUTHENTICATION_CLASSES` e `DEFAULT_PERMISSION_CLASSES` no DRF.
6. **Documentação e versionamento**
   - Adotar OpenAPI/Swagger (ex.: `drf-spectacular`) para documentar.
   - Planejar versionamento (`/api/v1/`), permitindo múltiplas barbearias com configurações distintas.
7. **Separar front-end (opcional)**
   - Uma vez que a API esteja pronta, o front-end pode migrar para um SPA ou app mobile consumindo os endpoints.

## Próximos passos sugeridos
- Normalizar configuração via `.env` (biblioteca `python-decouple` ou `django-environ`).
- Criar testes automatizados (`polls/tests.py`) cobrindo autenticação e futuras APIs.
- Automatizar provisionamento de banco (Docker Compose) para colaboradores.
- Ajustar CI/CD e linting (`ruff`, `black` etc.) conforme o projeto crescer.

---
Sinta-se à vontade para adaptar as instruções acima para a sua infraestrutura. Quando a API REST for construída, lembre-se de atualizar este README com os novos endpoints e fluxos.
