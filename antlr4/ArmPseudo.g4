grammar ArmPseudo;

program: statement+ EOF;

statement
    : assignment ';'
    | tupleAssignment ';'
    | functionCall ';'
    | loopStmt
    | ifStmt
    | caseStmt
    ;

assignment
    : type IDENTIFIER ('=' expression)?
    | IDENTIFIER slice? '=' expression
    | IDENTIFIER '[' indexList ']' '=' expression
    ;

tupleAssignment
    : '<' tupleElements '>' '=' expression
    ;

tupleElements
    : IDENTIFIER (',' IDENTIFIER)*
    ;

loopStmt
    : 'for' IDENTIFIER '=' expression 'to' expression block
    ;

ifStmt
    : 'if' condition 'then' block ('else' block)?
    ;

caseStmt
    : 'case' expression 'of' '{' whenClause+ '}'
    ;

whenClause
    : 'when' expression block
    ;

condition
    : expression
    ;

block
    : '{' statement* '}'
    ;

functionCall
    : scopedIdentifier '(' argumentList? ')'
    ;

expression
    : expression op=('EOR' | 'AND' | 'OR' | '*' | '/' | '+' | '-' | '<<' | '>>' | '&' | '|' | ':') expression # BinaryExpr
    | functionCall                                                                                          # FuncExpr
    | IDENTIFIER slice                                                                                      # SliceExpr
    | IDENTIFIER '[' indexList ']'                                                                          # IndexExpr
    | IDENTIFIER '[' ']'                                                                                    # EmptyIndexExpr
    | IDENTIFIER                                                                                            # IdentifierExpr
    | '(' expression ')'                                                                                    # ParenExpr
    | INTEGER                                                                                               # IntExpr
    ;

slice
    : '<' expression ':' expression '>'
    ;

indexList
    : expression (',' expression)*
    ;

argumentList
    : expression (',' expression)*
    ;

type
    : 'bits' '(' expression ')'
    | 'integer'
    ;

scopedIdentifier
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

IDENTIFIER: [a-zA-Z_] [a-zA-Z_0-9]*;
INTEGER: [0-9]+;
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;

