Feature: Reproduce Halfar analytic solution
        In order to perform SIA simulations that are accurate
        As an MPAS Developer
        I want MPAS-Land Ice SIA simulations to reproduce the Halfar analytic solution across different decompositions.

	Scenario: 1 procs with dome shallow-ice
		Given A "dome" test
		When I perform a 1 processor MPAS "landice_model_testing" run
		When I compute the Halfar RMS
		Then I see Halfar thickness RMS of <10m

	Scenario: 4 procs with dome shallow-ice
		Given A "dome" test
		When I perform a 4 processor MPAS "landice_model_testing" run
		When I compute the Halfar RMS
		Then I see Halfar thickness RMS of <10m

