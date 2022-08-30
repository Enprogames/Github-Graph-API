import os
from pathlib import Path
from collections import defaultdict
import time

import requests
import dill as pickle
import networkx as nx
from github import Github
from github.Repository import Repository


class LineStats:
    def __init__(self, lines: int = 0, percentage: float = 0):
        self.lines: int = lines  # number of lines written for a given programming language
        self.percentage: float = percentage  # percentage of total number of lines

    def __str__(self):
        return f"lines: {self.lines}, per: {round(self.percentage * 100, 2)}"

    def __repr__(self):
        return self.__str__()


class GithubStats:
    def __init__(self, github_integration_key: str):
        self.github: Github = Github(github_integration_key)

        # stats about lines written for each programming language
        self.language_stats: dict[str, int] = defaultdict(lambda: LineStats())
        # stats about how many lines were written for each language in this repo
        self.repo_language_stats = {}

        self.total_lines = 0

    def get_stats(self) -> 'GithubStats':

        self.total_lines = 0

        self.repos: list[Repository] = self.github.get_user().get_repos()
        # Then play with your Github objects:
        for repo in self.github.get_user().get_repos():
            if not repo.private:
                repo_languages = repo.get_languages()
                total_repo_lines = sum(lines for lines in repo_languages.values())
                self.total_lines += total_repo_lines
                # calculate stats about how many lines were written for each language in this repo
                self.repo_language_stats[repo.name] = {language: LineStats(lines, lines / total_repo_lines)
                                                       for language, lines in repo_languages.items()}

                for language, lines in repo_languages.items():
                    self.language_stats[language].lines += lines
        for language, stats in self.language_stats.items():
            self.language_stats[language].percentage = stats.lines / self.total_lines
        return self


class GithubProjectGraph(nx.Graph):
    def __init__(self, gh_stats: 'GithubStats', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gh_stats = gh_stats

    def construct_graph(self) -> 'GithubProjectGraph':
        # create language nodes
        for language, stats in self.gh_stats.language_stats.items():
            self.add_node(language, type='language', lines=stats.lines, percentage=stats.percentage)
        # create project nodes
        for project, lang_stats in self.gh_stats.repo_language_stats.items():
            self.add_node(project, type='repo', **{lang: {'lines': stats.lines, 'percentage': stats.percentage}
                                                   for lang, stats in lang_stats.items()})
            # connect project to its most used language
            most_used_lang = max(lang_stats.keys(), key=lambda lang: lang_stats[lang].lines, default=None)
            if most_used_lang:
                self.add_edge(project, most_used_lang)

        return self

    def get_language_colors(self) -> dict[str, object]:
        return requests.get('https://raw.githubusercontent.com/ozh/github-colors/master/colors.json').json()

    def get_cytoscape_style(self):
        language_colors: dict[str, object] = self.get_language_colors()
        base_styling = [{
            'selector': 'node',
            'css': {
                'content': 'data(name)',
                'text-valign': 'center',
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': 'green',
                'background-color': 'grey'
            }
        },
            {
            'selector': ':selected',
            'css': {
                'background-color': 'black',
                'line-color': 'black',
                'target-arrow-color': 'black',
                'source-arrow-color': 'black',
                'text-outline-color': 'black'
            }}
        ]
        node_stylings = []
        for node in self.nodes:
            node_data = self.nodes[node]
            if node_data['type'] == 'language':
                language = node
                # languages with more projects will be larger
                size = node_data['percentage'] * 90 + 10
                node_stylings.append({'selector': f"node[id = '{language}']",
                                      'style': {
                                          'background-color': language_colors[language]['color'],
                                          'width': size, 'height': size
                                      }})
            elif node_data['type'] == 'repo':
                repo = node
                repo_styling = {'selector': f"node[id = '{repo}']",
                                'style': {}}
                lang_stats = self.gh_stats.repo_language_stats[repo]
                # color project the same as its most used language
                most_used_lang = max(lang_stats.keys(), key=lambda lang: lang_stats[lang].lines, default=None)
                if most_used_lang:
                    repo_styling['style']['background-color'] = language_colors[most_used_lang]['color']
                node_stylings.append(repo_styling)
        return [*base_styling, *node_stylings]


class GithubGraphCacheHandler:
    def __init__(self, gh_integration_key: str, cache_dir: os.PathLike, max_cache_age: float = 10):
        self.gh_integration_key = gh_integration_key
        self.cache_dir = Path(cache_dir)
        self.graph_file = 'gh_project_graph.pickle'
        self.max_cache_age = max_cache_age

    def cache_graph(self, graph: nx.Graph):
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        with open(self.cache_dir / self.graph_file, 'wb') as fp:
            pickle.dump(graph, fp)

    def get_cached_graph(self) -> GithubProjectGraph:
        with open(self.cache_dir / self.graph_file, 'rb') as fp:
            return pickle.load(fp)

    def cache_exists(self) -> bool:
        return (self.cache_dir / self.graph_file).exists()

    def get_cache_age(self) -> float:
        return (time.time() - os.path.getmtime(self.cache_dir / self.graph_file)) / 60

    def get_new_github_graph(self) -> GithubProjectGraph:
        """Parse an entirely new project graph and return it.

        Returns:
            GithubProjectGraph: Graph of github projects and their programming languages.
        """
        gh_stats = GithubStats(self.gh_integration_key).get_stats()
        return GithubProjectGraph(gh_stats).construct_graph()

    def get_graph(self, force_overwrite: bool = False):
        if force_overwrite or not self.cache_exists() or (self.cache_exists() and self.get_cache_age() >= self.max_cache_age):
            print(f"lamma Making new graph via github API. Graph cache exists: {self.cache_exists()}. Cache age: {self.get_cache_age()}")
            project_graph = self.get_new_github_graph()
            self.cache_graph(project_graph)
        else:
            print("lamma Getting cached graph")
            project_graph = self.get_cached_graph()

        return project_graph

    def get_graph_json(self, force_overwrite: bool = False):
        return nx.cytoscape_data(self.get_graph(force_overwrite))['elements']
