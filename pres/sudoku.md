# Sudoku in Python

* * * * *

# Presentation Plan
## Generator Expressions
## Sudoku Notation
## Constraint Propagation
## Search

* * * * *

# Generators

In scientific programming, we often encounter situations where we have a recipe for producing data that we do not want
to use immediately.  We want the interpreter to evaluate our producer function *lazily*, only giving us data when we really need it.
Suppose, as a somewhat trivial example, that we were interested in the sum of the first 10 Fibonacci numbers.  We could
write a for loop to do this:

    !python
    # Generate the sum of the first 10 Fibonacci numbers
    n1, n2 = 0, 1
    sum = 0
    for i in xrange(10):
      sum += n2
      n1, n2 = n2, n1+n2

But suppose our Fibonacci sequences are used everywhere (we write really interesting code on the
weekends), so we choose to refactor the Fibonacci code into a *generator* function.
      
* * * * *

# Fibonacci Generator Function

Python allows us to define a generator function, *fib*, that will return a *generator-iterator* for lazily evaluating the Fibonacci
sequences.  Each time *next* is called on the *generator-iterator*, it executes the code defined in the function body of
*fib* until it reaches a *yield* statement or the end of the function body, at which point execution is returned to the
caller. 

    !python
    def fib():
      "Generates Fibonacci numbers, starting from the first"
      n1, n2 = 0, 1
      while 1:
        yield n2
        n1, n2 = n2, n1+n2

    f = fib()
    sum = 0
    for i in xrange(10):
      sum += next(f)

* * * * *

# List Comprehensions

There are a few programming idioms that have become very common over the last half-century that it
is handy to have a concise notation for using them.  Perhaps one of the most common is an iteration that
generates a list of values.  Suppose we wished to generate a list of the first 10 Fibonacci numbers.  The following is
valid Python code that newcomers from other languages might write.

## Common Code 
    !python
    f = fib()
    l = []
    for i in xrange(10):
      l.append(next(f))

 Experience Python developers prefer to use *list comprehensions*, a terser syntax inspired by mathematical set notation.

## List Comprehension
    !python
    f = fib()
    l = [next(f) for i in xrange(10)]
    
List comprehensions can include multiple for loops and if statements, we'll see a more complicated example in next section.

* * * * *

# Generator Expressions

You might think that it would be very useful to combine the power of list comprehensions with lazy evaluation, and you'd
be right!  Fortunately, the designers of Python have included *generator expressions* as a language feature, which look
syntactically nearly identical to list comprehensions, with [ ] replaced ( ).

Suppose we wanted a function to compute the Cartesian product of two sets A and B (ignoring the fact that this is implemented as
itertools.product).  The function could eagerly return all values in a list with a list comprehension.

## Cartesian Product from a List Comprehension
    !python
    def cart_prod(A,B):
      return [(x,y) for x in A for y in B]
    A = 'abc'
    B = xrange(3)
    print(cart_prod(A,B))

But if the output of the Cartesian Product will be consumed one value at a time, we could probably save space by using a
generator expression instead:

## Cartesian Product from a Generator Expression
    !python
    def cart_prod(A,B):
      return ((x,y) for x in A for y in B)
    for f in cart_prod(A,B):
      print f

* * * * *

# Sudoku Notation

The rest of this lecture will present and extend an [excellent article](http://norvig.com/sudoku.html)
(and accompanying code) by Peter Norvig, Director of Research at Google, Inc.  

A Sudoku puzzle is composed of a 9x9 *grid* of 81 *squares*, with the columns numbered 1-9, and the
rows labeled A-I.  The 9x9 grid can be further subdivided into *units*, which can either be one of
the columns, rows, or one of the 9 non-overlapping 3x3 boxes.  A square's *peers* are the other squares
that also belong to the three units it is a member of.  A puzzle starts with some number of
the 81 squares prefilled with digits ranging between 1-9.  It is considered solved when each unit
(that is, every row, column, and box) contains a permutation of the digits 1-9.

(The below ASCII graphic from Norvig's site shows the names of the squares, a sample puzzle, and its
solution):

    A1 A2 A3| A4 A5 A6| A7 A8 A9    4 . . |. . . |8 . 5     4 1 7 |3 6 9 |8 2 5 
    B1 B2 B3| B4 B5 B6| B7 B8 B9    . 3 . |. . . |. . .     6 3 2 |1 5 8 |9 4 7
    C1 C2 C3| C4 C5 C6| C7 C8 C9    . . . |7 . . |. . .     9 5 8 |7 2 4 |3 1 6 
    --------+---------+---------    ------+------+------    ------+------+------
    D1 D2 D3| D4 D5 D6| D7 D8 D9    . 2 . |. . . |. 6 .     8 2 5 |4 3 7 |1 6 9 
    E1 E2 E3| E4 E5 E6| E7 E8 E9    . . . |. 8 . |4 . .     7 9 1 |5 8 6 |4 3 2 
    F1 F2 F3| F4 F5 F6| F7 F8 F9    . . . |. 1 . |. . .     3 4 6 |9 1 2 |7 5 8 
    --------+---------+---------    ------+------+------    ------+------+------
    G1 G2 G3| G4 G5 G6| G7 G8 G9    . . . |6 . 3 |. 7 .     2 8 9 |6 4 3 |5 7 1 
    H1 H2 H3| H4 H5 H6| H7 H8 H9    5 . . |2 . . |. . .     5 7 3 |2 9 1 |6 8 4 
    I1 I2 I3| I4 I5 I6| I7 I8 I9    1 . 4 |. . . |. . .     1 6 4 |8 7 5 |2 9 3 

* * * * *

# Code Basics
    !python
    ## Throughout this program we have:
    ##   r is a row,    e.g. 'A'
    ##   c is a column, e.g. '3'
    ##   s is a square, e.g. 'A3' 
    ##   d is a digit,  e.g. '9'
    ##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1'] 
    ##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
    ##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

Norvig's strategy is already apparent in the first several lines of code.  He will maintain a
dictionary, `values`, that contains a character string of uneliminated candidate digits for each
square on the grid.  He will then use a strategy to eliminate candidate digits from the dictionary
until there is only one uneliminated digit for each square in the dictionary.  

It turns out that Norvig uses two techniques for elimination:

* Constraint Propagation
* Depth-First Search

Before we get into the strategy implementation, we need some preliminary functions and data. 

* * * * *

# Cartesian Product Function

Now he defines a simple function to take Cartesian products (used in setup).
    !python
    def cross(A, B):
      "Cross product of elements in A and elements in B."
      return [a+b for a in A for b in B]

Notice the list comprehension!  Also, this code is slightly out of date, since the modern
`itertools` module, built-in to Python, contains a `product` function that performs a very similar
operation so that cross could have been implemented slightly more efficiently like this:

    !python
    def cross(A, B):
      "Cross product of elements in A and elements in B."
      map(''.join,itertools.product(a,b))

Here, the funny `''.join"`  notation and use of `map` are to keep a consistent format with Norvig's
string data objects (Norvig uses 'A1' instead of ('A','1'), the natural tuple that would arise from
a Cartesian product of two character sets.  Get used to `.join`, a very useful method that belongs
to all string objects. For any string object `s`, `s.join` concatenates two or more strings using
`s` as the separator between elements.  For example, we could have used `'.'.join` if we wanted 'A.1'.

* * * * *
# Code Setup - Basic Data

A Python file containing source code is often referred to as a *module*.  To make use of a Python
module (on the path), it is customary to load the module using an `import` statement:

    !python
    import sudoku
    
When the interpreter encounters the import statement, it executes all the code in the module in its
own namespace, which usually includes the definition of several functions, and in this case, the
declaration and definition of some module data.

    !python
    digits   = '123456789'
    rows     = 'ABCDEFGHI'
    cols     = digits

Remember that character strings in Python are *immutable*, so the third statement makes a copy of
the digits (This usage of character strings ends up simplifying Norvig's code quite a bit, and was a
deliberate choice on his part).

All of the following data is available from the interpreter by accessing the sudoku namespace.  Here
are three ways of printing sudoku.digits, using slightly different import semantics:

    !python
    import sudoku; print sudoku.digits
    import sudoku as sd; print sd.digits
    from sudoku import digits; print digits

* * * * *
# Code Setup - Advanced Data I

Recall that there are 81 *squares*, which are easily generated by taking a Cartesian product of the
row and column indices:
    
    !python
    squares  = cross(rows, cols)

The unit list comprises the 9 column units, 9 row units, and 9 box units, also generated by
Cartesian products.  Note that the below code generates a list of 3 lists, with each sublist
containing 9 string entries.

    !python
    unitlist = ([cross(rows, c) for c in cols] +
          [cross(r, cols) for r in rows] +
          [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

* * * * *
# Code Setup - Advanced Data II

Norvig now sets up two dictionaries that will assist in eliminating candidate digits.  The first
dictionary, `units`, associates each square with the three units that it belongs to, allowing him to
ask (and answer) the question "To which list of units does square s belong?" by using s as a key to the
dictionary.  Notice the use of an outer (non-nested) generator
expression for each square `s`  as well as the `if` and `in` statements in the list comprehension to
qualify the three members of unitlist that `s` belongs to.

    !python
    units = dict((s, [u for u in unitlist if s in u])
                  for s in squares)
 
 The second dictionary, `peers`, determines the unique set of squares that constitute each square's
 peers by taking the set difference of the union of the three units and the square itself (which is
 a member of all three units but is not its own peer). 

    !python
    peers = dict((s, set(sum(units[s],[]))-set([s]))
                 for s in squares)

Norvig's technique for flattening the list of three lists into a single list: `sum(units[s],[])`, is
deprecated in newer versions of Python, and the following code should be used instead:
    
    !python
    peers = dict((s, set(itertools.chain.from_iterable(units[s]) - set([s])))
                 for s in squares)

* * * * *
 
# Parsing and Initializing Grids

These functions assume that an `assign` function has been defined, which we will cover next.
Something surprising to non-Python programmers might be the `for s,d in ...` line in `parse_grid`.
This is an example of tuple unpacking, and is used throughout Python when multiple values are needed
on the left-hand side of an assignment.  The `zip` function can be thought of as a "tuple pack", it
takes two sequences as arguments and returns a list of tuples, with each tuple containing the i-th
element of each sequence.

    !python
    def parse_grid(grid):
        """Convert grid to a dict of possible values, {square: digits}, or
        return False if a contradiction is detected."""
        ## To start, every square can be any digit; then assign values from the grid.
        values = dict((s, digits) for s in squares)
        for s,d in grid_values(grid).items():
            if d in digits and not assign(values, s, d):
                return False ## (Fail if we can't assign d to square s.)
        return values

    def grid_values(grid):
        "Convert grid into a dict of {square: char} with '0' or '.' for empties."
        chars = [c for c in grid if c in digits or c in '0.']
        assert len(chars) == 81
        return dict(zip(squares, chars))
    
* * * * *
 
# Constraint Propagation

Constraint propagation is the "secret sauce" of Norvig's Sudoku solver.  The key idea he employs is
that assignments trigger eliminations, which can trigger more eliminations or assignments recursively.

    !python
    def assign(values, s, d):
        """Eliminate all the other values (except d) from values[s] and propagate.
        Return values, except return False if a contradiction is detected."""
        other_values = values[s].replace(d, '')
        if all(eliminate(values, s, d2) for d2 in other_values):
            return values
        else:
            return False

* * * * *

# Elimination 

    def eliminate(values, s, d):
        """Eliminate d from values[s]; propagate when values or places <= 2.
        Return values, except return False if a contradiction is detected."""
        if d not in values[s]:
            return values ## Already eliminated
        values[s] = values[s].replace(d,'')
        ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values[s]) == 0:
            return False ## Contradiction: removed last value
        elif len(values[s]) == 1:
            d2 = values[s]
            if not all(eliminate(values, s2, d2) for s2 in peers[s]):
                return False
        ## (2) If a unit u is reduced to only one place for a value d, then put it there.
        for u in units[s]:
            dplaces = [s for s in u if d in values[s]]
            if len(dplaces) == 0:
                return False ## Contradiction: no place for this value
            elif len(dplaces) == 1:
                # d can only be in one place in unit; assign it there
                if not assign(values, dplaces[0], d):
                    return False
    return values

* * * * *

# Search

It turns out that for simple Sudoku puzzles, constraint propagation is sufficient enough to solve
the puzzle completely.  For more difficult cases, Norvig uses a simple *depth-first search* that
hypothesizes a trial assignment, then propagates and searches from the trial position until a
contradiction (prune) or solution (done!) is found.  The search and solve code are very simple to
write:

    !python
    
    def solve(grid): return search(parse_grid(grid))

    def search(values):
        "Using depth-first search and propagation, try all possible values."
        if values is False:
            return False ## Failed earlier
        if all(len(values[s]) == 1 for s in squares):
            return values ## Solved!
        ## Chose the unfilled square s with the fewest possibilities
        n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
        return some(search(assign(values.copy(), s, d))
                    for d in values[s])

The only real tricks to this code are the use of the `.copy` method on the mutable `values`
dictionary for each trial, and Norvig's `some` function, which is defined with the misleading doc
string:

    !python
    "Return some element of seq that is true."

`some` more precisely returns the first element of `seq` that is True, and returns False otherwise.  

