# Run with uvicorn Github-Graph-API.graph_api_server:app --host gh_fastapi --port 8500
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, 'Github-Graph-API')
from github_projects_graph import GithubGraphCacheHandler

load_dotenv()

app = FastAPI()

origins = os.environ.get('ALLOWED_ORIGINS').split(' ')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gh_integration_key = os.environ.get('GITHUB_PERSONAL_INTEGRATION_KEY')
if not gh_integration_key:
    raise ValueError('A github integration key must be provided through the GITHUB_PERSONAL_INTEGRATION_KEY env variable')

graph_cache_handler = GithubGraphCacheHandler(gh_integration_key, '/graph_cache')


# access like this: http://127.0.0.1:8500/
@app.get("/")
async def get_block_json():
    graph_json = graph_cache_handler.get_graph_json()
    style_json = graph_cache_handler.get_graph().get_cytoscape_style()
    return JSONResponse(content={'graph': graph_json,
                                 'style': style_json})
