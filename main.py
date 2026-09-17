import textwrap
import difflib

recipes = {}

prompt = f"""\n-----------------------------------------------------
Enter the recipe in this order:
  'KEY: recipe_name' : 'VALUE: recipe_content'
Type ['/help'] to show available commands.
-----------------------------------------------------
[~! REMEMBER ABOUT CORRECT recipe FORMAT !~]
\n>>> """

def nothing_to_add() -> None:
    """Func that displays communicate 'Nothing to add'"""
    print("\n!!! Nothing to add !!!")

def format_error() -> None:
    format_communicate = """\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
!!! ERROR: Read the prompt above !!!"""
    print(format_communicate)

user_help_menu = """
> Type ['/end'] or ['/exit'] to escape the program.
> Type ['/shall'] to display all recipes in table.
> Type ['/find'] or [/'search'] to search the recipe (with close matches and allowing typos)
> Type ['/del'], ['/delete'] or ['/rm'] 
   to enter the deleting by name mode 
   (SUGGESTION: first type ['/shall'] to show what's the name of the recipe)."""

def print_user_manual() -> None:
    """Func for displaying user manual"""
    print(user_help_menu)

def add_recipe(name, content) -> None:
    """Func for adding recipes"""
    recipes[name] = content

def del_recipe() -> None:
    """Deletes the recipe by name"""
    if not recipes:
        print("\n!!! There's no recipes yet !!!")
        return

    name_of_recipe = input("\n>>> Enter recipe name to delete\n>>> ").strip().lower()

    # First try to delete recipe if user's input is accurate
    deleted_recipe = recipes.pop(name_of_recipe, None)

    # If user's input is accurate end the func
    if deleted_recipe is not None:
        print(f"\n> Successfully removed: {name_of_recipe.capitalize()} <")
        return

    # If user's input was not accurate search for similar matches
    matches = difflib.get_close_matches(name_of_recipe, recipes.keys(), cutoff=0.5)

    print(f"\n!!! Error 404: Not found: {name_of_recipe.capitalize()} !!!")

    if matches:
        print("??? Did you mean one of these:")
        for match in matches:
            print(f"  > {match.capitalize()}")

def search_recipe() -> None:
    """Searches precisely recipe by its name"""
    # Check if there's no recipes
    if not recipes:
        print("\n!!! There's no recipes yet !!!")
        return

    # Store the input in search_query variable
    search_query = input("\n>>> Enter the recipe name to search (allows typos)\n>>> ")

    # matches = close matches to search_query(input) searching in the names(keys)
    # of recipes with precision 0.5 (min = 0, max = 1)
    matches = difflib.get_close_matches(search_query, recipes.keys(), cutoff=0.5)

    # If there are matches
    if matches:
        print("\n??? Did you mean:")
        # Display close formatted matches
        for match in matches:
            print(f"\n> {match.capitalize()}:\n  {recipes[match]}")
    # If there's no matches
    else:
        print(f"\n!!! No close matches for {search_query.capitalize()} found !!!")

# Print all recipes in table
def print_all_recipes_in_table() -> None:
    """Display table-formatted recipes"""
    if not recipes:
        print("\n!!! There's no recipes yet !!!")
        return

    for name, recipe in recipes.items():
        formatted_recipe = recipe.replace(',', ',\n')
        formatted_recipe = textwrap.indent(formatted_recipe, '  ')
        print(f"\n{name.capitalize()}:\n"
              f"{formatted_recipe}\n--------------------------")



# ---MAIN-APP-LOOP---
while True:

    try:
        # .strip() deletes unwanted spaces at the beginning and at the end
        user_cmd = input(prompt).strip().lower()
    # If user's input is Ctrl + C or Ctr + D escape the program without any errors and print summary of recipes
    except(EOFError, KeyboardInterrupt):
        print('\n---------------------\n>> Escaped program <<\n---------------------')
        print(f"\n@| You've added {len(recipes)} recipe/s |@")
        break

    # ---COMMANDS-CHECKS---
    match user_cmd:
        case '/end' | '/exit':
            print('\n---------------------\n>> Escaped program <<\n---------------------')
            print(f"\n@| You've added {len(recipes)} recipe/s |@")
            break
        case '/help':
            print_user_manual()
            continue
        case '/shall':
            print_all_recipes_in_table()
            continue
        case '/search' | '/find':
            search_recipe()
            continue
        case '/delete' | '/del' | '/rm':
            del_recipe()
            continue

        # ---ERRORS-PREDICTING---
        # Check for white spaces
        case '':
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
