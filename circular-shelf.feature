Feature: Reproduce Circular Shelf benchmark solution
        In order to perform ice shelf simulations that are accurate
        As an MPAS Developer
        I want MPAS-Land Ice FO simulations to match the circular shelf benchmark solution across different decompositions.

	Scenario: 1 procs with circular-shelf first-order
		Given A setup test environment
		Given A "circular-shelf" test
		When I perform a 1 processor MPAS "landice_model_testing" run
		Then I see a circular-shelf maximum speed near 1918 m/yr

	Scenario: 4 procs with circular-shelf first-order
		Given A setup test environment
		Given A "circular-shelf" test
		When I perform a 4 processor MPAS "landice_model_testing" run
		Then I see a circular-shelf maximum speed near 1918 m/yr

