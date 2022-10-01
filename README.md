# Github-Graph-API
A python server using fastapi which returns a cytoscape-style graph of all public projects for a user.

Idea: Create an easy way for people to see what projects I've worked on and what technologies they use by visiting my website.

This is intended to be run on an AWS instance with a real domain name. For example, my project graph will be available through [https://project-graph.ethanposner.com/](https://project-graph.ethanposner.com/).

## Technologies
This project uses python, fastapi, and various other libraries for parsing data from github.
- **[Networkx](https://networkx.org/documentation/stable/index.html)** library for creating a graph of all projects for a user. Networkx also lets you return a cytoscape.js style graph through the [cytoscape_graph()](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.cytoscape_graph.html) function.
- **[FastAPI](https://fastapi.tiangolo.com/)** for handling and returning API calls.
- **[Traefik](https://www.nginx.com/)** is setup as the web server. It acts as a reverse proxy for the FastAPI backend. It also allows for SSL to be setup very easily. Nginx was originally used, but it caused many problems and wasn't working with SSL.
- **[PyGithub]()** allows for data from github to be easily parsed.
- **[Let's Encrypt](https://letsencrypt.org/)** for issuing SSL certificates.

## Installation with Docker
1. Make sure docker is installed: [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)
2. Start docker e.g. by running docker desktop, or by running docker daemon on linux.
3. Create a new file called `.env` and copy all contents from `.env.example` into it. Make any necessary changes.
    - Create github integration key: [Github REST API](https://docs.github.com/en/rest). Set `GITHUB_PERSONAL_INTEGRATION_KEY` to this key.
    - You must have a domain name routed to your linux machine. Set `DOMAIN_NAME` to your domain name. For example, with an AWS instance you need to do the following:
        - Create an A record with host `@` pointing to the IP address of your instance.
        - Create a CNAME record with host `www` pointing to the public IPv4 DNS for the instance.
    - Set an email to receive error messages from with `ERROR_EMAIL`.
    - If you want to use the traefik dashboard feature, set `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD`.
4. Build the docker image: `docker-compose build`
5. Start the docker image
    - Run server (a good first step for testing): `docker-compose up`
    - Run daemonized (in background): `docker-compose up -d`
    - Stop server: `docker-compose stop`

## Usage
1. Start the docker image with `docker-compose up -d`.
    - SSL certificates will expire after 3 months. See notes for more info on dealing with this.
2. The graph JSON data can be seen by visiting `https://www.<server-hostname>/`.
3. Use `cytoscape.js` to render the graph inside of a webpage ([tutorial](http://cytoscapeweb.cytoscape.org/tutorial/)). See the demo inside of the `demo` folder.

## Notes
- I setup Traefik using the tutorials [How to Deploy a Secure API with FastAPI, Docker and Traefik](https://towardsdatascience.com/how-to-deploy-a-secure-api-with-fastapi-docker-and-traefik-b1ca065b100f) and [Dockerizing FastAPI with Postgres, Uvicorn, and Traefik](https://testdriven.io/blog/fastapi-docker-traefik/#lets-encrypt).
- If after running the docker image for the first time, you get the error message `no permission to read from '/home/${USER}/Github-Graph-API/traefik-public-certificates/acme.json'`, simply change the permissions of the file. A quick and dirty fix is to do `sudo chmod 777 /home/${USER}/Github-Graph-API/traefik-public-certificates/acme.json`
