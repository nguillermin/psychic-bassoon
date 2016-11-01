from pyparsing import CaselessKeyword, Literal, ZeroOrMore, OneOrMore, Group, Optional, \
                        Combine, Forward, Word, FollowedBy, Suppress, QuotedString, \
                        alphas, nums, printables, dblSlashComment

# pyparsing API at https://pythonhosted.org/pyparsing/
# Grammar provided by http://dgrok.excastle.com/Grammar.htm

FUNCTION = CaselessKeyword('function')
PROCEDURE = CaselessKeyword('procedure')
LPAREN = Literal('(')
RPAREN = Literal(')')
COLON = Literal(':')
SEMICOLON = Literal(';')
COMMA = Literal(',').suppress()
BEGIN = CaselessKeyword('begin')
END = CaselessKeyword('end')
PERIOD = Literal('.')
IF = CaselessKeyword('if')
THEN = CaselessKeyword('then')
ELSE = CaselessKeyword('else')
ASSIGN = Combine(Literal(':') + FollowedBy('=') + Literal('='))
VAR = CaselessKeyword('var')
CONST = CaselessKeyword('const')
BEGIN = CaselessKeyword('begin')
END = CaselessKeyword('end')
WITH = CaselessKeyword('with')
DO = CaselessKeyword('do')
EQUALS = Literal('=')
CONCAT = Literal('+')
LTHAN = Literal('<')
GTHAN = Literal('>')
LTHANEQ = Literal('<=')
GTHANEQ = Literal('>=')
NEQUAL = Literal('<>')
PLUS = Literal('+')
MINUS = Literal('-')
MULTIPLY = Literal('*')
DIVIDE = Literal('/')
NOT = CaselessKeyword('not')
AT = Literal('@')
INHERITED = CaselessKeyword('inherited')
LBRACKET = Literal('[')
RBRACKET = Literal(']')
OR = CaselessKeyword('or')
XOR = CaselessKeyword('xor')
TRY = CaselessKeyword('try')
FINALLY = CaselessKeyword('finally')
EXCEPT = CaselessKeyword('except')
ON = CaselessKeyword('on')
NIL = CaselessKeyword('nil')

ident = Word(alphas)
identList = ident + ZeroOrMore(COMMA + ident)
qualifiedIdent = ident + ZeroOrMore(PERIOD + ident)
_type = ident
retval = ident
RelOp = EQUALS | LTHAN | GTHAN | LTHANEQ | GTHANEQ | NEQUAL
AddOp = PLUS | MINUS | OR | XOR
MulOp = MULTIPLY | DIVIDE #| DIV | MOD | AND | SHL | SHR
UnaryOp = NOT | PLUS | MINUS | AT | INHERITED

expression = Forward()
expressionList = Forward()
parameterExpression = Forward()

setLiteral = Forward()

Particle = (ident | Word(nums) | NIL | QuotedString("'",unquoteResults=False,escQuote="''") |
            (LPAREN + expression + RPAREN) | setLiteral)
Atom = Particle + ZeroOrMore( (PERIOD + ident) |
                    (LBRACKET + expressionList + RBRACKET) |
                    (LPAREN + ZeroOrMore(parameterExpression + ZeroOrMore(COMMA + parameterExpression)) + RPAREN)
                )

Factor = Forward()
Factor << (Atom | UnaryOp + Factor) # [sic]
Term = Factor + ZeroOrMore(MulOp + Factor)
simpleExpression = Term + ZeroOrMore(AddOp + Term)

expression << (simpleExpression + ZeroOrMore(RelOp + simpleExpression))
assignment = expression + ASSIGN + expression
expressionOrAssignment = ~END + (assignment | expression) # Currently this NotAny(END) is the only distinction between this code and the grammar cited above
expressionOrRange = simpleExpression + ZeroOrMore(Literal('..') + simpleExpression)
expressionOrRangeList = expressionOrRange + ZeroOrMore(COMMA + expressionOrRange)
setLiteral << LBRACKET + expressionOrRangeList + RBRACKET

expressionList << (expression + ZeroOrMore(COMMA + expression))
parameterExpression << (expression + ZeroOrMore(COLON + expression))

block = Forward()
statement = Forward()
statementList = Forward()
withStatement = Group(WITH + expressionList + DO) + statement
ifStatement = IF + expression + THEN + statement + Optional(ELSE + statement) 
exceptionItem = ON + ident + COLON + qualifiedIdent + DO + statement + SEMICOLON
tryStatement = TRY + statementList + (FINALLY + statementList | EXCEPT + ZeroOrMore(exceptionItem) + ELSE + statementList)
statement << (block | withStatement | ifStatement | tryStatement | expressionOrAssignment )
#statement << simpleStatement # | Label + COLON + simpleStatement
statementList << OneOrMore(ZeroOrMore(statement) + SEMICOLON) # I also differ from the grammar here, where
block << (BEGIN + Optional(statementList) + END)

varSection = VAR + OneOrMore(Group(identList + COLON + _type + SEMICOLON))

implementationDecl = varSection #| constSection | typeSection | ...

fancyBlock = ZeroOrMore(implementationDecl) + block

methodReturnType = qualifiedIdent | QuotedString("'")
parameterType = methodReturnType
parameter = Optional(VAR | CONST) + identList + COLON + parameterType
methodHeading = ((FUNCTION + qualifiedIdent + LPAREN + ZeroOrMore(parameter + ZeroOrMore(SEMICOLON + parameter)) + RPAREN + COLON + methodReturnType + SEMICOLON) |
                (PROCEDURE + qualifiedIdent + LPAREN + ZeroOrMore(parameter + ZeroOrMore(SEMICOLON + parameter)) + RPAREN + SEMICOLON))

methodImplementation = methodHeading + fancyBlock + SEMICOLON

grammar = OneOrMore(methodImplementation)
grammar.ignore(dblSlashComment)

def main(argv):
    with open(argv, 'r') as f:
        string = f.read()
    grammar.parseString(string).pprint()


if __name__ == "__main__":
    import pprint, sys
    main(sys.argv[1])