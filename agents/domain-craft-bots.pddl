;; write the domain file to match the PDDL Interface python file

;; scenario includes 3 actors moving between 10 locations connected by edges
;; aim of the scenario is for the actors to use the resources to construct as many buildings as possible

;; resources can be gathered at mines by mining and carried by actors, using pick up, deposit, and drop
;; resources come in five types: red, green, blue, black, and orange
;; actors can start construction at any location. Actors should deposit resources into partially constructed buildings 
;; and then spend time constructing, until the building is complete

;; buildings require different resources, and completing a building will improve the score, with the aim being to
;; complete as many buildings as possible

(define (domain craft-bots)

    (:requirements :strips :typing :numeric-fluents :negative-preconditions)

    (:types
        actor location resource building site mine edge node task color - object
    )

    (:predicates
        (alocation ?a - actor ?l - location)
        (connected ?l1 - location ?l2 - location)
        (rlocation ?l - location ?c - color)
        
        (blocation ?b - building ?l - location)
        (not_blocation ?b - building ?l - location)
        
        (create_site ?l - location)
        (not_created_site ?l - location)
        
        (slocation ?s - site ?l - location)
        (dlocation ?m - mine ?l - location)
        
        (carrying ?a - actor ?c - color)
        (not_carrying ?a - actor ?c - color)
        
        ; (mining ?r - resource)
        ; (not_mining ?r - resource)
        (mine_color ?m - mine ?c - color)
        
        (rcolor ?r - resource ?c - color)
        (deposited ?a - actor ?c - color ?l - location)
        (not_deposited ?a - actor ?c - color ?l - location)

        (constructed ?c - color ?l - location)
        (not_constructed ?c - color ?l - location)
    )

    (:functions
        (color_count ?c - color ?l - location)
    )
    
    ;; agent moves between two nodes of the graph provided that the nodes are connected
    (:action move
        :parameters (?a - actor ?l1 - location ?l2 - location)
        :precondition (and (alocation ?a ?l1) (connected ?l1 ?l2))
        :effect (and (alocation ?a ?l2) (not (alocation ?a ?l1)))
    )

    ;; when the agent is at a node that contains a mine, the agent produces one resource of the mine’s resource type. 
    ;; the resource appears on the ground at that node
    (:action dig
        :parameters (?a - actor ?m - mine ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (dlocation ?m ?l) (mine_color ?m ?c))
        :effect (and (rlocation ?l ?c))
    )

    ;; agent collects a resource on the ground in the same node and adds it to the agent’s inventory
    (:action pick-up
        :parameters (?a - actor ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (rlocation ?l ?c) (not_carrying ?a ?c))
        :effect (and (carrying ?a ?c) (not (rlocation ?l ?c)) (not (not_carrying ?a ?c)))
    )

    ;; agent removes one resource from its inventory and adds it to the ground at the current node
    (:action drop
        :parameters (?a - actor ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (carrying ?a ?c))
        :effect (and (rlocation ?l ?c) (not (carrying ?a ?c)) (not_carrying ?a ?c))
    )

    ;; create a new site at the given node and add it to the list of sites
    (:action create-site
        :parameters (?a - actor ?l - location)
        :precondition (and (alocation ?a ?l) (not_created_site ?l))
        :effect (and (create_site ?l) (not (not_created_site ?l)))
    )

    ;; agent removes one resource from its inventory and adds it to a site at the current node. 
    ;; resources cannot be recovered once deposited into a site
    (:action deposit
        :parameters (?a - actor ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (carrying ?a ?c) (not_deposited ?a ?c ?l) (create_site ?l))
        :effect (and (not (carrying ?a ?c)) (deposited ?a ?c ?l) (not (not_deposited ?a ?c ?l)) (not_carrying ?a ?c))
    )

    ;; progresses the completion of a site at the current node. The completion is bounded by the fraction of required resources 
    ;; that have been deposited. Once complete, the site will transform into a completed building
    (:action construct
        :parameters (?a - actor ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (deposited ?a ?c ?l) (> (color_count ?c ?l) 0))
        :effect (and (not (deposited ?a ?c ?l)) (decrease (color_count ?c ?l) 1))
    )
)