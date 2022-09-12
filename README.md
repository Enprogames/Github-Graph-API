# Github-Graph-API
A python server using fastapi which returns a cytoscape-style graph of all public projects for a user.

Idea: Create an easy way for people to see what projects I've worked on and what technologies they use by visiting my website.

## Technologies
This project uses python, fastapi, and various other libraries for parsing data from github.
- **[Networkx](https://networkx.org/documentation/stable/index.html)** library for creating a graph of all projects for a user. Networkx also lets you return a cytoscape.js style graph through the [cytoscape_graph()](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.cytoscape_graph.html) function.
- **[FastAPI](https://fastapi.tiangolo.com/)** for handling and returning API calls.
- **[Nginx](https://www.nginx.com/)** is setup as the web server. It acts as a reverse proxy for the FastAPI backend.
- **[PyGithub]()** allows for data from github to be easily parsed.
- **[Let's Encrypt](https://letsencrypt.org/)** for issuing SSL certificates.

## Installation with Docker
1. Make sure docker is installed: [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)
2. Start docker e.g. by running docker desktop, or by running docker daemon on linux.
3. Create a new file called `.env` and copy all contents from `.env.example` into it. Make any necessary changes.
4. Go to `nginx/nginx.conf` and change all occurrences of `example.com` to your domain name. # lamma
3. Build the docker image: `docker-compose build`
4. Start the docker image
    - Run server (a good first step for testing): `docker-compose up`
    - Run daemonized (in background): `docker-compose up -d`
    - Stop server: `docker-compose stop`

## Usage
1. Create github personal integration key
2. In `.env`, set `GITHUB_PERSONAL_INTEGRATION_KEY` to your personal integration key.
3. Go to `nginx/nginx.conf`. Change all occurences of `project-graph-ethanposner.com` to your website name e.g. `bobswebsite.com`.
4. Start the docker image with `docker-compose up -d`.
5. With the docker image running, run `docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d <server-hostname>` to create a new SSL certificate. Rate limits can apply, so use letsencrypt staging environment with `--test-cert` while testing.
    - SSL certificates will expire after 3 months. See notes for more info on dealing with this.
6. The graph JSON data can be seen by visiting `https://www.<server-hostname>/`.
7. Use `cytoscape.js` to render the graph inside of a webpage ([tutorial](http://cytoscapeweb.cytoscape.org/tutorial/)). See the demo inside of the `demo` folder.

## Notes
- I followed the tutorial [HTTPS using Nginx and Let's encrypt in Docker](https://mindsers.blog/post/https-using-nginx-certbot-docker/) to get SSL working. Some parts of the tutorial were incomplete, so 
- SSL certificates from letsencrypt will expire after 3 months. With the docker image running, renew the certificates with `docker compose run --rm certbot renew`. Maybe start a cron job to automate this?
