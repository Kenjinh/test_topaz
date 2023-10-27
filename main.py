import os
import requests
from dotenv import load_dotenv
load_dotenv()


def get_user():
    """
    Retrieves user information from the GitHub API.

    Returns:
        The JSON response containing user information.

    Raises:
        Exception: If an error occurs during the API request.
    """
    try:
        response = requests.get(url=f"{os.getenv('GITHUB_API_URL')}/user", headers={"Authorization": f"Bearer {os.getenv('TOKEN')}"})
        return response.json()
    except Exception as error:
        return error 



def get_repos(user):
    """
    Retrieves a list of repositories for a given user.

    Parameters:
        user (str): The username of the user for whom to retrieve the repositories.

    Returns:
        str: A string containing information about the repositories, including the ID, name, and URL of each repository.
    """
    repos = """"""
    try:
        response = requests.get(url=f"{os.getenv('GITHUB_API_URL')}/users/{user}/repos")
    except Exception as error:
        return error 
    
    for rep in response.json():
        repos+=(
        f"  ID: {rep['id']}\n"
        f"  Nome: {rep['name']}\n"
        f"  url: {rep['svn_url']}\n"
    )
    return repos
def main():
    """
    This function retrieves user information from an API and writes it to a text file.
    It does not take any parameters.
    It does not return any value.
    """
    user = get_user()
    repos = get_repos(user['login'])
    content = (
        f"Nome: {user['name']}\n"
        f"Perfil: {user['login']}\n"
        f"Número de repositórios publicos: {user['public_repos']}\n"
        f"Número de seguidores: {user['followers']}\n"
        f"Número de usuários seguidos: {user['following']}\n"
        f"Lista da Repositórios:\n"
        f"{repos}"
    )
    with open(f"{user['login']}.txt", "w") as file:
        file.write(content)

if __name__ == '__main__':
    main()