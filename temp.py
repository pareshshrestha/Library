def is_yes(prompt:str) -> bool:
    while True:
        user_input = input(prompt)
        user_input = user_input.strip().lower()
        if user_input.startswith("y"):
            return True
        elif user_input.startswith("n"):
            return False
        else:
            print("Please enter Y or N only.")

print(is_yes("Do you like Python? (Y/N): "))