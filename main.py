import requests


class User:
    def __init__(self, username, profile_url, public_repos, followers, following):
        self.username = username
        self.profile_url = profile_url
        self.public_repos = public_repos
        self.followers = followers
        self.following = following

    def __repr__(self):
        return (f"User(username={self.username}, profile_url={self.profile_url}, "
                f"public_repos={self.public_repos}, followers={self.followers}, following={self.following})")


def get_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        user = User(
            username=user_data['login'],
            profile_url=user_data['html_url'],
            public_repos=user_data['public_repos'],
            followers=user_data['followers'],
            following=user_data['following']
        )
        return user
    else:
        print(f"Erro ao buscar dados do usuário {username}: {response.status_code}")
        return None


def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repos_data = response.json()
        repos_dict = {repo['name']: repo['html_url'] for repo in repos_data}
        return repos_dict
    else:
        print(f"Erro ao buscar repositórios do usuário {username}: {response.status_code}")
        return None


def user_report(user, repos):
    filename = f"{user.username}.txt"
    with open(filename, 'w') as file:
        file.write(f"Nome: {user.username}\n")
        file.write(f"Perfil: {user.profile_url}\n")
        file.write(f"Número de repositórios publicos: {user.public_repos}\n")
        file.write(f"Número de seguidores: {user.followers}\n")
        file.write(f"Número de usuários seguidos: {user.following}\n")
        file.write("Repositórios:\n")
        for repo_name, repo_url in repos.items():
            file.write(f"{repo_name}: {repo_url}\n")
    print(f"Relatório gerado: {filename}")


if __name__ == "__main__":
    username = "octocat"

    # Obter os dados do usuário
    user = get_user(username)
    if user:
        print(user)

        # Obter os repositórios do usuário
        repos = get_user_repos(username)
        if repos:
            print(repos)
            # Gerar o relatório do usuário
            user_report(user, repos)


import unittest

class TestMethods(unittest.TestCase):
    """Classe de testes unitários."""

    def test_user_class_has_minimal_parameters(self):
        """
        Teste unitário relativo ao primeiro passo do desafio.
        """
        parameters = [
            'username', 'profile_url', 'public_repos', 'followers', 'following'
        ]
        user = get_user('octocat')
        self.assertIsNotNone(user)
        for param in parameters:
            self.assertTrue(hasattr(user, param))

    def test_user_class_invalid_parameters(self):
        """
        Teste unitário para verificar se a função lida corretamente com um nome de usuário inválido.
        """
        invalid_username = 'invalidusername1234567890'
        user = get_user(invalid_username)
        self.assertIsNone(user)

    def test_user_repos_invalid_parameters(self):
        """
        Teste unitário para verificar se a função lida corretamente com um nome de usuário inválido.
        """
        invalid_username = 'invalidusername1234567890'
        user = get_user_repos(invalid_username)
        self.assertIsNone(user)


    def test_empty_repositories(self):
        """
        Teste unitário para verificar se a função lida corretamente com repositório vazio.
        """
        empty_repos_username = 'coutinhoKleber'  #usuário não possui repositórios
        repos = get_user_repos(empty_repos_username)
        self.assertIsNotNone(repos)



if __name__ == "__main__":
    unittest.main()
