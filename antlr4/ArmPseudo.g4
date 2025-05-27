grammar ArmPseudo;

program: statement+ EOF;

statement
    : assignment ';'
    | functionCall ';'
    | loopStmt
    | ifStmt
    ;

assignment
    : type IDENTIFIER ('=' expression)?
    | IDENTIFIER '[' indexList ']' '=' expression
    | IDENTIFIER '=' expression
    ;


loopStmt
    : 'for' IDENTIFIER '=' expression 'to' expression block
    ;

ifStmt
    : 'if' condition 'then' block ('else' block)?
    ;

condition
    : expression
    ;

block
    : '{' statement* '}'
    ;

functionCall
    : IDENTIFIER '(' argumentList? ')'
    ;

expression
    : expression ('+' | '-' | '*' | '/' | '<<' | '>>' | '&' | '|') expression
    | '(' expression ')'
    | IDENTIFIER
    | IDENTIFIER '[' indexList ']'
    | INTEGER
    ;

indexList
    : expression (',' expression)*
    ;

argumentList
    : expression (',' expression)*
    ;

type
    : 'bits' '(' IDENTIFIER ')'
    | 'integer'
    ;

IDENTIFIER: [a-zA-Z_] [a-zA-Z_0-9]*;
INTEGER: [0-9]+;
WS: [ \t\r\n]+ -> skip;

COMMENT: '//' ~[\r\n]* -> skip;
