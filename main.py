import textwrap

recipes = {}

prompt = f"""\n-----------------------------------------------------
Enter the recipe in this order:
  'KEY: recipe_name' : 'VALUE: recipe_content'
Type ['/man'] to show user manual.
-----------------------------------------------------
[~! REMEMBER ABOUT CORRECT recipe FORMAT !~]
\n>>>"""

manual_menu = """
> Type ['/end'] or ['/exit'] to escape the program.
> Type ['/shall'] to display all recipes in table."""


def nothing_to_add():
    print("!!! Nothing to add !!!")


def add_recipe(name, content):
    recipes[name] = content


# NOT WORKING
def print_all_recipes_in_table():
    """Display table-formatted recipes"""
    if not recipes:
        print("\n!!! There's no recipes yet !!!")
        return

    for name, recipe in recipes.items():
        formatted_recipe = recipe.replace(',', ',\n')
        formatted_recipe = textwrap.indent(formatted_recipe, '  ')
        print(f"\n{name.capitalize()}:\n"
              f"{formatted_recipe}\n--------------------------")


def print_user_manual():
    print(manual_menu)


def format_error():
    format_communicate = """\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
!!! ERROR: Read the prompt above !!!"""
    print(format_communicate)
    return


# Main app loop
while True:
    # .strip() deletes unwanted spaces at the beginning and at the end
    user_cmd = input(prompt).strip()

    # ---COMMANDS-CHECKS---
    # Check for program exiting command
    if user_cmd.lower() == '/end' or user_cmd.lower() == '/exit':
        print('\n---------------------\n>> Escaped program <<\n---------------------')
        print(f"\n@| You've added {len(recipes)} recipe/s |@")
        break

    # Display all recipes in table (for now it is primitive)
    elif user_cmd.lower() == '/shall':
        print_all_recipes_in_table()
        continue

    # Check for /man (user manual command)
    elif user_cmd.lower() == '/man':
        print_user_manual()
        continue

    # ---ERRORS-PREDICTING---
    # Check for white spaces
    if user_cmd == '':
        nothing_to_add()
        continue

    # If ":" is not in user's input print error about incorrect recipe format
    if ":" not in user_cmd:
        format_error()
        continue

    # if everything's ok add recipe
    # split user_cmd after ":"
    recipe_name, recipe_content = user_cmd.split(':', maxsplit=1)

    # Check if user typed recipe without name or only recipe name without content and display communicate
    if not recipe_name.strip() or not recipe_content.strip():
        nothing_to_add()
        continue

    # After all validations above if everything is ok add recipe to dict
    add_recipe(recipe_name.strip(), recipe_content.strip())
    print(f'\n> Saved <\n{recipe_name.strip().capitalize()}:\n  {recipe_content.strip()}')
