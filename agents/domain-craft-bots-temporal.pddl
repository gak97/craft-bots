;; domain file for assignment-1 part-2

(define (domain craft-bots-temporal)

    (:requirements :strips :typing :equality :fluents :durative-actions :conditional-effects :negative-preconditions :timed-initial-literals)

    (:types
        actor location resource building site mine edge node task color - object
    )

    (:predicates 
        (alocation ?a - actor ?l - location)
        (connected ?l1 - location ?l2 - location)
        (rlocation ?l - location ?c - color)
        
        (create_site ?l - location)
        (not_created_site ?l - location)
        (dlocation ?m - mine ?l - location)
        
        (carrying ?a - actor ?c - color)
        (not_carrying ?a - actor ?c - color)
        (mine_color ?m - mine ?c - color)
        
        (deposited ?a - actor ?c - color ?l - location)
        (not_deposited ?a - actor ?c - color ?l - location)
        (not-same ?a1 ?a2 - actor)
        (is_orange ?c - color)
        (is_blue ?c - color)
        (not_orange ?c - color) 
        (not_blue ?c - color)
        
        (red_available)
        (not_resource_carrying ?a - actor)
        (is_red ?c - color)
        (not_red ?c - color)
        (not_green ?c - color)
        (is_black ?c - color)
        (not_black ?c - color)
)

    (:functions 
        (color_count ?c - color ?l - location)
        (edge_length ?l1 - location ?l2 - location)
        (move_speed ?a - actor)
        (mine_duration_blue ?m - mine)
        (mine_duration_orange ?m - mine)
        (mine_duration ?m - mine)
)

    (:durative-action move
        :parameters (?a - actor ?l1 - location ?l2 - location)
        ;; duration determined by actor move speed and edge length between locations
        :duration (= ?duration (/ (edge_length ?l1 ?l2) (move_speed ?a)))
        :condition (and 
            (at start (and 
                (alocation ?a ?l1) (connected ?l1 ?l2))
            )
            (over all (and 
                (connected ?l1 ?l2))
            )
        )
        :effect (and 
            (at end (and 
                (alocation ?a ?l2) (not (alocation ?a ?l1)))
            )
        )
    )

    (:durative-action create-site
        :parameters (?a - actor ?l - location)
        :duration (= ?duration 1)
        :condition (and 
            (at start (and 
                (alocation ?a ?l) (not_created_site ?l))
            )
            (over all (and 
                (alocation ?a ?l) (not_created_site ?l))
            )
        )
        :effect (and 
            (at end (and 
                (create_site ?l) (not (not_created_site ?l)))
            )
        )
    )
    
    ;; dig red, black or green resources
    (:durative-action dig
        :parameters (?a - actor ?m - mine ?l - location ?c - color)
        ;; duration determined by the mine's max progress and actor's mining rate
        :duration (= ?duration (mine_duration ?m))
        :condition (and 
            (over all (and 
                (alocation ?a ?l) (dlocation ?m ?l) (mine_color ?m ?c) (not_orange ?c) (not_blue ?c))
            )
        )
        :effect (and 
            (at end 
                (rlocation ?l ?c)
            )
        )
    )

    ;; blue resource takes twice as long to mine
    (:durative-action dig-blue
        :parameters (?a - actor ?m - mine ?l - location ?c - color)
        ;; duration determined by the mine's max progress and actor's mining rate
        :duration (= ?duration (mine_duration_blue ?m))
        :condition (and 
            (over all (and 
                (alocation ?a ?l) (dlocation ?m ?l) (mine_color ?m ?c) (is_blue ?c) (not_orange ?c))
            )
        )
        :effect (and 
            (at end 
                (rlocation ?l ?c)
            )
        )
    )

    ;; orange resource requires multiple actors to mine
    (:durative-action dig-orange
        :parameters (?a1 - actor ?a2 - actor ?m - mine ?l - location ?c - color)
        :duration (= ?duration (mine_duration_orange ?m))
        :condition (and 
            (over all (and 
                (alocation ?a1 ?l) (not-same ?a1 ?a2) (alocation ?a2 ?l) (dlocation ?m ?l) 
                (mine_color ?m ?c) (is_orange ?c) (not_blue ?c))
            )
        )
        :effect (and 
            (at end (and 
                (rlocation ?l ?c))
            )
        )
    )

    ;; red resource can only be collected within time interval 0-1200
    (:durative-action collect-red
        :parameters (?a - actor ?l - location ?c - color)
        :duration (= ?duration 1)
        :condition (and 
            (at start (and 
                (alocation ?a ?l) (rlocation ?l ?c) (not_carrying ?a ?c) (red_available) 
                (is_red ?c) (not_orange ?c) (not_blue ?c) (not_black ?c))
            )
            (over all (and 
                (rlocation ?l ?c) (not_carrying ?a ?c))
            )
        )
        :effect (and 
            (at end (and 
                (carrying ?a ?c) (not (rlocation ?l ?c)) (not (not_carrying ?a ?c)))
            )
        )
    )
    
    ;; black resource cannot be carried with any other resource
    (:durative-action collect-black
        :parameters (?a - actor ?l - location ?c - color)
        :duration (= ?duration 1)
        :condition (and 
            (at start (and 
                (alocation ?a ?l) (rlocation ?l ?c) (not_carrying ?a ?c) (not_resource_carrying ?a) 
                (is_black ?c) (not_orange ?c) (not_blue ?c) (not_red ?c))
            )
            (over all (and 
                (rlocation ?l ?c) (not_carrying ?a ?c))
            )
        )
        :effect (and 
            (at end (and 
                (carrying ?a ?c) (not (rlocation ?l ?c)) (not (not_carrying ?a ?c)) (not (not_resource_carrying ?a)))
            )
        )
    )
    
    (:durative-action pick-up
        :parameters (?a - actor ?l - location ?c - color)
        :duration (= ?duration 1)
        :condition (and 
            (at start (and 
                (alocation ?a ?l) (rlocation ?l ?c) (not_carrying ?a ?c) (not_resource_carrying ?a) (not_black ?c) (not_red ?c))
            )
            (over all (and 
                (rlocation ?l ?c) (not_carrying ?a ?c))
            )
        )
        :effect (and 
            (at end (and 
                (carrying ?a ?c) (not (not_carrying ?a ?c)) (not (rlocation ?l ?c)) (not (not_resource_carrying ?a)))
            )
        )
    )
    
    (:durative-action deposit
        :parameters (?a - actor ?l - location ?c - color)
        :duration (= ?duration 1)
        :condition (and 
            (at start (and 
                (alocation ?a ?l) (carrying ?a ?c) (not_deposited ?a ?c ?l) (create_site ?l))
            )
            (over all (and 
                (carrying ?a ?c) (not_deposited ?a ?c ?l))
            )
        )
        :effect (and 
            (at end (and 
                (deposited ?a ?c ?l) (not (not_deposited ?a ?c ?l)) (not (carrying ?a ?c)) 
                (not_carrying ?a ?c) (not_resource_carrying ?a))
            )
        )
    )
    
    (:durative-action construct
        :parameters (?a - actor ?l - location ?c - color)
        :duration (= ?duration 33) ;; construction duration is given by site_max_progress (100) / actor_build_speed (3) 
        :condition (and 
            (at start (and 
                (alocation ?a ?l) (deposited ?a ?c ?l) (> (color_count ?c ?l) 0))
            )
            (over all (and 
                (deposited ?a ?c ?l) (> (color_count ?c ?l) 0))
            )
        )
        :effect (and 
            (at end (and 
                (not (deposited ?a ?c ?l)) (decrease (color_count ?c ?l) 1) (not_deposited ?a ?c ?l))
            )
        )
    )
    
)