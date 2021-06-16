grammar SPK;

program : function_* bigStmt* EOF;


bigStmt : (if_stat | while_stat | for_loop | declaration SEP | assignment SEP | print_ SEP | function_exec SEP | break_ SEP |sleep_ SEP);

// if_ : IF_ condition_block THEN_ block;
if_stat : IF_ condition_block (ELSE IF_ condition_block)* (ELSE block)?;
while_stat : WHILE expr THEN_ block;

for_loop : FOR VARIABLE_NAME IN iterable block;

print_ : PRINT_ expr ;

range_:  OSQBRACE FROM expr TO expr CSQBRACE;


condition_block : condition THEN_ block;
condition: expr;

block : OBRACE block CBRACE | OBRACE bigStmt+ CBRACE;
fblock : block;
function_ : FUN_ VARIABLE_NAME OPAR arguments CPAR (RETURNS returnable)? fblock ;
// function_body: OBRACE bigStmt+ CBRACE;
returnable: TYPE_NAME VARIABLE_NAME;
function_exec : VARIABLE_NAME OPAR arguments_exec CPAR;

arguments : ((TYPE_NAME VARIABLE_NAME ',')* TYPE_NAME VARIABLE_NAME)?;
arguments_exec : ((expr ',')* expr)?;

declaration : TYPE_NAME VARIABLE_NAME ASSIGN expr ;
assignment : VARIABLE_NAME list_index? ASSIGN expr ;

break_: BREAK_;
sleep_: SLEEP_ '(' expr ')';
TYPE_NAME : (INT | LIST | FLOATING | STRING_ | BOOL_ );
BOOL_ : 'LOGICZNA';
FUN_ : 'FUNKCJA';
INT : 'CA\u0141KOWITA' ;
LIST : 'LISTA';
FLOATING : 'U\u0141AMKOWA';
STRING_ : 'NAPIS';
IF_ : 'JE\u017BELI';
THEN_ : 'TO';
ELSE : 'INACZEJ';
WHILE: 'DOP\u00D3KI';
FOR: 'DLA';
IN: 'W';
PRINT_: 'WYPISZ';
LENGTH: 'D\u0141UGO\u015A\u0106';
FROM: 'OD';
TO: 'DO';
RETURNS: 'ZWRACA';
BREAK_: 'STOP';
TO_INT: 'JAKO_CA\u0141KOWITA';
TO_FLOAT: 'JAKO_U\u0141AMKOWA';
TO_STRING: 'JAKO_NAPIS';
SLEEP_: 'CZEKAJ';


expr
 : expr POW expr                        
 | expr op=(MULT | DIV | MOD) expr      
 | expr op=(PLUS | MINUS) expr          
 | expr op=(LTEQ | GTEQ | LT | GT) expr 
 | expr op=(EQ | NEQ) expr  
 | expr AND expr   
 | expr OR expr           
 | MINUS expr                           
 | NOT expr            
 | atom
 ;

atom
 : OPAR expr CPAR 
 | LENGTH '(' expr ')'
 | TO_INT '(' expr ')'
 | TO_FLOAT '(' expr ')'
 | TO_STRING '(' expr ')'
 | function_exec                     
 | INTEGER_NUMBER 
 | FLOAT_NUMBER
 | VARIABLE_NAME            
 | STRING  
 | BOOL_VALUE
 | range_
 | list_values  
 | list_element 
 ;

iterable
 : range_
 | list_values    
 | STRING
 | VARIABLE_NAME
 ;
BOOL_VALUE : 'Prawda' | 'Fa\u0142sz';


OR : 'LUB';
AND : 'ORAZ';
EQ : '==';
NEQ : '!=';
GT : '>';
LT : '<';
GTEQ : '>=';
LTEQ : '<=';
PLUS : '+';
MINUS : '-';
MULT : '*';
DIV : '/';
MOD : '%';
POW : '^';
NOT : '!';


VARIABLE_NAME
 : [a-zA-Z_\u00D3\u0104\u0105\u0106\u0107\u0118\u0119\u0141\u0142\u0143\u0144\u015A\u015B\u0179\u017A\u017B\u017C\u00F3] 
 [a-zA-Z_0-9\u00D3\u0104\u0105\u0106\u0107\u0118\u0119\u0141\u0142\u0143\u0144\u015A\u015B\u0179\u017A\u017B\u017C\u00F3]*
 ;

INTEGER_NUMBER : NON_ZERO_DIGIT DIGIT* | '0';
FLOAT_NUMBER : NON_ZERO_DIGIT DIGIT* '.' DIGIT+ | '0.' DIGIT+;
STRING
 : '"' (~["\r\n] | '""')* '"'
 ;
list_element: VARIABLE_NAME list_index;
list_values : '['((expr',')* expr)? ']';
list_index: OSQBRACE expr CSQBRACE;
NON_ZERO_DIGIT : [1-9];
DIGIT : [0-9];



ASSIGN : '=';
OPAR : '(';
CPAR : ')';
OBRACE : '{';
CBRACE : '}';
OSQBRACE : '[';
CSQBRACE : ']';


COMMENT
 : '??' ~[\r\n]* -> skip
 ;
SEP : ';';
WS : [ \t\r\n] -> skip;

OTHER
 : . 
 ;
