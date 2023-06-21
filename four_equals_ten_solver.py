import re
import math
import os

# Global variables
four_digits = ""  # The four digit number of the puzzle
solution_info = {
    "answer_list": [],
    "operator_info": {"plus": 0, "minus": 0, "mult": 0, "div": 0, "parenthesis": 0},
    "pattern_info": {
        "N#N#N#N": 0,
        "(N#N)#N#N": 0,
        "(N#N#N)#N": 0,
        "N#(N#N)#N": 0,
        "N#(N#N#N)": 0,
        "N#N#(N#N)": 0
    }
}


def solver(number_str):
    """
    Given a number as a string, it returns a list of calculations as strings that solve the puzzle
    """
    global solution_info
    solution_info["answer_list"] = []
    solution_info["operator_info"] = {"plus": 0, "minus": 0, "mult": 0, "div": 0, "parenthesis": 0}
    solution_info["pattern_info"] = {
        "N#N#N#N": 0,
        "(N#N)#N#N": 0,
        "(N#N#N)#N": 0,
        "N#(N#N)#N": 0,
        "N#(N#N#N)": 0,
        "N#N#(N#N)": 0
    }

    calculation_templates = [
        "N#N#N#N",
        "(N#N)#N#N",
        "(N#N#N)#N",
        "N#(N#N)#N",
        "N#(N#N#N)",
        "N#N#(N#N)"
    ]
    operators = ["+", "-", "*", "/"]

    # go over all unique permutations of number_str
    for permutation in anagrams(number_str):
        # for each permutation, go over all valid parenthesis positions
        for calculation_template in calculation_templates:
            # replace every N in calculation_template with the
            # corresponding digits from permutation
            index = 0

            def replace_N_in_template(matchobject):
                nonlocal index
                digit = permutation[index]
                index = index + 1
                return digit
            calculation_template_with_numbers = re.sub(
                r'N', replace_N_in_template, calculation_template
            )

            # replace every # in calculation_template with the corresponding
            # operator from the current calculation operators
            calculation_operators = [0, 0, 0]  # it starts as +, +, +
            while calculation_operators is not None:
                index = 0

                def replace_op_in_template(matchobject):
                    nonlocal index
                    operator = operators[calculation_operators[index]]
                    index = index + 1
                    return operator
                calculation = re.sub(
                    r'#', replace_op_in_template, calculation_template_with_numbers
                )

                # add to a list every combination that evaluates to 10
                result = 0
                try:
                    result = eval(calculation)
                except ZeroDivisionError:
                    result = 0
                if result == 10:
                    solution_info["answer_list"].append(calculation)
                    for symbol in [
                        ("plus", "+"),
                        ("minus", "-"),
                        ("mult", "*"),
                        ("div", "/"),
                        ("parenthesis", "(")
                    ]:
                        if calculation.find(symbol[1]) != -1:
                            solution_info["operator_info"][symbol[0]] += 1
                    solution_info["pattern_info"][calculation_template] += 1
                calculation_operators = next_operators(calculation_operators)
    # end for


def anagrams(word):
    """ Generate all of the anagrams of a word. """
    if len(word) < 2:
        yield word
    else:
        for i, letter in enumerate(word):
            if letter not in word[:i]:  # avoid duplicating earlier words
                for j in anagrams(word[:i]+word[i+1:]):
                    yield letter + j


def next_operators(operator_arr):
    """
    Returns the next 3 digit number in base 4
    If opearator_arr is [3, 3, 3], it returns None
    """
    carry = 0
    (operator_arr[2], carry) = base_four_increase(operator_arr[2])
    i = 1
    while carry > 0 and i >= 0:
        (operator_arr[i], carry) = base_four_increase(operator_arr[i])
        i = i - 1
    return operator_arr if carry == 0 else None


def base_four_increase(num):
    """
    returns the tuple (result, carry)
    """
    return ((num + 1) % 4, math.floor((num + 1) / 4))


# menu functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_title():
    print("-----------------")
    print("4=10 solver")
    print("-----------------")


def print_main_menu():
    clear_screen()
    show_title()
    if four_digits == "":
        print("Choose option 1 to enter a number to solve its puzzle.")
    else:
        print(f"Currently solving for {four_digits}.")
    print("Note that due to the mathematical properties of some operations, "
          "sometimes multiple solutions to a puzzle may be practically identical")
    print("-----------------")
    print("1. Enter a number and generate solutions")
    print("2. Show solutions")
    print("3. Show parenthesis placement for solutions")
    print("4. Show full operator info")
    print("5. Hint: is + used?")
    print("6. Hint: is - used?")
    print("7. Hint: is * used?")
    print("8. Hint: is / used?")
    print("9. Hint: are parenthesis used?")
    print("10. Exit")
    print("-----------------")


def get_user_choice():
    choice = input(">> ")
    return choice.strip()


def process_choice_main_menu(choice):
    if choice == "1":
        enter_number_menu()
    # Ignore options about solutions unless a number is entered
    elif four_digits != "" and choice in ["2", "3", "4", "5", "6", "7", "8", "9"]:
        show_info_menu(choice)
    elif choice == "10":
        clear_screen()
        exit()


def enter_number_menu():
    global four_digits
    four_digits = ""
    while four_digits == "":
        clear_screen()
        show_title()
        print("Please enter a four digit number (i.e 5678).")
        print()
        num_input = input(">> ")
        if re.match(r'^\d{4}$', num_input):
            four_digits = num_input
    solver(four_digits)


def show_info_menu(info_choice):
    choice = ""
    while choice != "1":
        clear_screen()
        show_title()
        if info_choice == "2":
            show_answer_list()
        elif info_choice == "3":
            show_pattern_info()
        elif info_choice == "4":
            show_full_operator_info()
        elif info_choice in ["5", "6", "7", "8", "9"]:
            show_is_op_used_info(info_choice)
        print("1. Exit")
        print("-----------------")
        print()
        choice = get_user_choice()


def show_answer_list():
    i = 1
    print("Solutions:\n")
    for answer in solution_info["answer_list"]:
        print(f"{str(i)}) {answer}")
        i += 1
    if (len(solution_info["answer_list"]) == 0):
        print("This puzzle has no solutions.")
    print()


def show_pattern_info():
    print("Parenthesis placement for solutions:\n")
    print("N represents a digit and # represents an operator.\n")
    for k, v in solution_info["pattern_info"].items():
        print(f"- The parenthesis pattern {k} is used in {v} solution{'s' if v != 1 else ''}.")
    print()


def show_full_operator_info():
    print("Full operator info:\n")
    for k, v in solution_info["operator_info"].items():
        if k == "plus":
            print(f"- plus (+) signs are used in {v} solution{'s' if v != 1 else ''}.")
        elif k == "minus":
            print(f"- minus (-) signs are used in {v} solution{'s' if v != 1 else ''}.")
        elif k == "mult":
            print(f"- multiplication (*) signs are used in {v} solution{'s' if v != 1 else ''}.")
        elif k == "div":
            print(f"- division (/) signs are used in {v} solution{'s' if v != 1 else ''}.")
        elif k == "parenthesis":
            print(f"- parenthesis are used in {v} solution{'s' if v != 1 else ''}.")
    print()


def show_is_op_used_info(choice):
    print("Is it used?\n")
    operator = {"5": "plus", "6": "minus", "7": "mult", "8": "div", "9": "parenthesis"}[choice]
    usage = solution_info["operator_info"][operator]
    if usage > 0:
        if operator == "parenthesis":
            print(f"- parenthesis are used in {usage} solution{'s' if usage != 1 else ''}.")
        elif operator == "plus" or operator == "minus":
            print(
                f"- {operator} signs are used in {usage} solution{'s' if usage != 1 else ''}."
            )
        elif operator == "mult":
            print(
                f"- multiplication signs are used in {usage} solution{'s' if usage != 1 else ''}."
            )
        elif operator == "div":
            print(f"- division signs are used in {usage} solution{'s' if usage != 1 else ''}.")
    else:
        if operator == "parenthesis":
            print("- Parenthesis are not used in any solutions.")
        else:
            print("- This sign is not used in any solutions.")
    print()


def main():
    while True:
        print_main_menu()
        print()
        choice = get_user_choice()
        process_choice_main_menu(choice)


if __name__ == '__main__':
    main()
