Feature: Reproduce EISMINT2 benchmark solutions
        In order to perform thermomechanically coupled simulations that are accurate
        As an MPAS Developer
        I want MPAS-Land Ice SIA simulations to match the EISMINT2 benchmark solutions.

	Scenario: 1 procs with EISMINT2-a SIA
		Given A setup test environment
		Given A "EISMINT2" test
		Given EISMINT2 experiment "a" 
		When I perform a 4 processor MPAS "landice_model_testing" run
		Then I see a MPAS results within range of EISMINT2 experiment "a" benchmarks.


