Feature: No answer changes
	In order to avoid changing answers from previous versions of the model
	As an MPAS Developer
	I want MPAS-Land Ice simulations to be bit-for-bit identical to a trusted version of the model.

	Scenario: 1 vs 1 procs with dome shallow-ice against trusted
		Given A "dome" test for "testing"
		Given A "dome" test for "trusted"
		When I perform a 1 processor MPAS "landice_model_testing" run
		When I perform a 1 processor MPAS "landice_model_trusted" run
		When I compute the RMS of "thickness"
		Then I see "thickness" RMS of 0
		When I compute the RMS of "normalVelocity"
		Then I see "normalVelocity" RMS of 0

	Scenario: 4 vs 4 procs with dome shallow-ice against trusted
		Given A "dome" test for "testing"
		Given A "dome" test for "trusted"
		When I perform a 4 processor MPAS "landice_model_testing" run
		When I perform a 4 processor MPAS "landice_model_trusted" run
		When I compute the RMS of "thickness"
		Then I see "thickness" RMS of 0
		When I compute the RMS of "normalVelocity"
		Then I see "normalVelocity" RMS of 0

