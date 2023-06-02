import sys
import re
import math

def solver(number_str):
    """
    Given a number as a string, it returns a list of calculations as strings that solve the puzzle
    """
    answer_list = []
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
            calculation_template = re.sub(r'N', replace_N_in_template, calculation_template)

            # replace every # in calculation_template with the corresponding
            # operator from the current calculation operators
            calculation_operators = [0, 0, 0] # it starts as +, +, +
            while calculation_operators != None:
                index = 0
                def replace_op_in_template(matchobject):
                    nonlocal index
                    operator = operators[calculation_operators[index]]
                    index = index + 1
                    return operator
                calculation = re.sub(r'#', replace_op_in_template, calculation_template)

                # add to a list every combination that evaluates to 10
                result = 0
                try:
                    result = eval(calculation)
                except ZeroDivisionError:
                    result = 0
                if result == 10:
                    answer_list.append(calculation)
                calculation_operators = next_operators(calculation_operators) 
    # end for
    return answer_list         

def anagrams(word):
    """ Generate all of the anagrams of a word. """ 
    if len(word) < 2:
        yield word
    else:
        for i, letter in enumerate(word):
            if not letter in word[:i]: # avoid duplicating earlier words
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

def main():
    """
    The script is run with 1 argument:
    argv[1] is a 4 digit number representing the puzzle to solve
    """
    if len(sys.argv) < 2:
        print("Error: missing argument (4 digit number)")
        sys.exit(1)
    if not re.match(r'^\d{4}$', sys.argv[1]):
        print("Error: input must be a four digit number")
        sys.exit(1)

    number_str = sys.argv[1]

    # get the answers
    answer_list = solver(number_str)

    # ToDo: cli menu
    print(answer_list)
  
if __name__ == '__main__':
    main()
