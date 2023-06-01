import sys
import re

def solver(number_str):
  """
  Given a number as a string, it returns a list of calculations as strings that solve the puzzle
  """
  answer_list = []

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
  
if __name__ == '__main__':
    main()
