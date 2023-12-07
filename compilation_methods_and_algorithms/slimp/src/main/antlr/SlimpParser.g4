parser grammar SlimpParser;

@header {
package com.slimp.generated;
}

options {
    tokenVocab = SlimpLexer;
}

program
    : declaration* EOF
    ;

declaration
    : globalVariable
    | function
    ;

globalVariable
    : pattern '=' expression ';'
    ;

function
    : 'fun' IDENTIFIER '(' functionParams? ')' (':' type)? block
    ;

functionParams
    :   functionParam (',' functionParam)* ','?
    ;

functionParam
    : '&'? typedIdentifier
    ;

block
    : '{' statement* '}'
    ;

statement
    : ';'                                                   #EmptyStatement
    | pattern '=' expression ';'                            #AssignmentStatement
    | expression ';'                                        #ExpressionStatement
    | (ifStatement | forLoop | whileLoop)                   #BlockStatement
    | 'return' expression? ';'                              #ReturnStatement
    | ('break' | 'continue')                                #LoopControlStatement
    ;

ifStatement
    : 'if' expression block
    (
        'else' (block | ifStatement)
    )?
    ;

forLoop
    : 'for' IDENTIFIER /** hack, should be `pattern` */ '<-' expression block
    ;

whileLoop
    : 'while' expression block
    ;

expression
    : IDENTIFIER                                #IdentifierExpression
    | '@parent' IDENTIFIER                      #ParentIdentifierExpression
    | literal                                   #LiteralExpression
    | IDENTIFIER '(' expressionElements ')'     #FunctionCallExpression
    | expression '[' expression ']'             #IndexingExpression
    | expression 'as' type                      #TypeCastExpression
    | expression arithmeticOperator expression  #ArithmeticExpression
    | '-' expression                            #ArithmeticExpression
    | expression comparisonOperator expression  #ComparisonExpression
    | expression logicalOperator expression     #LogicalExpression
    | '!' expression                            #LogicalExpression
    | expression '..' expression                #RangeExpression
    | '(' expression ')'                        #ParenthesizedExpression
    | '(' expressionElements ')'                #TupleExpression
    | '[' expressionElements ']'                #ArrayExpression
    | '{' mapExpressionElements '}'             #MapExpression
    ;

expressionElements
    : (expression ',')* expression?
    ;

mapExpressionElements
    : (expression '->' expression ',')* (expression '->' expression)?
    ;

logicalOperator
    : '&&'
    | '||'
    ;

comparisonOperator
    : '=='
    | '!='
    | '>'
    | '<'
    | '>='
    | '<='
    ;

arithmeticOperator
    : '+'
    | '-'
    | '*'
    | '/'
    | '//'
    | '%'
    ;

literal
    : INTEGER_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | STRING_LITERAL
    | KW_FALSE
    | KW_TRUE
    ;

typedIdentifier
    : IDENTIFIER ':' type
    ;

type
    : IDENTIFIER                    #TypeIdentifier
    | '(' type ')'                  #ParenthesizedType
    | '(' tupleTypeElements ')'     #TupleType
    | '[' type ';' expression ']'   #ArrayType
    | '{' type '->' type '}'        #MapType
    ;

tupleTypeElements
    : (type ',')* type?
    ;

pattern
    : IDENTIFIER                    #UntypedPatternIdentifier
    | typedIdentifier               #TypedPatternIdentifier
/** | literal                       #PatternLiteral
    | '_'                           #WildCardPattern
    | '(' pattern ')'               #ParenthesizedPattern
    | '(' patternElements ')'       #TuplePattern
    | '[' patternElements ']'       #ArrayPattern
    | '{' mapPatternElements '}'    #MapPattern */
    ;

patternElements
    : (pattern ',')* pattern?
    ;

mapPatternElements
    : (pattern '->' pattern ',')* (pattern '->' pattern)?
    ;
