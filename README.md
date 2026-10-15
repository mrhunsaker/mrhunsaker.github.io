# mrhunsaker.github.io

Root Site for all my Github Pages websites — a splash page / landing page linking to every GitHub Pages project and documentation site.

## How the home page is populated

The home page uses the `home.html` layout (`_layouts/home.html`), which reads three YAML data files from `_data/` and renders each as a section of linked lists:

| Section on home page  | Data file              | Purpose |
| --------------------- | ---------------------- | ------- |
| Professional Projects | `_data/projects.yml`   | Work tools, apps, APIs, and documentation sites |
| Personal Projects     | `_data/personal.yml`   | Personal coding projects and my published writing |
| Instructional Materials | `_data/resources.yml` | Guides, courses, protocols, and reference sites for others |

Jekyll automatically loads every file in `_data/` as `site.data.<filename>`, so `_data/projects.yml` becomes `site.data.projects`. The layout loops over each list and renders an entry like:

```liquid
{% for p in site.data.projects %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a>
  {% if p.description %} — {{ p.description }}{% endif %}</li>
{% endfor %}
```

### Entry format

Add entries to the appropriate `.yml` file:

```yaml
- title: Required Title
  url: /Repo_Name/
  description: Optional one-line description
```

- `title` and `url` are required; `description` is optional.
- For sites under this account, use root-relative URLs such as `/Repo_Name/`
  (the `relative_url` filter adds the site base automatically).
- For external sites, use the full `https://...` URL.

### Adding a new GitHub Pages site

1. Create the repo and enable GitHub Pages on it.
2. Add an entry to `personal.yml`, `projects.yml`, or `resources.yml`
   (see table above for which section fits).
3. Commit and push — GitHub Pages rebuilds the site automatically.

### Discovering all your GitHub Pages sites

Run the helper script in this repo to list every repo with Pages enabled:

```bash
export GITHUB_TOKEN="your_token"   # optional, avoids API rate limits
python3 getGitHubPages.py
```

It prints each repo name and its live URL, which you can paste into the
`_data/` files.

### Keeping the lists in sync automatically

`update_Content.json` (repo root) is a simple JSON prompt for an LLM agent.
Give it to an agent and it will:

1. Run `getGitHubPages.py` to list all live GitHub Pages sites.
2. Add any site missing from the `_data/` files to the right one
   (personal / projects / resources) with a title and description.
3. Remove entries whose Pages site no longer exists (external links are
   never touched).
4. Validate the YAML and report what changed.
