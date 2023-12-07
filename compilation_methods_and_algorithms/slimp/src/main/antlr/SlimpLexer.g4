lexer grammar SlimpLexer;

@header {
package com.slimp.generated;
}

// keywords

KW_AS: 'as';
KW_BREAK: 'break';
KW_CONTINUE: 'continue';
KW_ELSE: 'else';
KW_FALSE: 'false';
KW_FN: 'fun';
KW_FOR: 'for';
KW_IF: 'if';
KW_RETURN: 'return';
KW_TRUE: 'true';
KW_WHILE: 'while';
KW_PARENT: '@parent';

// identifier

IDENTIFIER: [a-zA-Z_][a-zA-Z_0-9]*;

// comment

COMMENT: '#' ~[\r\n\u2028\u2029]* -> channel(HIDDEN);

// whitespace and newline

WHITESPACE: [\p{Zs}] -> channel(HIDDEN);
NEWLINE: ('\r\n' | [\r\n]) -> channel(HIDDEN);

// literals

INTEGER_LITERAL
    : DEC_LITERAL
    | BIN_LITERAL
    | OCT_LITERAL
    | HEX_LITERAL
    ;

DEC_LITERAL: DEC_DIGIT (DEC_DIGIT | '_')*;

HEX_LITERAL: '0x' '_'* HEX_DIGIT (HEX_DIGIT | '_')*;

OCT_LITERAL: '0o' '_'* OCT_DIGIT (OCT_DIGIT | '_')*;

BIN_LITERAL: '0b' '_'* [01] [01_]*;

FLOAT_LITERAL
    : DEC_LITERAL '.' DEC_LITERAL FLOAT_EXPONENT?
    | '.' DEC_LITERAL FLOAT_EXPONENT?
    | DEC_LITERAL FLOAT_EXPONENT?
   ;

CHAR_LITERAL
   : '\''
   (
      ~['\\\n\r\t]
      | QUOTE_ESCAPE
      | ASCII_ESCAPE
   ) '\''
   ;

STRING_LITERAL
   : '"'
   (
      ~["]
      | QUOTE_ESCAPE
      | ASCII_ESCAPE
      | ESC_NEWLINE
   )* '"'
   ;
   
// symbols
LUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';
SLASHSLASH: '//';
PERCENT: '%';
NOT: '!';
AND: '&';
ANDAND: '&&';
OROR: '||';
EQ: '=';
EQEQ: '==';
NE: '!=';
GT: '>';
LT: '<';
GE: '>=';
LE: '<=';
UNDERSCORE: '_';
DOT: '.';
DOTDOT: '..';
COMMA: ',';
SEMI: ';';
COLON: ':';
LARROW: '<-';
RARROW: '->';
POUND: '#';

LCURLYBRACE: '{';
RCURLYBRACE: '}';
LSQUAREBRACKET: '[';
RSQUAREBRACKET: ']';
LPAREN: '(';
RPAREN: ')';


// fragment rules

fragment DEC_DIGIT: [0-9];
fragment OCT_DIGIT: [0-7];
fragment HEX_DIGIT: [0-9a-fA-F];

fragment FLOAT_EXPONENT: [eE] [+-]? '_'* DEC_LITERAL;

fragment ASCII_ESCAPE: '\\x' OCT_DIGIT HEX_DIGIT | COMMON_ESCAPE;
fragment BYTE_ESCAPE: '\\x' HEX_DIGIT HEX_DIGIT | COMMON_ESCAPE;
fragment COMMON_ESCAPE: '\\' [nrt\\0];
fragment QUOTE_ESCAPE: '\\' ['"];
fragment ESC_NEWLINE: '\\' '\n';
