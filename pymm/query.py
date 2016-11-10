class Where(object):
    """
    Where object is a helper to construct WHERE SQL clause with specific Python
    arguments.

    Where is chainable and are represented as a tree structure to know the
    precedence for the boolean logic
    """
    # possible link operator on the children tree node between the
    # different WHERE SQL clause, right now only AND and OR are supported
    operator = None
    _query_string = None
    _arguments = None

    def __init__(self, where_or_qs, arguments=None, operator=None):
        """ Initialize the where object which represent a condition in the WHERE SQL clause """
        if isinstance(where_or_qs, Where):
            # we have a where parent clause as argument,
            # just create it as a child
            self._children = [where_or_qs, ]
        else:
            # we need to create a full Where object
            self._query_string = where_or_qs
            self._arguments = arguments

            self._children = []

        # possible operator (OR / AND) on the child
        self.operator = operator

    @property
    def arguments(self):
        """ Build the arguments for the query_string """
        args = tuple()
        if self._arguments is not None:
            args += (self._arguments, )
        for child in self._children:
            args += child.arguments
        return args

    def OR(self, where):
        """ chain the WHERE SQL clause with a OR boolean operator """
        where.operator = 'OR'
        self._children.append(where)
        return self

    def AND(self, where):
        """ chain the WHERE SQL clause with a AND boolean operator """
        where.operator = 'AND'
        self._children.append(where)
        return self

    @property
    def query_string(self):
        # compute all the tree in order to retrieve the
        # query_string to pass in the WHERE SQL clause
        if self._children == []:
            # we don't have any children to chain the query, we
            # simply return the query string
            return self._query_string
        else:
            # we have children so we need to browse them recursively
            children_qs = ''
            for child in self._children:
                if child.operator:
                    children_qs += ' {} {}'.format(child.operator, child.query_string)
                else:
                    children_qs += ' {}'.format(child.query_string)

            if self._query_string:
                return '( {}{} )'.format(
                    self._query_string,
                    children_qs
                )
            else:
                return '({} )'.format(
                    children_qs
                )
