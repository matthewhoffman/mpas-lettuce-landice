Feature: Bit-Reproducible simulations
        In order to perform simulations using varying decompositions
        As an MPAS Developer
        I want MPAS-Land Ice simulations to be bit-reproducible across different decompositions.

	Scenario: 2 vs 4 procs with dome shallow-ice
		Given A setup test environment
		Given A "dome" "sia" test
		When I perform a 2 processor MPAS "landice_model_testing" run
		When I perform a 4 processor MPAS "landice_model_testing" run
		When I compute the RMS of "thickness"
		Then I see "thickness" RMS of 0

	Scenario: 1 vs 4 procs with dome shallow-ice
		Given A setup test environment
		Given A "dome" "sia" test
		When I perform a 1 processor MPAS "landice_model_testing" run
		When I perform a 4 processor MPAS "landice_model_testing" run
		When I compute the RMS of "thickness"
		Then I see "thickness" RMS of 0

