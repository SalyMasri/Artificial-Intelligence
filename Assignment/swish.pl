%%  friends(-Solution)
%   @param  Solution is a list of friends that satisfy all constraints.

:- use_rendering(table,[header(p('Person', 'Season', 'Hobbies', 'Housing', 'Occupation'))]).

%Two people are neighbours if they live in the same type of housing.
neighbours(P1, P2, Ls) :-				
    member(p(P1, _, _, X, _),Ls),
    member(p(P2, _, _, Y, _),Ls),
    not(P1 == P2),
    X = Y.

% The facts:
fact1(Ls) :- 
    member(p(p1,_,_,house,_), Ls).
fact2(Ls) :- 
    member(p(p4, _, tennis, _, _), Ls).
fact3(Ls) :- 
    member(p(p3, _, football, _, _), Ls).
fact4(Ls) :-
    member(p(_, _, football, _, employee), Ls).
fact5(Ls) :-
    member(p(_, spring, _, _, unemployed), Ls).
fact6(Ls) :-
    member(p(_, summer, football, _, _), Ls),
    member(p(_, fall, dota2, _, _), Ls),
    member(p(_, winter, tennis, _, _), Ls),
    member(p(_, spring, lol, _, _), Ls).
fact7(Ls) :-
    member(p(_, _, dota2, house, employee), Ls).
fact8(Ls) :-
    member(p(_, winter, _, X, Y),Ls),
    not(X == house),
    Y = student.
fact9(Ls) :- 
    neighbours(p2, p4, Ls).
fact10(Ls) :-
    member(p(SummerLover, summer, _, _, _), Ls),
    neighbours(SummerLover, p2, Ls),
    not(neighbours(SummerLover, p1, Ls)).
fact11(Ls) :- 
    neighbours(p3, TennisPlayer, Ls),
    member(p(TennisPlayer, _, tennis, _, _), Ls).

% Problem:
friends(Ls) :-
    length(Ls, 4),						%There are 4 friends in our list Ls
    member(p(p1,_,_,_,_), Ls), member(p(p2,_,_,_,_), Ls), member(p(p3,_,_,_,_), Ls), member(p(p4,_,_,_,_), Ls), %One of them is p1, one is p2, one is p3, one is p4
    member(p(_,summer,_,_,_), Ls), member(p(_,fall,_,_,_), Ls), member(p(_,winter,_, _,_), Ls), member(p(_,spring,_, _,_), Ls), %One of them loves summer, one of them fall, one of them winter, one of them spring
    member(p(_,_,football,_,_), Ls), member(p(_,_,dota2, _,_), Ls), member(p(_,_,tennis, _,_), Ls), member(p(_,_,lol, _,_), Ls), %One of them plays football, one of them dota2, one of them tennis, and one of them lol
    member(p(_,_,_, house,_), Ls), member(p(_,_,_, apartment,_), Ls), %Some live in a house and some live in an apartment
    member(p(_,_,_, _,employee), Ls), member(p(_,_,_, _,student), Ls), member(p(_,_,_, _,unemployed), Ls), %Some are employees, some are students, some are unemployed
    fact1(Ls),
    fact2(Ls),
    fact3(Ls),
    fact4(Ls),
    fact5(Ls),
    fact6(Ls),
    fact7(Ls),
    fact8(Ls),
    fact9(Ls),
    fact10(Ls),
    fact11(Ls).
 
%To see the results, run ?- friends(Ls).
