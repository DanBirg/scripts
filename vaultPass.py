import os
import requests
import sys

if sys.version_info[0] > 2:
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
else:
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def gen_token():
    """
    This Method takes the Vault role_id and the secret_id from environment variables and generates API Token.
    """
    url = 'utl_for_login'
    # Secret and role id's will be provided by the Vault administrators
    #print(os.environ) # For debug only
  
    role_id = os.environ["VAULT_ROLE_ID"] # Create an environment variable
    secret_id = os.environ["VAULT_SECRET_ID"] # Create an environment variable

    params = {"role_id": role_id, "secret_id": secret_id}

    response = requests.post(url=url, data=params).json()
    auth = response['auth']
    client_token = auth['client_token']

    # Remove on production
    #print(client_token)
    return client_token


def get_secret(token, secret_path, secret_name):
    """
    This method receives a token, secret path, and secret name and returns the secret data.
    """
    #url = f'https://vault.com/v1/{secret_path}/data/{secret_name}'
    url = "https://vault.com/v1/{:s}/data/{:s}".format(secret_path, secret_name)
    headers = {'X-Vault-Token': token}
    response = requests.get(url=url, headers=headers).json()
    data = response['data']

    # Remove on production
    #print(data)
    return data


def main():
    token = gen_token()
    return get_secret(token, 'it/secrets', 'switches')


if __name__ == '__main__':
    main()
