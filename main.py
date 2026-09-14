import textwrap

recipes = {}
recipe_name = recipes.keys()
recipe_content = recipes.values()

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

is_command = False


def add_recipe(name, content):
    recipes[name] = content


# NOT WORKING
def print_all_recipes_in_table():
    """Display table-formatted recipes"""
    if not recipes:
        print("\n!!! There's no recipes !!!")
        return

    for name, recipe in recipes.items():
        formatted_recipe = recipe.replace(',', ',\n')
        formatted_recipe = textwrap.indent(formatted_recipe, '   ')
        print(f"\n{name.capitalize()}:\n"
              f"{formatted_recipe}\n--------------------------")


def print_user_manual():
    print(manual_menu)


def format_error():
    format_comunicate = """\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
!!! ERROR: Read the prompt above !!!"""
    print(format_comunicate)
    return


# Main app loop
while True:
    # .strip() deletes unnessesary spaces at the beginning and at the and
    user_input = input(prompt).strip()

    # Check for program exitting command
    if user_input.lower() == '/end' or user_input.lower() == '/exit':
        is_command = True
        print('\n---------------------\n>> Escaped program <<\n---------------------')
        print(f"\n@| You've added {len(recipes)} recipe/s |@")
        break

    # Display all recipes in table
    elif user_input.lower() == '/shall':
        is_command = True
        print_all_recipes_in_table()
        continue

    elif user_input.lower() == '/man':
        is_command = True
        print_user_manual()
        continue

    # Check for white spaces
    if user_input == '':
        is_command = False
        print('\n!!! Nothing to add !!!')
        continue

    if ":" not in user_input:
        format_error()
        continue

    # if everything's ok add recipe
    # split user_input after ":"
    recipe_name, recipipe_content = user_input.split(':', maxsplit=1)
    add_recipe(recipe_name.strip(), recipipe_content.strip())
    print(f'\n> Saved <\n{recipe_name.strip().capitalize()}:\n  {recipipe_content.strip()}')
