%{
#include "wrapper.h"  /* Declares append_token() */
%}

%option noyywrap
%option caseless

/* Definitions */
DIGIT           [0-9]
LETTER          [a-zA-Z]
ID              {LETTER}([a-zA-Z0-9$_])*
STRING_SINGLE   \'([^\\\']|(\\.))*\'
STRING_DOUBLE   \"([^\\\"]|(\\.))*\'
BACKTICK        \`([^\\\`]|(\\.))*\`
WHITESPACE      [ \t\r\n]+

/* Comments:
   C-style comments, or -- comments (up to newline), or # comments */
COMMENT         (\/\*([^*]|\*+[^*/])*\*+\/)|(--[^\n]*)|(#.*)

/* Merge all keywords into one regex with alternation */
KEYWORDS        (SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|JOIN|INNER|LEFT|RIGHT|FULL|OUTER|ON|AS|VALUES|SET|CREATE|ALTER|DROP|TABLE|DATABASE|USE|INDEX|VIEW|TRIGGER|PROCEDURE|FUNCTION|IF|EXISTS|NULL|NOT|AND|OR|IN|LIKE|GROUP|BY|ORDER|HAVING|DISTINCT|LIMIT|OFFSET|UNION|ALL|ANY|CASE|WHEN|THEN|ELSE|END|PRIMARY|KEY|FOREIGN|REFERENCES|CHECK|DEFAULT|AUTO_INCREMENT|ENGINE|COMMENT)

/* Merge operators into one regex.
   Multi‑character operators come first */
OPERATORS       (<>|<=|>=|!=|=|<|>|!|\*|\/|\+|\-)

/* Merge punctuation into one regex */
PUNCTUATION     (\(|\)|,|;|\.)

%%

{WHITESPACE}              ;  /* Skip whitespace */
{COMMENT}                 { append_token("COMMENT"); }
{KEYWORDS}                { append_token("KEYWORD"); }
{DIGIT}+(\.{DIGIT}+)?      { append_token("NUMBER"); }
{STRING_SINGLE}           { append_token("STRING"); }
{STRING_DOUBLE}           { append_token("STRING"); }
{BACKTICK}                { append_token("IDENTIFIER"); }
{ID}                      { append_token("IDENTIFIER"); }
{OPERATORS}               { append_token("OPERATOR"); }
{PUNCTUATION}             { append_token("PUNCTUATION"); }
.                         { append_token("UNKNOWN"); }

%%
