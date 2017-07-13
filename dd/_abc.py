"""Interface specification.

This specification is implemented by the modules:

- `dd.autoref`
- `dd.cudd`
- `dd.sylvan` (partially)
- `dd.buddy` (partially)
"""
# Copyright 2017 by California Institute of Technology
# All rights reserved. Licensed under BSD-3.
#


class BDD(object):
    """Shared reduced ordered binary decision diagram."""

    def __init__(self, levels=None):
        pass

    def __eq__(self, other):
        pass

    def __len__(self):
        pass

    def __contains__(self, u):
        pass

    def __str__(self):
        pass

    def configure(self, **kw):
        pass

    def statistics(self):
        pass

    def succ(self, u):
        i, v, w = self._bdd.succ(u)
        v = self._wrap(v)
        w = self._wrap(w)
        return i, v, w

    def declare(self, *variables):
        """Add names in `variables` to `self.vars`.

        ```python
        bdd.declare('x', 'y', 'z')
        ```
        """
        for var in variables:
            self.add_var(var)

    def var(self, var):
        r = self._bdd.var(var)
        return self._wrap(r)

    def var_at_level(self, level):
        """Return variable with `level`."""

    def level_of_var(self, var):
        """Return level of `var`, or `None`."""

    def copy(self, u, other):
        """Copy operator `u` from `self` to `other` manager."""

    def support(self, u, as_levels=False):
        """Return `set` of variables that node `u` depends on."""

    def let(self, definitions, u):
        """Substitute `definitions` for variables in `u`.

        @param definitions: `dict` that maps some variable
            names to Boolean values, or other variable names,
            or BDD nodes. All values should be of same type.
        """

    def forall(self, variables, u):
        """Quantify `variables` in `u` universally."""

    def exist(self, variables, u):
        """Quantify `variables` in `u` existentially."""

    def count(self, u, nvars=None):
        """Return number of models of node `u`.

        @param n: number of variables to assume.

            If omitted, then assume those in `support(u)`.
            The levels of variables outside support
            are ignored in counting, and `n` used to
            increase the result at the end of recursion.
        """

    def pick(self, u, care_vars=None):
        """Return a single assignment as `dict`.

        An assignment is a `dict` that maps
        each variable to a `bool`. Examples:

        ```python
        >>> u = bdd.add_expr('x')
        >>> bdd.pick(u)
        {'x': True}

        >>> u = bdd.add_expr('y')
        >>> bdd.pick(u)
        {'y': True}

        >>> u = bdd.add_expr('y')
        >>> bdd.pick(u, care_vars=['x', 'y'])
        {'x': False, 'y': True}

        >>> u = bdd.add_expr('x \/ y')
        >>> bdd.pick(u)
        {'x': False, 'y': True}

        >>> u = bdd.false
        >>> bdd.pick(u) is None
        True
        ```

        By default, `care_vars = support(u)`.
        Log a warning if `care_vars < support(u)`.

        Thin wrapper around `pick_iter`.
        """
        return next(self.pick_iter(u, care_vars), None)

    def pick_iter(self, u, care_vars=None):
        """Return generator over assignments.

        By default, `care_vars = support(u)`.
        Log a warning if `care_vars < support(u)`.

        @param care_vars: cases:

            1. `None`: return (uniform) assignments that
               include exactly those variables in `support(u)`

            2. `set`: return (possibly partial) assignments
               that include at least all bits in `set`

        @rtype: generator of `dict(str: bool)`
        """
        raise NotImplementedError

    def to_bdd(self, expr):
        raise NotImplementedError('use `add_expr`')

    def to_expr(self, u):
        """Return a Boolean expression for node `u`."""

    def ite(self, g, u, v):
        """Ternary conditional `IF g THEN u ELSE v`."""
        pass

    def apply(self, op, u, v=None, w=None):
        r"""Apply operator `op` to nodes `u` and `v`.

        @type op: `str` in:
          - `'not', '~', '!'`
          - `'and', '/\', '&', '&&'`
          - `'or', '\/', '|', '||'`
          - `'xor', '#', '^'`
          - `'=>', '->', 'implies'`
          - `'<=>', '<->', 'equiv'`
          - `'diff', '-'`
          - `'\A', 'forall'`
          - `'\E', 'exists'`
          - `'ite'`
        @type u, v, w: nodes
        """

    def _add_int(self, i):
        pass

    def cube(self, dvars):
        pass

    # TODO: homogeneize API
    def dump(self, filename, roots=None,
             filetype=None, **kw):
        pass

    def load(self, filename, levels=True):
        pass

    @property
    def false(self):
        """Return Boolean constant false."""

    @property
    def true(self):
        """Return Boolean constant true."""


def reorder(bdd, order=None):
    """Apply Rudell's sifting algorithm to `bdd`."""
    _bdd.reorder(bdd._bdd, order=order)


def copy_vars(source, target):
    _bdd.copy_vars(source._bdd, target._bdd)


def copy_bdd(u, target):
    r = _bdd.copy_bdd(u.node, u.bdd, target._bdd)
    return target._wrap(r)


class Operator(object):
    """Convenience wrapper for edges returned by `BDD`."""

    def __init__(self, node, bdd):
        assert node in bdd._bdd, node
        self.bdd = bdd
        self.manager = bdd._bdd
        self.node = node
        self.manager.incref(node)

    def __hash__(self):
        return self.node

    def to_expr(self):
        pass

    def __int__(self):
        pass

    def __str__(self):
        pass

    def __len__(self):
        """Number of nodes reachable from this node."""

    def __del__(self):
        """Dereference node in manager."""

    def __eq__(self, other):
        """`|= self \equiv other`."""

    def __ne__(self, other):
        """`~ |= self \equiv other`."""

    def __lt__(self, other):
        """`(|= self => other) /\ ~ |= self \equiv other`."""

    def __le__(self, other):
        """`|= self => other`."""

    def __invert__(self):
        """Negation `~ self`."""

    def __and__(self, other):
        """Conjunction `self /\ other`."""

    def __or__(self, other):
        """Disjunction `self \/ other`."""

    # def __xor__(self, other):
    #     pass

    # unsure about this
    def implies(self, other):
        pass

    # unsure about this
    def equiv(self, other):
        pass

    @property
    def level(self):
        """Level where this node currently is."""

    @property
    def var(self):
        """Variable at level where this node is."""

    @property
    def low(self):
        """Return "else" node."""

    @property
    def high(self):
        """Return "then" node."""

    @property
    def ref(self):
        """Sum of reference counts of node and its negation."""

    @property
    def negated(self):
        """Return `True` if a complemented edge."""

    @property
    def support(self):
        """Return `set` of variables in support."""

    def let(self, **definitions):
        return self.bdd.let(definitions, self)

    def exist(self, *variables):
        return self.bdd.exist(variables, self)

    def forall(self, *variables):
        return self.bdd.forall(variables, self)

    def pick(self, care_vars=None):
        return self.bdd.pick(self, care_vars)

    def count(self, nvars=None):
        return self.bdd.count(self, nvars)
