# LL(1) parser code in python import re
import lexer

# calculation of first
# epsilon is denoted by '#' (semi-colon)

# pass rule in first function 
def first(rule):
    global rules, nonterm_userdef, term_userdef, diction, firsts
    # recursion base condition 
    # # (for terminal or epsilon)
    if len(rule) != 0 and (rule is not None):
         if rule[0] in term_userdef:
            return rule[0] 
         elif rule[0] == '#':
            return '#'
    # condition for Non-Terminals 
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            # fres temporary list of result 
            fres = []
            rhs_rules = diction[rule[0]]
            # call first on each rule of RHS # fetched (& take union)
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                        for i in indivRes:
                            fres.append(i)
                else:
                        fres.append(indivRes)

            # if no epsilon in result # - received return fres 
            if '#' not in fres:
                return fres
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = [] 
                fres.remove('#') 
                if len(rule) > 1:
                    ansNew = first(rule[1:]) 
                if ansNew != None:
                    if type(ansNew) is list:
                        newList = fres + ansNew
                    else:
                        newList = fres + [ansNew]
                else:
                    newList = fres + [ansNew]
                return newList
            # if result is not already returned 
            # # - control reaches here
            # lastly if eplison still persists 
            # # - keep it in result of first 
            fres.append('#')
            return fres


# calculation of follow
# use 'rules' list, and 'diction' dict from above

# follow function input is the split result on
# - Non-Terminal whose Follow we want to compute 

def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    # for start symbol return $ (recursion base case)
    solset = set()
    if nt == start_symbol:
        # return '$' 
        solset.add('$')
    # check all occurrences
    # solset - is result of computed 'follow' so far
    # For input, check in all rules 
    for curNT in diction:
        rhs = diction[curNT]
        # go for all productions of NT 
        for subrule in rhs:
            if nt in subrule:
                # call for all occurrences on # - non-terminal in subrule 
                while nt in subrule:
                    index_nt = subrule.index(nt) 
                    subrule = subrule[index_nt + 1:]
                    # empty condition - call follow on LHS 
                    if len(subrule) != 0:
                        # compute first if symbols on
                        # - RHS of target Non-Terminal exists 
                        res = first(subrule)
                        # if epsilon in result apply rule # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A) 
                        if '#' in res:
                            newList = [] 
                            res.remove('#')
                            ansNew = follow(curNT) 
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # when nothing in RHS, go circular 
                        # - and take follow of LHS
                        # only if (NT in LHS)!=curNT 
                        if nt != curNT:
                            res = follow(curNT)
                    # add follow result in set form 
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)
  


   
 
def computeAllFirsts():
    global rules, nonterm_userdef, term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        # remove un-necessary spaces 
        k[0] = k[0].strip()
        k[1] = k[1].strip() 
        rhs = k[1]
        multirhs = rhs.split('|')
        # remove un-necessary spaces 
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs

    print(f"\nRules: \n") 
    for y in diction:
        print(f"{y}->{diction[y]}")
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y): 
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        firsts[y]=t           
    print("\nCalculated firsts: ") 
    key_list = list(firsts.keys()) 
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
            f"=> {firsts.get(gg)}")
        index += 1


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef,term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT) 
        if sol is not None:
            for g in sol:
                solset.add(g) 
        follows[NT] = solset

    print("\nCalculated follows: ") 
    key_list = list(follows.keys())
    index = 0
    for gg in follows: 
        print(f"follow({key_list[index]})"f" => {follows[gg]}") 
        index += 1


# create parse table
def createParseTable(): 
    import copy
    global diction, firsts, follows, term_userdef 
    print("\nFirsts and Follow Result table\n")

    # find space size 
    mx_len_first = 0
    mx_len_fol = 0 
    for u in diction:
        k1 = len(str(firsts[u])) 
        k2 = len(str(follows[u])) 
        if k1 > mx_len_first:
            mx_len_first = k1 
        if k2 > mx_len_fol:
            mx_len_fol = k2
    print(f"{{:<{10}}} "
        f"{{:<{mx_len_first + 5}}} "
        f"{{:<{mx_len_fol + 5}}}"
    
    .format("Non-T", "FIRST", "FOLLOW"))
    for u in diction:
        print(f"{{:<{10}}} "
            f"{{:<{mx_len_first + 5}}} "
            f"{{:<{mx_len_fol + 5}}}"
            .format(u, str(firsts[u]), str(follows[u])))

    # create matrix of row(NT) x [col(T) + 1($)] 
    # create list of non-terminals
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef) 
    terminals.append('$')

    # create the initial empty state of ,matrix 
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col 
        mat.append(row)

    # Classifying grammar as LL(1) or not LL(1) 
    grammar_is_LL = True
    # rules implementation 
    for lhs in diction:
        rhs = diction[lhs] 
        for y in rhs:
            res = first(y)
            # epsilon is present,
            # - take union with follow 
            if '#' in res:
                if type(res) == str:
                    firstFollow = [] 
                    fol_op = follows[lhs] 
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('#') 
                    res = list(res) +\
                        list(follows[lhs])
            # add rules to table 
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp) 
            for c in res:
                xnt = ntlist.index(lhs) 
                yt = terminals.index(c) 
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] + f"{lhs}->{' '.join(y)}"
                else:
                    # if rule already present
                    if f"{lhs}->{y}" in mat[xnt][yt]: 
                        continue
                    else: 
                        grammar_is_LL = False 
                        mat[xnt][yt] = mat[xnt][yt] \
                        + f",{lhs}->{' '.join(y)}"
    # final state of parse table 
    print("\nGenerated parsing table:\n") 
    frmt = "{:>12}" * len(terminals) 
    print(frmt.format(*terminals))
    j = 0
    for y in mat:
        frmt1 = "{:>12}" * len(y) 
        print(f"{ntlist[j]} {frmt1.format(*y)}") 
        j += 1
    return (mat, grammar_is_LL, terminals)

def validateStringUsingStackBuffer(parsing_table, grammarll1,table_term_list, input_string, term_userdef,start_symbol):

    print("Parsing")
    
    # for more than one entries
    # - in one cell of parsing table 
    if grammarll1 == False:
        return f"\nInput String = \"{input_string}\"\nGrammar is not LL(1)"

    # implementing stack buffer

    stack = [start_symbol, '$'] 
    buffer = []

    # reverse input string store in buffer 
    input_string = input_string.split() 
    input_string.reverse()
    buffer = ['$'] + input_string

    print("{:>20}\t\t {:>20}\t {:>20}".
    format("	Buffer	", "	Stack	","	Action	"))

    while True:
        # end loop if all symbols matched 
        if stack == ['$'] and buffer == ['$']:
            print("{:>20}\t\t {:>20}\t {:>20}"
                .format(' '.join(buffer),
                    ' '.join(stack), "Valid"))
            return "\nValid String!" 
        elif stack[0] not in term_userdef:
            # take font of buffer (y) and tos (x)
            x = list(diction.keys()).index(stack[0]) 
            y = table_term_list.index(buffer[-1]) 
            if parsing_table[x][y] != '':
                # format table entry received 
                entry = parsing_table[x][y] 
                print("{:>20}\t\t {:>20}\t {:>25}".format(' '.join(buffer),' '.join(stack),f"T[{stack[0]}][{buffer[-1]}] = {entry}")) 
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip() 
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                print("{:>20} {:>20} {:>25}".format(' '.join(buffer),' '.join(stack),f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                return f"\nInvalid String! No rule at " f"Table[{stack[0]}][{buffer[-1]}]."
        else:
            # stack top is Terminal 
            if stack[0] == buffer[-1]:
                print("{:>20}\t\t {:>20}\t {:>20}".format(' '.join(buffer),' '.join(stack), f"Matched:{stack[0]}"))
                buffer = buffer[:-1] 
                stack = stack[1:]
            else:
                print(f"\n\nExpected Character : {stack[0]}\n Actual Character : {buffer[-1]}")
                return "\nInvalid String! Unmatched terminal symbols"


rules = ["S -> T M B A D",
        "T -> int",
        "M -> main()", "B -> begin",
        "D -> end",
        "A -> E F",
        "E -> T n , i , sum = 0 ;",
        "F -> for ( X ; Y ; Z ) B H D", "X -> i = 1",
        "Y -> i <= n",
        "Z -> ++ i",
        "H -> expr = expr + expr ;"]

nonterm_userdef = ['S', 'T', 'M', 'B', 'A', 'D', 'E', 'F', 'X', 'Y', 'Z', 'H']
term_userdef = ["int", "main()", "begin", "end","n", "i", "sum", "=", "0", "for","(",")", "1", "<=", "++", "expr","+", ";", ","]


inp = ''
with open('input.txt','r+') as f: 
    for line in f.readlines():
        inp += line
        valid, ip = lexer.run(inp) 
if valid:
    # diction - store rules inputed
    # firsts - store computed firsts 
    diction = {}
    firsts = {} 
    follows = {}
    computeAllFirsts()
    # assuming first rule has start_symbol start symbol can be modified in below line of 
    start_symbol = list(diction.keys())[0]
    # computes all FOLLOWs for all occurrences 
    computeAllFollows()
    # computes all FIRSTs for all non terminals 
    
    # generate formatted first and follow table then generate parse table 
    (parsing_table, result, tabTerm) = createParseTable()
    # validate string input using stack-buffer concept 
    if ip is not None:
       validity = validateStringUsingStackBuffer (parsing_table, result,tabTerm, ip, term_userdef,start_symbol) 
       print(validity)
    else:
       print("\nNo input String detected")
else:
    print(ip) 
    print("Invalid Input")