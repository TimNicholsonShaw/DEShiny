from shiny.express import input, ui, render
from yaml import safe_load


with open(".secrets.yaml", "r") as file:
    secret_password = safe_load(file)["password"]
ui.input_password("password", "Password:")

def check_auth():
    return input.password() == secret_password
@render.text
def test():
    return check_auth()