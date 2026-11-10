# Ekar — Tupi-Portuguese sentence search

Ekar (*ekar*, "search" in Tupi) is a small web app for searching example sentences in Tupi (Tupi Antigo), with Portuguese translations, and for looking up word definitions.

## Features

- Search by a Tupi word and get every sentence that contains it, with its translation.
- Show the source of each sentence when one is recorded, linked to the original page.
- Show a word's definition when it exists in the dictionary data.
- Web page at `/`, plus a JSON API for the same data.
- Terminal search with `main.py`.
- The public app opens the database in read-only mode, so searches can't change the data.

Search matching ignores accents and capital letters, and treats the apostrophe variants `’`, `‘` and `ʼ` as the same character. It matches the Tupi text only, not the Portuguese translations.

## Data

- `tupi.db` (SQLite) holds the sentences and words used by the app.
- 85 expressions were imported from [Língua Brasílica — Expressões](https://linguabrasilica.wordpress.com/expressoes/). Each one links back to that page through its `fonte` field. Thanks to the authors of that page.
- Some entries are fragments or single words rather than full sentences.

## Project structure

| File | Purpose |
| --- | --- |
| `api.py` | FastAPI app: the web page and the JSON API |
| `search.py` | Shared search functions and read-only database connection |
| `database.py` | Database schema, text normalization, and JSON import |
| `main.py` | Terminal search |
| `static/index.html` | Search page (plain HTML, CSS and JavaScript) |
| `tupi.db` | Sentence and word database |
| `requirements.txt` | Python dependencies |

## Running locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload
```

Then open http://127.0.0.1:8000/. Interactive API docs are at http://127.0.0.1:8000/docs.

To search from the terminal instead:

```bash
python main.py
```

## API

| Method and path | Returns |
| --- | --- |
| `GET /api/search?q=<word>` | `busca`, `definicao` (or `null`), and `frases`, a list of `{tupi, traducao, fonte}` |
| `GET /api/words/<word>` | `palavra` and `definicao`, or 404 if the word isn't in the dictionary |

Example:

```bash
curl "http://127.0.0.1:8000/api/search?q=katu"
```

## Deployment

The app is a standard Python web service. On a host such as Render, use:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
