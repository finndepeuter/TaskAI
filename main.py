# import of streamlit to use for the webapplication
import streamlit as st

# creation of some variable containers and columns to contain the parts of the webapplication
header = st.container()
input = st.container()
solution = st.container()
puzzle , solvedPuzzle = st.columns(2)
# creation of the variables needed to store the solutions
factor1 = 0
factor2 = 0
result = 0

# implement the header part on the webpage
with header:
    st.title("Task 01 AI: Finn De Peuter")

# implement the container with a title and 3 input fields
with input:
    st.header("Choose two words for your puzzle and the result it has to give")
    # we ask for the input of the user for the two words to add and the answer it's supposed to give
    first = st.text_input("First word")
    second = st.text_input("Second word")
    answer = st.text_input("Result")
    

from simpleai.search import CspProblem, backtrack
# if statement needed to not get errors when one of the variables isn't filled in
if first and second and answer:
# we put these words into a set to create a list of variables with just the letters and no duplicates
    variables = set(first + second + answer)
# print the variables just to see what they are
    print(variables)

# we create the domains
    domains = {
        char: list(range(1, 10)) # we loop through the characters in the variables
        if char == first[0] or char == answer[0] or char == second[0] # if it's the first letter of a word we use the range as 1 to 9
        else list(range(10)) for char in variables # else we also include 0
    }

    def constraint_unique(variables, values):
        return len(values) == len(set(values))  # remove repeated values and count

    def constraint_add(variables, values):
        # create the placeholders for the needed entities and make them global so they update with each iteration
        global factor1, factor2, result
        factor1 = 0 
        factor2 = 0
        result = 0
        # we loop through the characters of the each word and match them to their index in the variables list
        for char in first:
            index = variables.index(char) # we retrieve the index of the letter to the variables list
            factor1 = factor1 * 10 + values[index] # we add the value to the factor1 and move to the left each iteration

        for char in second:
            index = variables.index(char)
            factor2 = factor2 * 10 + values[index] 

        for char in answer:
            index = variables.index(char)
            result = result * 10 + values[index]
        # we always multiply by ten to make sure it always moves one place to the left so 3 becomes 30 for example

        return (factor1 + factor2) == result # we check to see if the two factors combined create the result

    # the constraints needed
    constraints = [
        (variables, constraint_unique),
        (variables, constraint_add),
    ]

    problem = CspProblem(variables, domains, constraints)

    output = backtrack(problem)
    print('\nSolutions:', output)    

    # container with the solution of the puzzle 
    # if we have a solution, display the rest of the code
    if output:
        with solution:
            st.subheader("Solution")
        # write the assignment
        with puzzle:
            st.markdown(
            f"""
            <div style="border: 2px solid #0077b6; border-radius: 5px; background-color: lightyellow; text-align: center;">
                <p style="font-weight: bold;">{first}</p>
                <p style="font-weight: bold;">+ {second}</p>
                <p style="font-weight: bold;">= {answer}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
        # write the solution
        with solvedPuzzle:
            st.markdown(
            f"""
            <div style="border: 2px solid #0077b6; border-radius: 5px; background-color: lightyellow; text-align: center;">
                <p style="font-weight: bold;">{factor1}</p>
                <p style="font-weight: bold;">+ {factor2}</p>
                <p style="font-weight: bold;">= {result}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
           
        # write the solution in the format of a table
        st.write("Each letter with their corresponding value:")
        st.dataframe(output)
    else:
        with solution:
            st.subheader("No solution for this puzzle, choose something else")    
        