similar_5(X, Y) :-
    (
        same_actors3(X, Y)
    ;
        same_actors2(X, Y),
        same_genres1(X, Y)
    ;
        same_director(X, Y),
        same_genres1(X, Y)
    ;
        similar_plot3(X, Y)
    ).
similar_4(X, Y) :-
    (
        similar_5(X, Y)
    ;
        same_actors2(X, Y)
    ;
        similar_plot2(X, Y) 
    ;
        same_director(X, Y)
    ;
        same_foreign_language(X, Y),
        same_genres1(X, Y)
    ;
        same_genres3(X, Y),
        similar_plot1(X, Y)
    ).
similar_3(X, Y) :-
    (
        similar_4(X, Y)
    ;
        similar_plot1(X, Y)
    ;
        same_actors1(X, Y),
        same_genres2(X, Y)
    ;
        same_decade(X, Y),
        same_genres2(X, Y)
    ).
similar_2(X, Y) :-
    (
        similar_3(X, Y)
    ;
        same_production_companies(X, Y),
        same_genres1(X, Y)
    ;
        same_actors1(X, Y),
        same_genres1(X, Y)
    ).
similar_1(X, Y) :-
    (
        similar_2(X, Y)
    ;
        same_genres1(X, Y)
    ;
        same_actors1(X, Y)
    ).

new_similar_3(X, Y) :-
(
    same_genres3(X, Y),
    good_movie(Y)
;
    great_movie(Y),
    same_genres2(X, Y)
;
    similar_plot3(X, Y),
    ok_movie(Y)
;
    same_director(X, Y),
    good_movie(Y)
;
    same_actors2(X, Y),
    good_movie(Y)
;
    same_production_companies(X, Y),
    good_movie(Y)
).
new_similar_2(X, Y) :-
(
    good_movie(Y),
    same_genres1(X, Y)
;
    same_genres2(X, Y),
    ok_movie(Y)
;
    good_movie(Y),
    same_actors1(X, Y)
;
    ok_movie(Y),
    similar_plot2(X, Y)
;
    ok_movie(Y),
    same_production_companies(X, Y)
).
new_similar_1(X, Y) :-
(
    similar_plot1(X, Y),
    ok_movie(Y)
;
    same_genres1(X, Y),
    ok_movie(Y)
).
