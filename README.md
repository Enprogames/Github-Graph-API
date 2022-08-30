# Github-Graph-API
A python server using fastapi which returns a cytoscape-style graph of all public projects for a user.

Idea: 

## Technologies
This project uses python, fastapi, and various other libraries for parsing data from github. It returns a 
- **[Networkx](https://networkx.org/documentation/stable/index.html)** library for creating a graph of all projects for a user. Networkx also lets you return a cytoscape.js style graph through the [cytoscape_graph()](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.cytoscape_graph.html) function.
- **[FastAPI](https://fastapi.tiangolo.com/)** for handling and returning API calls.
- **[Nginx](https://www.nginx.com/)** is setup as the web server. It acts as a reverse proxy for the FastAPI backend.
- **[PyGithub]()** allows for data from github to be easily parsed.

## Installation with Docker
1. Make sure docker is installed: [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)
2. Start docker e.g. by running docker desktop, or by running docker daemon on linux.
3. Create a new file called `.env` and copy all contents from `.env.example` into it. Make any necessary changes.
3. Build the docker image: `docker-compose build`
4. Start the docker image
    - Run server (a good first step for testing): `docker-compose up`
    - Run daemonized (in background): `docker-compose up -d`
    - Stop server: `docker-compose stop`

## Usage
1. Create github personal integration key
2. In `.env`, set `GITHUB_PERSONAL_INTEGRATION_KEY` to your personal integration key.
3. Start the docker image with `docker-compose up -d`.
4. The graph JSON data can be seen by visiting `http://<server-hostname>/`.
5. Use `cytoscape.js` to render the graph inside of a webpage ([tutorial](http://cytoscapeweb.cytoscape.org/tutorial/)).
