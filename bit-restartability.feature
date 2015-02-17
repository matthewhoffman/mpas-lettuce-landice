Feature: Bit-Restartable simulations
	In order to perform simulations using restarts
	As an MPAS Developer
	I want MPAS-Land Ice simulations to be bit-restartable across different decompositions.

	Scenario: 4 vs 4 procs with dome shallow-ice
		Given A "dome" test
		When I perform a 4 processor MPAS "landice_model_testing" run
		When I perform a 4 processor MPAS "landice_model_testing" run with restart
		When I compute the RMS of "thickness"
		Then I see "thickness" RMS of 0

	Scenario: 1 vs 4 procs with dome shallow-ice
		Given A "dome" test
		When I perform a 1 processor MPAS "landice_model_testing" run
		When I perform a 4 processor MPAS "landice_model_testing" run with restart
		When I compute the RMS of "thickness"
		Then I see "thickness" RMS of 0


