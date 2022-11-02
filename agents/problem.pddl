(define(problem craft-bots-problem)

(:domain craft-bots)

(:objects
	a31 a30 a29 - actor
	t23 t24 t25 t26 t27 t28 - task
	n0 n1 n3 n6 n9 n11 n13 n15 n17 n20 - location
	m36 m33 m35 m32 m34 - mine
)
(:init
	(alocation a31 n1)
	(not (alocation a31 n0))
	(not (alocation a31 n3))
	(not (alocation a31 n6))
	(not (alocation a31 n9))
	(not (alocation a31 n11))
	(not (alocation a31 n13))
	(not (alocation a31 n15))
	(not (alocation a31 n17))
	(not (alocation a31 n20))
	(alocation a30 n1)
	(not (alocation a30 n0))
	(not (alocation a30 n3))
	(not (alocation a30 n6))
	(not (alocation a30 n9))
	(not (alocation a30 n11))
	(not (alocation a30 n13))
	(not (alocation a30 n15))
	(not (alocation a30 n17))
	(not (alocation a30 n20))
	(alocation a29 n1)
	(not (alocation a29 n0))
	(not (alocation a29 n3))
	(not (alocation a29 n6))
	(not (alocation a29 n9))
	(not (alocation a29 n11))
	(not (alocation a29 n13))
	(not (alocation a29 n15))
	(not (alocation a29 n17))
	(not (alocation a29 n20))
	(connected n1 n0)	(connected n0 n1)
	(connected n3 n0)	(connected n0 n3)
	(connected n6 n0)	(connected n0 n6)
	(connected n3 n1)	(connected n1 n3)
	(connected n6 n3)	(connected n3 n6)
	(connected n9 n6)	(connected n6 n9)
	(connected n11 n9)	(connected n9 n11)
	(connected n13 n11)	(connected n11 n13)
	(connected n15 n13)	(connected n13 n15)
	(connected n17 n13)	(connected n13 n17)
	(connected n17 n15)	(connected n15 n17)
	(connected n20 n15)	(connected n15 n20)
	(connected n20 n17)	(connected n17 n20)
	(dlocation m36 n0)
	(dlocation m33 n13)
	(dlocation m35 n15)
	(dlocation m32 n17)
	(dlocation m34 n20)
)
(:goal
	(and
		(alocation a31 n0)
		(alocation a30 n0)
		(alocation a29 n0)
)))
