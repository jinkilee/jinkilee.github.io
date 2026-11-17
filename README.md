# jinkilee.github.io

Personal site of Jinki Lee, built with [al-folio](https://github.com/alshedivat/al-folio) (v1, gem-based).

## Where things live

| What | File |
| --- | --- |
| Site settings, feature flags | `_config.yml` |
| About page (bio, profile) | `_pages/about.md`, `assets/img/prof_pic.jpg` |
| News items | `_news/*.md` |
| Blog posts | `_posts/YYYY-MM-DD-title.md` |
| Projects | `_projects/*.md` |
| Publications | `_bibliography/papers.bib` |
| CV page / PDF | `_data/cv.yml`, `assets/pdf/JinkiLee-CV.pdf` |
| Social links | `_data/socials.yml` |

## Local preview

```bash
docker compose up        # http://localhost:8080
# or
bundle install && bundle exec jekyll serve
```

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the site and pushes it to the `gh-pages` branch.
GitHub Pages must be set to **Settings → Pages → Deploy from a branch → `gh-pages` / root**,
and **Settings → Actions → General → Workflow permissions** must be **Read and write**.

Template license: see `LICENSE-al-folio` (MIT).
