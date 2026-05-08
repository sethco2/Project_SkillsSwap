# Seth Grant — AI Portfolio + Campus SkillSwap

Final AI Portfolio for Baylor's MIS AI class. A Django site that doubles as
Seth Grant's personal portfolio (front door at `/`) and a live demo of the
Campus SkillSwap class project (mounted at `/skillswap/`).

## Rubric alignment

The site covers every rubric requirement in one Django project.

| Required page         | Route                                |
| --------------------- | ------------------------------------ |
| Home                  | `/`                                  |
| About                 | `/about/`                            |
| Projects              | `/projects/`                         |
| Project detail        | `/projects/<slug>/`                  |
| Skills                | `/skills/`                           |
| Resume                | `/resume/`                           |
| Contact               | `/contact/`                          |
| Django admin          | `/admin/`                            |
| Live Django demo      | `/skillswap/` (Campus SkillSwap)     |

Every project detail page has the rubric's required 10 sections:

1. Project title
2. One-sentence summary
3. Business problem
4. Tools used
5. Key features
6. My role / contribution
7. Biggest challenge
8. What I learned
9. Screenshot or visual
10. GitHub or demo link

The 6 required projects are seeded by a data migration, fully editable from
Django admin: HandyMan Pricing Agent (LangChain), Personal Document Brain
(n8n), Conversational Chatbot, Google AI Studio Media, scikit-learn ML, and
Campus SkillSwap (Django).

Django features used: models, views, templates, ORM, admin, auth (existing
SkillSwap), and migrations (including a data migration that seeds content).

## Tech stack

- Python 3.12, Django 5.1+
- SQLite by default; Postgres via `DATABASE_URL` in production
- Whitenoise for static files
- Gunicorn for production WSGI
- Custom CSS with a dark, minimal aesthetic (Inter + JetBrains Mono)
- Pillow for image uploads via Django admin

## Run locally

```powershell
# 1. Create and activate a virtualenv
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file and fill in any values you want to override
copy .env.example .env

# 4. Run migrations (creates the schema and seeds content)
python manage.py migrate

# 5. Create an admin user so you can edit content at /admin/
python manage.py createsuperuser

# 6. Start the dev server
python manage.py runserver
```

Then visit:

- <http://127.0.0.1:8000/> — portfolio
- <http://127.0.0.1:8000/admin/> — admin (edit projects, skills, etc.)
- <http://127.0.0.1:8000/skillswap/> — Campus SkillSwap live demo

## Editing content

Everything renders from the database. Sign in to `/admin/` and edit:

- **Projects** — the 6 case studies. Use either the `image` upload or
  set `static_image` to a path inside `/static/` (e.g.
  `media/handyman-terminal.png`).
- **Skills** — grouped into AI, Web, ML, and Business.
- **Personal builds** — the "Beyond the classroom" section.
- **Experience** — entries on the resume page.

Replace seed screenshots by dropping new files into
`static/media/` (project images) or by uploading via admin.

## Deployment

The project is configured for both Railway and Render. Pick one.

### Railway (one-click style)

1. Push the repo to GitHub.
2. In Railway: **New Project → Deploy from GitHub repo**.
3. Add a Postgres plugin (optional, recommended). Railway auto-injects
   `DATABASE_URL`.
4. Add environment variables in the service's **Variables** tab:
   - `DJANGO_SECRET_KEY` — long random string
   - `DJANGO_DEBUG` — `False`
   - `DJANGO_ALLOWED_HOSTS` — your `*.up.railway.app` host (and any custom
     domain)
   - `DJANGO_CSRF_TRUSTED_ORIGINS` —
     `https://your-app.up.railway.app`
   - (Optional) `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
     `CONTACT_EMAIL` to enable the contact form.
5. Railway uses `railway.json` and runs `migrate` + `collectstatic` +
   `gunicorn` on each deploy.

### Render

1. Push the repo to GitHub.
2. In Render: **New → Blueprint** and point it at the repo. Render reads
   `render.yaml` and provisions the service.
3. To use Postgres: add a Render Postgres instance, then set
   `DATABASE_URL` on the web service.
4. Set the same environment variables listed above (Render's blueprint
   already creates `DJANGO_SECRET_KEY` and sets sensible defaults).

### Static files

`whitenoise` serves static files in production. `collectstatic` runs
automatically as part of the release/build step on both platforms. The
seeded screenshots live in `static/media/` and are picked up by
`collectstatic`. Admin-uploaded images live in `MEDIA_ROOT` (`/media/`),
which is gitignored — for persistent uploads in production, switch to
S3/Cloudinary or attach a Render disk.

### SQLite vs Postgres

SQLite is fine for the class submission and works on both Railway and
Render. The tradeoff: Render's free tier has an ephemeral filesystem, so
the SQLite file is rebuilt every deploy and any admin edits made through
the live site are lost. For durable edits, set `DATABASE_URL` to a managed
Postgres connection string. The code reads `DATABASE_URL` automatically
via `dj-database-url`.

## Project structure

```
.
├── manage.py
├── requirements.txt
├── Procfile             # Railway/Heroku-style release + web
├── runtime.txt          # Python version
├── railway.json         # Railway deploy config
├── render.yaml          # Render blueprint
├── .env.example         # Env var template
├── skillswap/           # Project package (settings, urls, wsgi)
├── portfolio/           # Portfolio app — front door of the site
│   ├── models.py        # Project, Skill, PersonalBuild, Experience
│   ├── admin.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── context_processors.py
│   └── migrations/
│       ├── 0001_initial.py
│       └── 0002_seed_content.py   # Seeds the 6 required projects
├── skills/              # Existing Campus SkillSwap app (live demo)
├── accounts/            # Existing accounts app for SkillSwap auth
├── templates/
│   ├── base.html        # SkillSwap base
│   └── portfolio/       # Portfolio templates (dark theme)
└── static/
    ├── css/
    │   ├── custom.css   # SkillSwap CSS
    │   └── portfolio.css
    └── media/
        ├── headshot.jpg
        ├── Seth_Grant_Resume.pdf
        └── (screenshots…)
```

## Required environment variables

| Variable                       | Purpose                                  |
| ------------------------------ | ---------------------------------------- |
| `DJANGO_SECRET_KEY`            | Django secret key                        |
| `DJANGO_DEBUG`                 | `True` locally, `False` in production    |
| `DJANGO_ALLOWED_HOSTS`         | Comma-separated host list                |
| `DJANGO_CSRF_TRUSTED_ORIGINS`  | Comma-separated `https://…` origins      |
| `DATABASE_URL` (optional)      | Postgres connection string               |
| `EMAIL_HOST` etc. (optional)   | SMTP for the contact form                |
| `CONTACT_EMAIL` (optional)     | Where contact-form messages go           |

## Replace later

- `static/media/headshot.jpg` — already populated from your headshot
- `static/media/Seth_Grant_Resume.pdf` — replace when you have a fresh PDF
- `static/media/*.png` — swap the seeded screenshots with real ones
- GitHub / demo links — set per project in `/admin/`

## Links

- Portfolio: TBD (paste deployed URL here once live)
- Repo: TBD
