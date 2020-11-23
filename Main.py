"""
Roberto Rivera Terán    - A00369870
Karla Paola García      - A01655768

    OBJECTIVE

        Make a program  that  reads  from  a  .txt file  the  elements  that  define  a  context-free grammar and
        apply the top-down parsing process for strings given by the user

        The grammar will be defined in a txt file. The file shall be defined as follows:

        -The first line indicates the set of non-terminal symbols separated by commas, only one uppercase character.
        -The second line indicates the set of terminal symbols separated by commas, only one lowercase character.
        -The third line indicates the start symbol.
        -The following lines indicate the productions of the grammar in the following format:

            simboloNoTerminal -> chain terminals or non-terminal symbol

       Lambda cannot appear as body of any production. The top-down parsing process that recieves  a string and an
       integer. The integer indicates the maximum depth of the parsing tree. If this depth is exceeded, you must
       stop the process indicating that no solution was found for the string.

       The outcome of the process must be the parsing tree.

    CONTENTS

    !   Inputs                              at line 183

    !   Extract information on .txt file    at line 195

    !   Top-Down Parsing process            at line 44

    !   Print Tree                          at line 142

"""
"""
    LIBRARIES:

    -import pptree:
        This package allows to pretty-print a tree of python objects. Will be using their Tree properties as well
        as the object Node in order to build said tree
"""
from pptree import *
"""
    TopDownParsing( Array       non-terminal symbols, 
                    Array       terminal symbols, 
                    String      Initial sate, 
                    Dictionary  productions of the grammar, 
                    String      string to validate, 
                    Int         maximum search Depth
                    ):
                    
    This function performs the Top-Down Parsing process and after finishing it, prints the corresponding tree
    
"""
def TopDownParsing(nonTerminal, terminal, initialState, productions, string, maxDepth):
    print("_________TopDownParsing Approach_________")
    print(" ")
    foundSearchedString = False
    maxDepthReached = False

    queue= []
    queue.append(initialState)

    Tree= {}

    reason=""

    depthDictionaryValues = {}
    depthDictionaryValues[initialState] = 0
    while queue and not foundSearchedString:
        done= False
        Q= queue.pop(0)

        #print(str(depthDictionaryValues[Q]))

        currentDepth= depthDictionaryValues[Q]+1

        if currentDepth >= maxDepth:
            reason = "Exited! maximum depth("+str(currentDepth)+") reached; no solution was found for the string"
            maxDepthReached = True;
            break

        #Get the leftmost variable in Q
        for i in range(len(Q)):
            if Q[i].isupper():
                Q= Q.partition(Q[i])
                break
        #2.4
        while not done and not foundSearchedString:
            for i in productions[Q[1]]:
                paths= []
                paths.append(Q[0])
                paths.append(i)
                paths.append(Q[2])

                uwv = "".join(paths)

                #print(paths)

                terminalCount = 0
                for i in range(len(uwv)):
                    if uwv[i] in terminal:
                        terminalCount+= 1

                foundMatch = True
                for j in range(len(Q[0].strip())):
                    ##print(str(j)+str(Q[0]))
                    ##print(str(str(len(Q[0][j])) + str(len(string))))
                    #print("String: "+str(string))
                    #print("Q : " + str(Q[0]).strip())

                    if Q[0] == string:
                        foundMatch= True
                        break
                    if len(Q[0]) > len(string):
                        foundMatch= False
                        reason= "the length on the search: "+Q[0]+" exceeded the evaluated string: "+string+" ´s length"
                        break
                    elif Q[0][j] != string[j]:
                        reason = "it is not possible to have "+string[j]+" next."
                        foundMatch= False
                        break

                if terminalCount < len(uwv) and foundMatch:
                    queue.append(uwv)
                    appendToDictionary(Tree, "".join(Q), uwv)
                    depthDictionaryValues[uwv]= depthDictionaryValues["".join(Q)]+1
                    if string == uwv:
                        foundSearchedString= True
                elif foundMatch:
                    appendToDictionary(Tree, "".join(Q), uwv)
                    if string == uwv:
                        foundSearchedString= True

            done= True

    # Set Tree structure and then print it
    treeRoot = Node(initialState)
    appendTreeNodes(Tree, initialState, treeRoot)
    # Print Tree
    print_tree(treeRoot, horizontal=False)

    #Report possible outcomes (after the tree is done)
    print("OUTCOME: ")
    if foundSearchedString == True:
        print("-> The string "+string+" is accepted at depth "+str(currentDepth))
    elif maxDepthReached:
        print(reason)
    else:
        print("-> The string is NOT accepted by the grammar because "+reason)

"""
    appendTreeNodes( Dictionary    the tree Dictionary that stores all the nodes & childern, 
                        String      The string to dsiplay as the node on console, 
                        Node        the parent node, 
                        ):

    This function will fill the tree based on the tree dictionary on TopDownParsing()
"""
def appendTreeNodes(Tree, key, parent):
    for i in Tree:
        for j in Tree[i]:
            if i == key:
                node= Node(j, parent)
                appendTreeNodes(Tree, j, node)
"""
    appendToDictionary( Dictionary  the depth Dictionary that stores all the values, 
                        String      the key value, 
                        String      the value to represent with the key, 
                        ):

    This function will fill the depthDictionaryValues dictionary in order to effectively print the tree
"""
def appendToDictionary(dict_obj, key, value):
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            dict_obj[key] = [dict_obj[key]]
        dict_obj[key].append(value)
    else:
        dict_obj[key]= [value]
"""
    Gather The necessary input informaction
"""
print("(Step 1/3) | Provide a String to evaluate in language [abba, bbaa, abab, etc]")
stringToEvaluate = input().lower()

print("(Step 2/3) | Indicate the maximun search maxDepth [Int]")
maxDepth = int(input())

print("(Step 3/3) | Select the test file [test1, test2, test3, test4]")
inputSelectedFile = input().lower()

"""
    Dinamically search the .txt file based on the guidelines
"""
with open(inputSelectedFile + ".txt") as file_in:
    lines = []  # This array will store every line of the file in their own index, in order.
    for line in file_in:
        line = line.rstrip()  # Sometimes the end of the line will keep a "\n" so this code removes it because it affects comparisons
        lines.append(line)

    # This variable stores the values on the first line of the .txt file, these are the set of non-terminal symbols separated by commas.
    nonTerminalSymbols = lines[0].split(',')
    print("\n-> Non-Terminal Symbols: ")
    print(nonTerminalSymbols)

    # This variable stores the values on the second line of the .txt file, these are set of terminal symbols separated by commas.
    terminalSymbols = lines[1].split(',')
    print("\n-> Terminal Symbols: ")
    print(terminalSymbols)

    # This variable stores the values on the second line of the .txt file, this is the start symbol.
    initialState = lines[2].strip()
    print("\n-> Initial State: ")
    print(initialState)

    # This variable stores the values on the 4th line onward of the .txt file,
    # these represent the productions of the grammar
    productions = {}
    for i in range(3, len(lines)):
        grammar = lines[i].strip()
        if not grammar:
            break
        grammar = grammar.split("->")
        if grammar[0].isupper():
            appendToDictionary(productions, grammar[0], grammar[1])
        grammar.clear()
    print("\n-> Productions: ")
    print(productions)
    print(" ")

TopDownParsing(nonTerminalSymbols, terminalSymbols, initialState, productions, stringToEvaluate, maxDepth)