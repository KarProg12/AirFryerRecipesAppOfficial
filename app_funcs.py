import textwrap
import difflib

recipes = {}

def greet_user():
    print("\n$$$ WELCOME TO THE AIR FRYER RECIPE APP $$$")

def nothing_to_add() -> None:
    """Func that displays communicate 'Nothing to add'"""
    print("\n!!! Nothing to add !!!")

def no_recipes() -> None:
    print("\n!!! There's no recipes yet !!!")

def print_format_error() -> None:
    format_communicate = """\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
!!! ERROR: Read the prompt above !!!"""
    print(format_communicate)

def print_user_manual() -> None:
    """Func for displaying user manual"""
    user_manual = """
    > Type ['/end'] or ['/exit'] to escape the program.
    > Type ['/shall'] to display all recipes in table.
    > Type ['/nameSearch'] to search the recipe by its name 
    > Type ['/ingrSearch'] to search in the recipes by ingredients
    > Type ['/del'], ['/delete'] or ['/rm'] 
        to enter the deleting by name mode."""
    print(user_manual)

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
        confirm = input(f"\n??? Did you mean: '{matches[0].capitalize()}'? [y/N]\n>>> ").strip().lower()
        # If user confirms delete the recipe
        if confirm in ['y', 'yes']:
            recipes.pop(matches[0])
            print(f"\n> Successfully removed: {matches[0].capitalize()} <")

        else:
            print("\n>> Removal cancelled <<")

def search_by_name() -> None:
    """Searches precisely recipe by its name"""
    # Check if there's no recipes
    if not recipes:
        no_recipes()
        return

    # Store the input in search_query variable
    search_query = input("\n>>> Enter the recipe name to search (allows typos)\n>>> ").strip().lower()

    # If there are matches
    if matches := difflib.get_close_matches(search_query, recipes.keys(), cutoff=0.6):
        print("\n??? Did you mean:\n=================")
        # Display close formatted matches
        for match in matches:
            print(f"\n> {match.capitalize()}:\n\t{recipes[match]}")
    else:
        print(f"\n!!! Error 404: Not found: {search_query} !!!")

def search_by_ingredient() -> None:
    if not recipes:
        no_recipes()
        return

    search_query = input("\n>>> Enter the recipe's ingredient you want to search (allows typos)\n>>> ").strip().lower()

    # List of found accurate matches
    matches = []

    # Iteration by every recipe in recipes
    for name, content in recipes.items():
        # If there is accurate input or difflib has found close matches
        if search_query in content.lower() or difflib.get_close_matches(search_query, content.lower().split(), cutoff=0.6):
            # Add recipe name and content to matches list as a tuple
            matches.append((name, content))

    if matches:
        print("\n??? Did you mean:\n=================")
        for name, content in matches:
            print(f"\n> {name.capitalize()}:\n\t{content}")
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