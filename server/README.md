# HotBot Server
Serves abstracts, summaries, and other pieces of information relevant for a given paper


## Commands
- Run server locally: `flask run`
- Run server, giving access to non-local computers: `flask run --host=0.0.0.0`

## Testing
```python
import requests
requests.get("http://127.0.0.1:5000/main_paper_information", params={"paper_url":"https://www.arxiv-vanity.com/papers/1412.3555/"})
```