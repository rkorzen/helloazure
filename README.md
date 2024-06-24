
## Azure

Skoro docelowo chcesz mieć bazę danych, warto teraz wybrać opcję "Aplikacja internetowa i baza danych". Dzięki temu będziesz miał bazę danych PostgreSQL skonfigurowaną od razu z aplikacją. Poniżej znajdziesz kroki, jak skonfigurować tę opcję i zintegrować ją z Twoją aplikacją Django.

### Kroki do utworzenia aplikacji internetowej z bazą danych na Azure

1. **Zaloguj się do Azure Portal**: Wejdź na [Azure Portal](https://portal.azure.com/) i zaloguj się na swoje konto.

2. **Utwórz nową aplikację internetową z bazą danych**:
    - Wybierz `Create a resource` w lewym górnym rogu.
    - W polu wyszukiwania wpisz `Web App + Database` i wybierz tę opcję z wyników.
    - Kliknij `Create`.

3. **Konfiguracja aplikacji internetowej i bazy danych**:
    - **Subscription**: Wybierz swoją subskrypcję.
    - **Resource Group**: Utwórz nową lub wybierz istniejącą grupę zasobów.
    - **Name**: Podaj unikalną nazwę dla swojej aplikacji. Ta nazwa będzie częścią adresu URL (np. `your-app-name.azurewebsites.net`).
    - **Database provider**: Wybierz `PostgreSQL`.
    - **App Service plan**: Wybierz plan, który najlepiej odpowiada Twoim potrzebom. Na początek możesz wybrać plan darmowy lub z niskimi kosztami.
    - **Region**: Wybierz region, w którym chcesz hostować swoją aplikację.
    - Kliknij `Next` i przejdź przez resztę kroków konfiguracji, używając domyślnych ustawień lub dostosowując je według potrzeb.
    - Na końcu kliknij `Review + create`, a potem `Create`.




### Konfiguracja aplikacji Django do używania bazy danych PostgreSQL

1. **Uzyskaj dane połączenia do bazy danych**:
    - Po utworzeniu zasobu, przejdź do swojej aplikacji webowej w Azure Portal.
    - W sekcji `Settings` wybierz `Configuration`.
    - Znajdziesz tam zmienne środowiskowe związane z bazą danych, takie jak `DATABASE_URL`. Możesz również przejść do swojej bazy danych PostgreSQL i skopiować dane połączenia (hostname, username, password, database name, port).

2. **Aktualizuj plik `settings.py` w swojej aplikacji Django**:

```python
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-3tiwh!42k24#d2w#j%n_)t&f^tu(0*ovp%%ay457l+!0r*_0r)"

DEBUG = True

ALLOWED_HOSTS = ['your-app-name.azurewebsites.net', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hello_azure.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hello_azure.wsgi.application"

# Database
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### Konfiguracja GitHub Actions

Upewnij się, że plik workflow GitHub Actions (`deploy.yml`) zawiera odpowiednie kroki do wdrożenia aplikacji:

```yaml
name: Django CI/CD

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Django tests
      run: |
        python manage.py migrate
        python manage.py test

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'your-app-name'
        slot-name: 'production'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### Generowanie profilu publikacji i dodanie go do GitHub

1. **Generowanie profilu publikacji**:
    - W Azure Portal, przejdź do swojej aplikacji webowej.
    - W menu po lewej stronie wybierz `Get publish profile`.
    - Zapisz pobrany plik `.publishsettings` na swoim komputerze.

2. **Dodanie profilu publikacji do GitHub Secrets**:
    - Przejdź do swojego repozytorium na GitHub.
    - Wybierz `Settings`.
    - Przejdź do `Secrets and variables` > `Actions`.
    - Kliknij `New repository secret`.
    - Nazwij sekret `AZURE_WEBAPP_PUBLISH_PROFILE`.
    - Skopiuj zawartość pliku `.publishsettings` i wklej ją do pola wartości sekretu.
    - Kliknij `Add secret`.

Po wykonaniu tych kroków, Twoje workflow GitHub Actions powinno być gotowe do automatycznego wdrożenia aplikacji na Azure przy każdym pushu do gałęzi `main`. Jeśli masz dalsze pytania lub potrzebujesz dodatkowej pomocy, daj znać!




# TROUBLESHOOTING


Przy zmianie workflow może być problem z wypchnięciem

 ! [remote rejected] master -> master (refusing to allow a Personal Access Token to create or update workflow `.github/workflows/master_alxazure.yml` without `workflow` scope)
error: nie można wypchnąć niektórych referencji do „https://github.com/rkorzen/helloazure.git”




    create a PAT (personal access token): official doc here. Make sure to tick the box "workflow" when creating it.
    In the terminal, instead of the classic
    git remote add origin https://github.com/<account>/<repo>.git
    swap it by
    git remote add origin https://<PAT>@github.com/<account>/<repo>.git
    Follow-up with the classic git branch -M main and git push -u origin main
