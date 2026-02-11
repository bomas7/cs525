############################################################
############################################################
#
# Assign03 for CS525, Spring, 2026
# It is due the 10th of February, 2026
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
# previous code
class term:
    ctag = ""
# end-of-class(term)
#
class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def __str__(self):
        return ("TMvar(" + self.arg1 + ")")
# end-of-class(term_var(term))
#
class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMlam"
    def __str__(self):
        return ("TMlam(" + self.arg1 + "," + str(self.arg2) + ")")
# end-of-class(term_lam(term))
#
class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def __str__(self):
        return ("TMapp(" + str(self.arg1) + "," + str(self.arg2) + ")")
# end-of-class(term_app(term))
#
############################################################
#
def TMvar(x00):
    return term_var(x00)
def TMlam(x00, tm1):
    return term_lam(x00, tm1)
def TMapp(tm1, tm2):
    return term_app(tm1, tm2)

# from hw1
def term_freevars(tm0):
    """
    Points: 10
    This function takes a term [tm0] and returns the set of
    free variables in [tm0]. The set returned should be the
    built-in set in Python
    """
    s = set()
    if (tm0.ctag == "TMvar"):
        s.update(tm0.arg1)
    elif (tm0.ctag == "TMlam"):
        s.update(term_freevars(tm0.arg2))
        if (tm0.arg1 in s):
            s.remove(tm0.arg1)
    else:
        s.update(term_freevars(tm0.arg1))
        s.update(term_freevars(tm0.arg2))
    return s

# from hw2
# (term, from, to)

def term_subst0(tm0, x00, sub):
    def subst0(tm0):
        if (tm0.ctag == "TMvar"):
            x01 = tm0.arg1
            return sub if (x00 == x01) else tm0
        if (tm0.ctag == "TMlam"):
            x01 = tm0.arg1
            if (x00 == x01):
                return tm0
            else:
                return TMlam(x01, subst0(tm0.arg2))
        if (tm0.ctag == "TMapp"):
            return TMapp(subst0(tm0.arg1), subst0(tm0.arg2))
        raise TypeError(tm0) # HX: should be deadcode!
    return subst0(tm0)

def term_gsubst(tm0, x00, sub):
    """
    Points: 20
    This function implements the (general) substitution
    function on terms that should correctly handle an open
    [sub] (that is, [sub] containing free variables)
    You can use the function [term_freevars] implemented
    in Assign01.
    """
    # sample code
    def subst0(tm0):
        if (tm0.ctag == "TMvar"):
            x01 = tm0.arg1
            return sub if (x00 == x01) else tm0
        if (tm0.ctag == "TMlam"):
            vars = term_freevars(sub)
            param = tm0.arg1
            # make new name if in freevars
            while (param in vars):
                param += "0"
            # replace
            fixed_arg2 = term_subst0(tm0.arg2, tm0.arg1, TMvar(param))
            fixed_term = TMlam(param, fixed_arg2)
            return term_subst0(fixed_term, x00, sub)

        if (tm0.ctag == "TMapp"):
            return TMapp(subst0(tm0.arg1), subst0(tm0.arg2))
        raise TypeError(tm0) # HX: should be deadcode!
    return subst0(tm0)
############################################################

def lambda_normalize(tm0):
    """
    HX: 10 points
    datatype term =
      | TMvar of strn
      | TMlam of (strn, term)
      | TMapp of (term, term)
    Given a term [tm0], [lambda_normalize] applies the
    leftmost evaluation strategy to normalize it.
    Note that normalization needs to be performed under
    'lambda' as well.
    """
    # TMapp(TMlam(param, body), arg)
    if tm0.ctag == "TMapp":
        if tm0.arg1.ctag != "TMlam":
            arg1_n = lambda_normalize(tm0.arg1)
            return lambda_normalize(TMapp(arg1_n, tm0.arg2))
        # body, param, arg
        tm0_n = term_gsubst(tm0.arg1.arg2, tm0.arg1.arg1, tm0.arg2)
        return lambda_normalize(tm0_n)
    elif tm0.ctag == "TMlam":
        return TMlam(tm0.arg1, lambda_normalize(tm0.arg2))
    else:
        return tm0

############################################################

def church(n):
    # church = f(x)
    c = TMvar("x")
    for i in range(n):
        c = TMapp(TMvar("f"), c) 
    return TMlam("f", TMlam("x", c))

n = TMvar("n")
f = TMvar("f")
x = TMvar("x")

def suc():
    # n, f, x -> f(n f(x))
    # lamda n -> n+1
    c = TMapp(f, TMapp(TMapp(n, f), x))
    return TMlam("n", TMlam("f", TMlam("x", c)))

t = TMapp(TMapp(TMapp(suc(), church(0)), f), x)

print(t)
print(lambda_normalize(t))
print("HERE")

# for i in range(5):
#     print(church(i))

x = TMvar("x")
y = TMvar("y")

def tup(t1, t2): 
    return TMlam("p", TMapp(TMapp(TMvar("p"), t1), t2))
def fst(t):
    return TMapp(t, TMlam("x", TMlam("y", x)))
def sec(t):
    return TMapp(t, TMlam("x", TMlam("y", y)))

def ipred_in_lambda():
    """
    HX: 10 points
    This one is what we often call "eat-your-own-dog-food"
    Please implement the predesessor function on integers
    A 'term' is returned by ipred_in_lambda() representing
    the predesessor function (that works on Church numerals).
    """
    n = TMvar("n")
    p = TMvar("p")
    f = TMlam("f", TMvar("x"))
    # <0, 0> -> <0, 1> -> <1, 2>
    # sec(p), f(sec(p))
    nxt = TMlam("p", tup(sec(p), TMapp(f, sec(p))))
    # n, f, <0, 0>
    ct = TMapp(TMapp(n, nxt), tup(church(0), church(0)))
    pre = fst(ct)
    # n -> n-1
    return TMlam("n", pre)

x = TMvar("x")
f = TMvar("f")
pred = ipred_in_lambda()
# print(TMapp(pred, TMapp(church(0), TMapp(f, x))))
print(TMapp(pred, church(0)))
print("--------\n")

############################################################

def isqrt_in_lambda():
    """
    HX: 20 points
    This one is what we often call "eat-your-own-dog-food"
    Please implement an integer version of the square root
    funtion. For instance,
    isqrt(0) = 0, isqrt(2) = 1, isqrt(10) = 3, ...
    In general, given n >= 0, isqrt(n) returns the largest
    integer x satisfying x * x <= n. Your implementation
    is expected to be effcient; your code may be tested on
    something input as large as 1000000.
    A 'term' is returned by isqrt_in_lambda() representing
    the isqrt function (that works on Church numerals).
    """
    raise NotImplementedError

############################################################
# end of [HWXI/CS525-2026-Spring/assigns/03/assign03.py]
############################################################

# TMvar("y")
print(lambda_normalize(TMapp(TMlam("x", TMvar("x")), TMvar("y"))))
# TMlam("y", TMvar("z"))
print(lambda_normalize(TMapp(TMlam("x", TMlam("y", TMvar("x"))), TMvar("z"))))
# TMvar("x")
print(lambda_normalize(TMvar("x")))
