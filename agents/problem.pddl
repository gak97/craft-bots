(define(problem craft-bots-problem)

(:domain craft-bots)

(:objects
	a21 a22 a20 - actor
	t19 - task
	n0 n1 n3 n5 n7 n9 n11 n13 n15 n17 - location
	m23 m25 m26 m24 m27 - mine
	red blue orange black green - color
)
(:init
	(alocation a21 n1)
	(not (alocation a21 n0))
	(not (alocation a21 n3))
	(not (alocation a21 n5))
	(not (alocation a21 n7))
	(not (alocation a21 n9))
	(not (alocation a21 n11))
	(not (alocation a21 n13))
	(not (alocation a21 n15))
	(not (alocation a21 n17))
	(alocation a22 n5)
	(not (alocation a22 n0))
	(not (alocation a22 n1))
	(not (alocation a22 n3))
	(not (alocation a22 n7))
	(not (alocation a22 n9))
	(not (alocation a22 n11))
	(not (alocation a22 n13))
	(not (alocation a22 n15))
	(not (alocation a22 n17))
	(alocation a20 n17)
	(not (alocation a20 n0))
	(not (alocation a20 n1))
	(not (alocation a20 n3))
	(not (alocation a20 n5))
	(not (alocation a20 n7))
	(not (alocation a20 n9))
	(not (alocation a20 n11))
	(not (alocation a20 n13))
	(not (alocation a20 n15))

	(connected n1 n0)	(connected n0 n1)
	(connected n3 n1)	(connected n1 n3)
	(connected n5 n3)	(connected n3 n5)
	(connected n7 n5)	(connected n5 n7)
	(connected n9 n7)	(connected n7 n9)
	(connected n11 n9)	(connected n9 n11)
	(connected n13 n11)	(connected n11 n13)
	(connected n15 n13)	(connected n13 n15)
	(connected n17 n15)	(connected n15 n17)

	(dlocation m23 n0)
	(mine_color m23 red)
	(dlocation m25 n5)
	(mine_color m25 orange)
	(dlocation m26 n9)
	(mine_color m26 black)
	(dlocation m24 n13)
	(mine_color m24 blue)
	(dlocation m27 n17)
	(mine_color m27 green)

	(not (carrying a21 red))
	(not_carrying a21 red)
	(not (carrying a21 blue))
	(not_carrying a21 blue)
	(not (carrying a21 orange))
	(not_carrying a21 orange)
	(not (carrying a21 black))
	(not_carrying a21 black)
	(not (carrying a21 green))
	(not_carrying a21 green)

	(not (carrying a22 red))
	(not_carrying a22 red)
	(not (carrying a22 blue))
	(not_carrying a22 blue)
	(not (carrying a22 orange))
	(not_carrying a22 orange)
	(not (carrying a22 black))
	(not_carrying a22 black)
	(not (carrying a22 green))
	(not_carrying a22 green)

	(not (carrying a20 red))
	(not_carrying a20 red)
	(not (carrying a20 blue))
	(not_carrying a20 blue)
	(not (carrying a20 orange))
	(not_carrying a20 orange)
	(not (carrying a20 black))
	(not_carrying a20 black)
	(not (carrying a20 green))
	(not_carrying a20 green)

	(not (deposited a21 red n13))
	(not_deposited a21 red n13)
	(not (deposited a21 blue n13))
	(not_deposited a21 blue n13)
	(not (deposited a21 orange n13))
	(not_deposited a21 orange n13)
	(not (deposited a21 black n13))
	(not_deposited a21 black n13)
	(not (deposited a21 green n13))
	(not_deposited a21 green n13)

	(not (deposited a22 red n13))
	(not_deposited a22 red n13)
	(not (deposited a22 blue n13))
	(not_deposited a22 blue n13)
	(not (deposited a22 orange n13))
	(not_deposited a22 orange n13)
	(not (deposited a22 black n13))
	(not_deposited a22 black n13)
	(not (deposited a22 green n13))
	(not_deposited a22 green n13)

	(not (deposited a20 red n13))
	(not_deposited a20 red n13)
	(not (deposited a20 blue n13))
	(not_deposited a20 blue n13)
	(not (deposited a20 orange n13))
	(not_deposited a20 orange n13)
	(not (deposited a20 black n13))
	(not_deposited a20 black n13)
	(not (deposited a20 green n13))
	(not_deposited a20 green n13)

	(not (create_site n13))
	(not_created_site n13)
	(= (color_count blue n13) 1)
	(= (color_count black n13) 1)
)
(:goal
	(and
		(= (color_count blue n13) 0)
		(= (color_count black n13) 0)
)))
