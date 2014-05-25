import ast
import sys
from io import StringIO
# This class should receive a list of statements, evaluate them and return an appropriate response.


class CodeRunner:

    def __init__(self):
        # constructor
        foo = 0 # placeholder


    def compile_tree(self, tree):
        return compile(tree, '<this is doge>', 'exec')

    def execute(self, program_text):
        ''' Run the given program. Returns a tuple (output, error) where output is the program's output
        (caught from stdout) and error is the name of the error thrown (None if there was no error).
        '''
        # Make the output go to file-like string objects
        code_output = StringIO()
        error = None

        try:
            # Try to parse, compile and execute the code

            tree = ast.parse(program_text)
            code_object = self.compile_tree(tree)

            sys.stdout = code_output  # Make the output go to a file-like string object


            exec(code_object)
            sys.stdout = sys.__stdout__  # Restore stdout

            print("EXECUTION SUCCESSFUL")
        except Exception as e:
            # If an exception occurred, remember it

            sys.stdout = sys.__stdout__  # Restore stdout

            error = e.__class__.__name__
            print("EXCEPTION: " + e.__class__.__name__)

        return code_output.getvalue(), error