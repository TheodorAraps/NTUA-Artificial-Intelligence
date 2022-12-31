% Για τα 1, 2, 3
% Returns a list of the genres of a movie, sorted
list_of_genres(X, L) :- 
    setof(G, genres(X, G), L).
same_genres3(X, Y) :-
    same_genres2(X, Y),
    list_of_genres(X, L1),
    list_of_genres(Y, L2),
    same_elements(L1, L2, Count),
    Count >= 4,
    X \= Y.
same_genres2(X, Y) :-
    list_of_genres(X, L1),
    list_of_genres(Y, L2),
    same_elements(L1, L2, Count),
    Count >= 2,
    X \= Y.
same_genres1(X, Y) :-
    list_of_genres(X, L1),
    list_of_genres(Y, L2),
    same_elements(L1, L2, Count),
    Count >= 1,
    X \= Y.

% Για το 4
same_director(X, Y) :- 
    director_name(X, D),
    director_name(Y, D),
    X \= Y.

% Για το 5, 6
list_of_plots(X, L) :- 
    setof(P, plot_keywords(X, P), L).
similar_plot3(X, Y) :-
    list_of_plots(X, L1),
    list_of_plots(Y, L2),
    same_elements(L1, L2, Count),
    X \= Y,
    Count >= 5.
similar_plot2(X, Y) :-
    list_of_plots(X, L1),
    list_of_plots(Y, L2),
    same_elements(L1, L2, Count),
    X \= Y,
    Count >= 3.
similar_plot1(X, Y) :-
    list_of_plots(X, L1),
    list_of_plots(Y, L2),
    same_elements(L1, L2, Count),
    Count >= 2,
    X \= Y.

% Για τα 7, 8, 9
% Returns a list of the 3 main actors of a movie, sorted
list_of_actors(X, L) :-
    actor_1_name(X, A1), 
    actor_2_name(X, A2), 
    actor_3_name(X, A3), 
    sort([A1, A2, A3], L).
same_elements([], _, 0).
same_elements([H1|T1], L2, Count) :-
    length([H1|T1], N1),
    length(L2, N2),
    (N1 =< N2 ->
        (
        member(H1, L2) -> 
            same_elements(T1, L2, Count2),
            Count is Count2 + 1
        ; 
            same_elements(T1, L2, Count)
        )
    ;   same_elements(L2, [H1|T1], Count)
    ).
same_actors3(X, Y):-
    list_of_actors(X, L1),
    list_of_actors(Y, L2),
    same_elements(L1, L2, 3),
    X \= Y.
same_actors2(X, Y):-
    list_of_actors(X, L1),
    list_of_actors(Y, L2),
    same_elements(L1, L2, 2),
    X \= Y.
same_actors1(X, Y) :- 
    list_of_actors(X, L1),
    list_of_actors(Y, L2),
    same_elements(L1, L2, 1),
    X \= Y.

% Για το 10:
same_language(X, Y) :-
	language(X, L),
	language(Y, L),
	X \= Y.
same_foreign_language(X, Y) :-
	language(X, L),
	language(Y, L),
	L \= 'English',
	X \= Y.
% Για το 11:
black_and_white(Y) :-
	setof(P, plot_keywords(Y, P), Plot),
	member('black and white', Plot). 

%12
same_production_companies(X, Y) :-
	production_companies(X, _, Company),
	production_companies(Y, _, Company),
	X \= Y.

%13
same_production_countries(X, Y) :-
	production_countries(X, _, Country),
	production_countries(Y, _, Country),
	X \= Y.

% 14: Συγκρινει ελέγχει αν έχουν ίδιο πηλίκο με το 10 (δηλαδή ίδια δεκαετία)
same_decade(X, Y) :-
	title_year(X, Y1),
	title_year(Y, Y2),
	atom_number(Y1, Year1),
	atom_number(Y2, Year2),
	div(Year1, 10) =:= div(Year2, 10),	
	X \= Y.

% Έξτρα κατηγορήματα
ok_movie(X) :-
    vote_average(X, R),
    atom_number(R, Rating),
    Rating >= 6,
    num_voted_users(X, V),
    atom_number(V, Voted),
    Voted >= 50.
good_movie(X) :-
    vote_average(X, R),
    atom_number(R, Rating),
    Rating >= 7,
    num_voted_users(X, V),
    atom_number(V, Voted),
    Voted >=50.
great_movie(X) :-
    vote_average(X, R),
    atom_number(R, Rating),
    Rating >= 8,
    num_voted_users(X, V),
    atom_number(V, Voted),
    Voted >=50.