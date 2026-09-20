# ---IMPORTS---
import app_funcs


prompt = f"""\n---------------------------------------------------------
Enter the recipe in this order:
  'KEY: recipe_name' : 'VALUE: recipe_content'
Type ['/help'] to show available commands.
You can also search in recipes or in recipes ingredients.
---------------------------------------------------------
[~! REMEMBER ABOUT CORRECT recipe FORMAT !~]
\n>>> """

app_funcs.greet_user()



# ---MAIN-APP-LOOP---
while True:

    try:
        # .strip() deletes unwanted spaces at the beginning and at the end
        user_cmd = input(prompt).strip()
    # If user's input is Ctrl + C or Ctr + D escape the program without any errors and print summary of recipes
    except(EOFError, KeyboardInterrupt):
        print('\n---------------------\n>> Escaped program <<\n---------------------')
        print(f"\n@| You've added {len(app_funcs.recipes)} recipe/s |@")
        break

    # ---COMMANDS---
    match user_cmd.lower():
        case '/end' | '/exit':
            print('\n---------------------\n>> Escaped program <<\n---------------------')
            print(f"\n@| You've added {len(app_funcs.recipes)} recipe/s |@")
            break
        case '/help':
            app_funcs.print_user_manual()
            continue
        case '/shall':
            app_funcs.print_all_recipes_in_table()
            continue
        case '/namesearch':
            app_funcs.search_by_name()
            continue
        case '/ingrsearch':
            app_funcs.search_by_ingredient()
            continue
        case '/delete' | '/del' | '/rm':
            app_funcs.del_recipe()
            continue

        # ---ERRORS-PREDICTING---
        # Check for white spaces
        case '':
            app_funcs.nothing_to_add()
            continue

    # If ":" is not in user's input print error about incorrect recipe format
    if ":" not in user_cmd:
        app_funcs.print_format_error()
        continue

    # if everything's ok add recipe
    # split user_cmd after ":"
    recipe_name, recipe_content = user_cmd.split(':', maxsplit=1)

    # Check if user typed recipe without name or only recipe name without content and display communicate
    if not recipe_name.strip() or not recipe_content.strip():
        app_funcs.nothing_to_add()
        continue

    # After all validations above if everything is ok add recipe to dict
    app_funcs.add_recipe(recipe_name.strip(), recipe_content.strip())
    print(f'\n> Saved <\n{recipe_name.strip().capitalize()}:\n  {recipe_content}')
