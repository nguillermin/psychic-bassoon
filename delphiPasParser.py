from pyparsing import CaselessKeyword, Literal, ZeroOrMore, OneOrMore, Group, Optional, \
                        Combine, Forward, Word, FollowedBy, Suppress, QuotedString, \
                        nums, alphanums, printables, dblSlashComment, SkipTo, LineEnd

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
LTHANEQ = Combine(Literal('<') + FollowedBy('=') + Literal('='))
GTHANEQ = Combine(Literal('>') + FollowedBy('=') + Literal('='))
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
UNIT = CaselessKeyword('unit')
TYPE = CaselessKeyword('type')
IMPLEMENTATION = CaselessKeyword('implementation')
IN = CaselessKeyword('in')
CLASS = CaselessKeyword('class')
USES = CaselessKeyword('uses')
CONTAINS = CaselessKeyword('contains')
INTERFACE = CaselessKeyword('interface')
PRIVATE = CaselessKeyword('private')
PUBLIC = CaselessKeyword('public')
PROTECTED = CaselessKeyword('protected')
PUBLISHED = CaselessKeyword('published')
PROPERTY = CaselessKeyword('property')
MESSAGE = CaselessKeyword('message')
ARRAY = CaselessKeyword('array')
OF = CaselessKeyword('of')
STDCALL = CaselessKeyword('stdcall')
EXTERNAL = CaselessKeyword('external')
CASE = CaselessKeyword('case')

braceComment = Literal('{') + SkipTo(Literal('}')) + Literal('}')

ident = Word(alphanums + "_" + "#")
identList = ident + ZeroOrMore(COMMA + ident)
qualifiedIdent = ident + ZeroOrMore(PERIOD + ident)
_type = Forward()
retval = ident
RelOp = EQUALS | LTHANEQ | GTHANEQ | NEQUAL | LTHAN | GTHAN
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
expressionOrAssignment = ~FINALLY + ~EXCEPT + ~END + (assignment | expression) # NotAny(END), NotAny(EXCEPT) are not included in the above grammar
expressionOrRange = simpleExpression + ZeroOrMore(Literal('..') + simpleExpression)
expressionOrRangeList = expressionOrRange + ZeroOrMore(COMMA + expressionOrRange)
setLiteral << LBRACKET + expressionOrRangeList + RBRACKET

expressionList << (expression + ZeroOrMore(COMMA + expression))
parameterExpression << (expression + ZeroOrMore(COLON + expression))

block = Forward()
statement = Forward()
statementList = Forward()
withStatement = WITH + expressionList + DO + statement
ifStatement = IF + expression + THEN + statement + Optional(ELSE + statement) 
exceptionItem = ON + ident + COLON + qualifiedIdent + DO + statement + SEMICOLON
tryStatement = TRY + statementList +  ((FINALLY + statementList) | (EXCEPT + (statementList | (ZeroOrMore(exceptionItem) + Optional(ELSE + statementList))))) + END
caseSelector = OneOrMore(expressionOrRange + ZeroOrMore(COMMA + expressionOrRange)) + COLON + statement + SEMICOLON
caseStatement = CASE + expression + OF + OneOrMore(caseSelector) + Optional(ELSE + Optional(statementList)) + END
statement << (block | withStatement | ifStatement | tryStatement | caseStatement | expressionOrAssignment )
#statement << simpleStatement # | Label + COLON + simpleStatement
statementList << OneOrMore(ZeroOrMore(statement) + SEMICOLON) # I also differ from the grammar here, where
block << (BEGIN + Optional(statementList) + END)


typedConstant = Forward()
typedConstant = expression | (LPAREN + Optional( typedConstant + ZeroOrMore(COMMA + typedConstant) | ZeroOrMore(qualifiedIdent + COLON + typedConstant + SEMICOLON)) + RPAREN)
constSection = CONST + OneOrMore(ident + Optional(COLON + _type) + EQUALS + typedConstant + SEMICOLON)
classType = Forward()
typeDecl = ident + EQUALS + _type + SEMICOLON
typeSection = TYPE + OneOrMore(typeDecl)
varSection = VAR + OneOrMore(Group(identList + COLON + _type + SEMICOLON))
fieldDecl = identList + COLON + _type + SEMICOLON # Grammar seems to think semicolon here is optional, not really sure about that
fieldSection = Optional(VAR) + OneOrMore(fieldDecl)

methodReturnType = qualifiedIdent | QuotedString("'")
openArray = ARRAY + OF + (qualifiedIdent | QuotedString("'") | CONST)
parameterType = openArray | qualifiedIdent | QuotedString("'")
parameter = Optional(VAR | CONST) + identList + COLON + parameterType
directive = Optional(SEMICOLON) + ((MESSAGE + expression) | STDCALL | EXTERNAL + QuotedString("'"))
methodHeading = Optional(CLASS) + (FUNCTION | PROCEDURE) + qualifiedIdent + Optional(LPAREN + parameter + ZeroOrMore(SEMICOLON + parameter) + RPAREN) + Optional(COLON + methodReturnType) + ZeroOrMore(directive) + SEMICOLON + FollowedBy(~directive)

_property = Optional(CLASS) + PROPERTY + ident + Optional(LPAREN + parameter + ZeroOrMore(SEMICOLON + parameter) + RPAREN) + Optional(COLON + methodReturnType) + SEMICOLON
methodOrProperty = methodHeading | _property
visibilitySection = Optional(PRIVATE | PUBLIC | PROTECTED | PUBLISHED) + OneOrMore(fieldSection | methodOrProperty | constSection | typeSection)
classType << Group(CLASS + LPAREN + qualifiedIdent + ZeroOrMore(COMMA + qualifiedIdent) + RPAREN +      # "The remainder is optional, but only if the base class is specified and 
                ZeroOrMore(visibilitySection) + END)                                                    # lookahead shows that the next token is a semicolon" ~ NOT_IMPLEMENTED 
arrayType = ARRAY + Optional(LBRACKET + _type + ZeroOrMore(COMMA + _type) + RBRACKET) + OF + _type

_type << (classType | arrayType | expressionOrRange)

interfaceDecl = (typeSection | varSection | constSection | methodHeading)

fancyBlock = Forward()
methodImplementation = (methodHeading + fancyBlock + SEMICOLON)
implementationDecl = (constSection | typeSection | varSection | methodImplementation)
fancyBlock << (ZeroOrMore(implementationDecl) + block)

usedUnit = qualifiedIdent | ident + IN + QuotedString("'",unquoteResults=False) #qualifiedIdent instead of ident here
usesClause = (USES | CONTAINS) + OneOrMore(usedUnit + ZeroOrMore(COMMA + usedUnit)) + SEMICOLON

interfaceSection = INTERFACE + Optional(usesClause) + ZeroOrMore(interfaceDecl)

implementationSection = IMPLEMENTATION + Optional(usesClause) + ZeroOrMore(implementationDecl)

initSection = END #| block # | INITIALIZATION + statementList + FINALIZATION + statementList + END

unit = UNIT + ident + SEMICOLON + interfaceSection + implementationSection + initSection + PERIOD

grammar = unit
grammar.ignore(dblSlashComment)
grammar.ignore(braceComment)

PasParser = grammar

def main(argv):
    with open(argv, 'r') as f:
        string = f.read()
    grammar.parseString(string).pprint()


if __name__ == "__main__":
    import pprint, sys

    if len(sys.argv)==1:
        # run tests
        pass
    else:
        main(sys.argv[1])