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
        (rlocation ?r - resource ?l - location)
        (blocation ?b - building ?l - location)
        (not_blocation ?b - building ?l - location)
        (slocation ?s - site ?l - location)
        (dlocation ?m - mine ?l - location)
        (carrying ?a - actor ?r - resource)
        (not_carrying ?a - actor ?r - resource)
        ; (built ?b - building)
        (mining ?a - actor ?r - resource)
        (not_mining ?a - actor ?r - resource)
        (rcolor ?r - resource ?c - color)
        (deposited ?a - actor ?r - resource ?c - color ?l - location)
        (not_deposited ?a - actor ?r - resource ?c - color ?l - location)
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
        :parameters (?a - actor ?m - mine ?r - resource ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (dlocation ?m ?l) (not_mining ?a ?r))
        :effect (and (mining ?a ?r) (rlocation ?r ?l) (rcolor ?r ?c) (not (not_mining ?a ?r)))
    )

    ;; agent collects a resource on the ground in the same node and adds it to the agent’s inventory
    (:action pick-up
        :parameters (?a - actor ?r - resource ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (rlocation ?r ?l) (rcolor ?r ?c) (not_carrying ?a ?r))
        :effect (and (carrying ?a ?r) (not (rlocation ?r ?l)) (not (mining ?a ?r)))
    )

    ;; agent removes one resource from its inventory and adds it to the ground at the current node
    (:action drop
        :parameters (?a - actor ?r - resource ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (carrying ?a ?r) (rcolor ?r ?c))
        :effect (and (rlocation ?r ?l) (not (carrying ?a ?r)) (not (rcolor ?r ?c)))
    )

    ;; agent removes one resource from its inventory and adds it to a site at the current node. 
    ;; resources cannot be recovered once deposited into a site
    (:action deposit
        :parameters (?a - actor ?r - resource ?s - site ?l - location ?c - color)
        :precondition (and (alocation ?a ?l) (carrying ?a ?r) (slocation ?s ?l) (rcolor ?r ?c) (not_deposited ?a ?r ?c ?l))
        :effect (and (not (carrying ?a ?r)) (not (rcolor ?r ?c)) (deposited ?a ?r ?c ?l) (not (not_deposited ?a ?r ?c ?l)))
    )

    ;; progresses the completion of a site at the current node. The completion is bounded by the fraction of required resources 
    ;; that have been deposited. Once complete, the site will transform into a completed building
    (:action construct
        :parameters (?a - actor ?s - site ?b - building ?l - location ?c - color, ?r - resource)
        :precondition (and (alocation ?a ?l) (slocation ?s ?l) (not_blocation ?b ?l) (deposited ?a ?r ?c ?l))
        :effect (and (not (slocation ?s ?l)) (blocation ?b ?l) (not (not_blocation ?b ?l)) (not (deposited ?a ?r ?c ?l)))
    )
)