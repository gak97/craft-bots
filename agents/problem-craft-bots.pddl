;; problem file for the domain-craft-bots.pddl file

(define (problem actors) 
(:domain craft-bots)
(:objects 
    ;; 1 actor 10 nodes 6 tasks 5 resources 4 sites 3 mines 1 building
    a1 - actor
    n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 - location
    t1 t2 t3 t4 t5 t6 - task
    r1 r2 r3 r4 r5 - resource
    m1 m2 m3 - mine
    b1 - building
    c1 - color
)

(:init
    (alocation a1 n1)
    (dlocation m1 n2)

    (not (create_site a1 n1))
    (not_created_site a1 n3)

    (not (mining a1 r1))
    (not_mining a1 r1)

    (not (rcolor r1 c1))

    (not (carrying a1 r1))
    (not_carrying a1 r1)

    (not (deposited a1 r1 c1 n3))
    (not_deposited a1 r1 c1 n3)
    
    (not (constructed a1 r1 c1 n3))
    (not_constructed a1 r1 c1 n3)

    (connected n1 n2)
    (connected n2 n3)
    (connected n3 n4)
    (connected n4 n5)
    (connected n5 n1)
)

(:goal 
    (and
        ;; move the actor to the mine and dig the resource
        (alocation a1 n2)
        ; (mining a1 r1)
        ; (carrying a1 r1)
        (create_site a1 n3)
        ; (deposited a1 r1 c1 n3)
        ; (constructed a1 r1 c1 n3)
    )
)

)