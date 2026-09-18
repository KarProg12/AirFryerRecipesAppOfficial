import textwrap
import difflib

recipes = {}

prompt = f"""\n-----------------------------------------------------
Enter the recipe in this order:
  'KEY: recipe_name' : 'VALUE: recipe_content'
Type ['/help'] to show available commands.
You can also search in recipes or in recipes ingredients.
-----------------------------------------------------
[~! REMEMBER ABOUT CORRECT recipe FORMAT !~]
\n>>> """

def nothing_to_add() -> None:
    """Func that displays communicate 'Nothing to add'"""
    print("\n!!! Nothing to add !!!")

def no_recipes() -> None:
    print("\n!!! There's no recipes yet !!!")

def print_format_error() -> None:
    format_communicate = """\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
!!! ERROR: Read the prompt above !!!"""
    print(format_communicate)

user_help_menu = """
> Type ['/end'] or ['/exit'] to escape the program.
> Type ['/shall'] to display all recipes in table.
> Type ['/nameSearch'] to search the recipe by its name 
> Type ['/ingrSearch'] to search in the recipes by ingredients
> Type ['/del'], ['/delete'] or ['/rm'] 
    to enter the deleting by name mode."""

def print_user_manual() -> None:
    """Func for displaying user manual"""
    print(user_help_menu)

def add_recipe(name, content) -> None:
    """Func for adding recipes"""
    recipes[name.strip().lower()] = content

def del_recipe() -> None:
    """Deletes the recipe by name"""
    if not recipes:
        no_recipes()
        return

    name_of_recipe = input("\n>>> Enter recipe name to delete\n>>> ").strip().lower()

    deleted_recipe = recipes.pop(name_of_recipe, None)

    # If match is equal to user input delete recipe
    if deleted_recipe is not None:
        print(f"\n> Successfully removed: {name_of_recipe.capitalize()} <")
        return

    # If there was no accurate input then check for typos and ask user
    matches = difflib.get_close_matches(name_of_recipe, recipes.keys(), cutoff=0.6)

    print(f"\n!!! Error 404: Not found: {name_of_recipe.capitalize()} !!!")

    if matches:
        confirm = input(f"\n??? Did you mean {matches[0].capitalize()}? [y/N]\n>>> ").strip().lower()
        # If user confirms delete the recipe
        if confirm in ['y', 'yes']:
            recipes.pop(matches[0])
            print(f"\n> Successfully removed: {matches[0].capitalize()} <")

        print("\n??? Did you mean:\n=================")
        for match in matches:
            print(f"  > {match.capitalize()}")

def search_by_name() -> None:
    """Searches precisely recipe by its name"""
    # Check if there's no recipes
    if not recipes:
        no_recipes()
        return

    # Store the input in search_query variable
    search_query = input("\n>>> Enter the recipe name to search (allows typos)\n>>> ").strip().lower()

    # matches = close matches to search_query(input) searching in the names(keys)
    # of recipes cutoff (max tolerance for typos = 0, no tolerance for typos 1)
    matches = difflib.get_close_matches(search_query, recipes.keys(), cutoff=0.6)

    # If there are matches
    if matches:
        print("\n??? Did you mean:\n=================")
        # Display close formatted matches
        for match in matches:
            print(f"\n> {match.capitalize()}:\n  {recipes[match]}")
    else:
        print(f"\n!!! Error 404: Not found: {search_query} !!!")

def search_by_ingredient() -> None:
    if not recipes:
        no_recipes()
        return

    search_query = input("\n>>> Enter the recipe's ingredient you want to search (allows typos)\n>>> ").strip().lower()

    matches = difflib.get_close_matches(search_query, recipes.values(), cutoff=0.5)

    if matches:
        print("\n??? Did you mean:\n=================")
        for match in matches:
            print(f"\n> {match}")
    else:
        print(f"\n!!! Error 404: Not found: {search_query} !!!")

# Print all recipes in table
def print_all_recipes_in_table() -> None:
    """Display nice table-formatted recipes"""
    if not recipes:
        no_recipes()
        return

    # Widths of columns for name and content of the recipes
    col_name_width = 20
    col_content_width = 40

    # Top table frame
    print(f"\n┌{'─' * col_name_width}┬{'─' * col_content_width}┐")
    print(f"│ {'Recipe Name':<{col_name_width - 1}}│ {'Ingredients / Content':<{col_content_width - 1}}│")
    print(f"├{'─' * col_name_width}┼{'─' * col_content_width}┤")

    for name, recipe in recipes.items():
        # Divide long recipe on the list to avoid table's bad formatting
        wrapped_content = textwrap.wrap(recipe, width=col_content_width - 2)

        # First line with recipe name
        first_line = wrapped_content[0] if wrapped_content else ""
        print(f"│ {name.capitalize():<{col_name_width - 1}}│ {first_line:<{col_content_width - 1}}│")

        # Next lines of the recipe (if the text was too long, and it has been wrapped)
        for line in wrapped_content[1:]:
            print(f"│ {'':<{col_name_width - 1}}│ {line:<{col_content_width - 1}}│")

        print(f"├{'─' * col_name_width}┼{'─' * col_content_width}┤")

    # Deleting the last separating line and closing the bottom of the table
    # (The loop above prints a line after each recipe so overwrite the last one with a bottom border)
    print(f"└{'─' * col_name_width}┴{'─' * col_content_width}┘")



# ---MAIN-APP-LOOP---
while True:

    try:
        # .strip() deletes unwanted spaces at the beginning and at the end
        user_cmd = input(prompt).strip()
    # If user's input is Ctrl + C or Ctr + D escape the program without any errors and print summary of recipes
    except(EOFError, KeyboardInterrupt):
        print('\n---------------------\n>> Escaped program <<\n---------------------')
        print(f"\n@| You've added {len(recipes)} recipe/s |@")
        break

    # ---COMMANDS---
    match user_cmd.lower():
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
        case '/namesearch':
            search_by_name()
            continue
        case '/ingrsearch':
            search_by_ingredient()
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
        print_format_error()
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
    print(f'\n> Saved <\n{recipe_name.strip().capitalize()}:\n  {recipe_content}')
