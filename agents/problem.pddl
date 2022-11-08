(define(problem craft-bots-problem)

(:domain craft-bots)

(:objects
	a30 a29 a31 - actor
	t23 t24 t25 t26 t27 t28 - task
	n0 n1 n3 n5 n8 n10 n12 n15 n18 n21 - location
	m35 m33 m36 m34 m32 - mine
	r0 r1 r2 r3 r4 r5 - resource
	red blue orange black green - color
)
(:init
	(alocation a30 n15)
	(not (alocation a30 n0))
	(not (alocation a30 n1))
	(not (alocation a30 n3))
	(not (alocation a30 n5))
	(not (alocation a30 n8))
	(not (alocation a30 n10))
	(not (alocation a30 n12))
	(not (alocation a30 n18))
	(not (alocation a30 n21))
	(alocation a29 n15)
	(not (alocation a29 n0))
	(not (alocation a29 n1))
	(not (alocation a29 n3))
	(not (alocation a29 n5))
	(not (alocation a29 n8))
	(not (alocation a29 n10))
	(not (alocation a29 n12))
	(not (alocation a29 n18))
	(not (alocation a29 n21))
	(alocation a31 n15)
	(not (alocation a31 n0))
	(not (alocation a31 n1))
	(not (alocation a31 n3))
	(not (alocation a31 n5))
	(not (alocation a31 n8))
	(not (alocation a31 n10))
	(not (alocation a31 n12))
	(not (alocation a31 n18))
	(not (alocation a31 n21))

	(connected n1 n0)	(connected n0 n1)
	(connected n3 n1)	(connected n1 n3)
	(connected n5 n1)	(connected n1 n5)
	(connected n5 n3)	(connected n3 n5)
	(connected n8 n5)	(connected n5 n8)
	(connected n10 n8)	(connected n8 n10)
	(connected n12 n8)	(connected n8 n12)
	(connected n12 n10)	(connected n10 n12)
	(connected n15 n10)	(connected n10 n15)
	(connected n15 n12)	(connected n12 n15)
	(connected n18 n12)	(connected n12 n18)
	(connected n18 n15)	(connected n15 n18)
	(connected n21 n18)	(connected n18 n21)

	(dlocation m35 n0)
	(mine_color m35 black)
	(dlocation m33 n3)
	(mine_color m33 blue)
	(dlocation m36 n3)
	(mine_color m36 green)
	(dlocation m34 n5)
	(mine_color m34 orange)
	(dlocation m32 n15)
	(mine_color m32 red)

	(not (carrying a30 red))
	(not_carrying a30 red)
	(not (carrying a30 blue))
	(not_carrying a30 blue)
	(not (carrying a30 orange))
	(not_carrying a30 orange)
	(not (carrying a30 black))
	(not_carrying a30 black)
	(not (carrying a30 green))
	(not_carrying a30 green)

	(not (carrying a29 red))
	(not_carrying a29 red)
	(not (carrying a29 blue))
	(not_carrying a29 blue)
	(not (carrying a29 orange))
	(not_carrying a29 orange)
	(not (carrying a29 black))
	(not_carrying a29 black)
	(not (carrying a29 green))
	(not_carrying a29 green)

	(not (carrying a31 red))
	(not_carrying a31 red)
	(not (carrying a31 blue))
	(not_carrying a31 blue)
	(not (carrying a31 orange))
	(not_carrying a31 orange)
	(not (carrying a31 black))
	(not_carrying a31 black)
	(not (carrying a31 green))
	(not_carrying a31 green)


	(not (deposited a30 red n15))
	(not_deposited a30 red n15)
	(not (deposited a30 blue n15))
	(not_deposited a30 blue n15)
	(not (deposited a30 orange n15))
	(not_deposited a30 orange n15)
	(not (deposited a30 black n15))
	(not_deposited a30 black n15)
	(not (deposited a30 green n15))
	(not_deposited a30 green n15)

	(not (deposited a29 red n15))
	(not_deposited a29 red n15)
	(not (deposited a29 blue n15))
	(not_deposited a29 blue n15)
	(not (deposited a29 orange n15))
	(not_deposited a29 orange n15)
	(not (deposited a29 black n15))
	(not_deposited a29 black n15)
	(not (deposited a29 green n15))
	(not_deposited a29 green n15)

	(not (deposited a31 red n15))
	(not_deposited a31 red n15)
	(not (deposited a31 blue n15))
	(not_deposited a31 blue n15)
	(not (deposited a31 orange n15))
	(not_deposited a31 orange n15)
	(not (deposited a31 black n15))
	(not_deposited a31 black n15)
	(not (deposited a31 green n15))
	(not_deposited a31 green n15)


	(not (create_site n15))
	(not_created_site n15)
	(= (color_count red n15) 1)
	(= (color_count blue n15) 1)
	(= (color_count orange n15) 2)
	(= (color_count black n15) 1)
)
(:goal
	(and
		(= (color_count red n15) 0)
		(= (color_count blue n15) 0)
		(= (color_count orange n15) 0)
		(= (color_count black n15) 0)
)))
