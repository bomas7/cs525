############################################################
#
# Assign01 for CS525, Spring, 2026
# It is due the 27th of January, 2026
# Note that the due time is always 11:59pm of
# the due date unless is specified otherwise.
#
############################################################
# datatype term =
# | TMvar of strn
# | TMlam of (strn, term)
# | TMapp of (term, term)
############################################################
#
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
#
############################################################
#
def I_():
    x = TMvar("x")
    return TMlam("x", x)
def K_():
    x = TMvar("x")
    return TMlam("x", TMlam("y", x))
def S_():
    x = TMvar("x")
    y = TMvar("y")
    z = TMvar("z")
    return TMlam("x", TMlam("y", TMlam("z", TMapp(TMapp(x, z), TMapp(y, z)))))
#
# _ = print("I =", I_())
# _ = print("K =", K_())
# _ = print("S =", S_())
#
############################################################
#
# HX: [sub] should be closed!
#
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
#
############################################################

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

# (term, from, to)
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

# print(term_gsubst(TMvar("x"), "x", TMvar("y")))
# lam y = x, x = y+y
my_term = TMlam("y", TMvar("x"))
sub = TMlam("x", TMvar("y"))
print(term_gsubst(my_term, "x", sub))

############################################################
# end of [HWXI/CS525-2026-Fall/assigns/02/lambda0.py]
############################################################
############################################################

