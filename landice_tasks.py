import sys, os, glob, shutil, numpy, math
import subprocess
from netCDF4 import Dataset as NetCDFFile
from lettuce import *


dev_null = open(os.devnull, 'w')


# ==============================================================================
@step('A "([^"]*)" "([^"]*)" test')
def get_test_case(step, test, velocity_solver):
	world.basedir = os.getcwd()
	world.test = "%s"%(test)
	world.num_runs = 0

	# ===============
	#Setup trusted...
	# ===============

	# make trusted_tests directory it it doesn't already exist and cd to it.
	if not os.path.exists("%s/trusted_tests"%(world.basedir)):
		command = "mkdir"
		arg1 = "-p"
		arg2 = "%s/trusted_tests"%(world.basedir)
		subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	os.chdir("%s/trusted_tests"%(world.basedir))

	# get test tarball if we don't already have it
	if not os.path.exists("%s/trusted_tests/%s-2.0.tar.gz"%(world.basedir, world.test)):  # TODO Need to deal with version numbers
		command = "wget"
		arg1 = "%s/%s-2.0.tar.gz"%(world.trusted_url, world.test)  # TODO Need to deal with version numbers
		subprocess.call([command, arg1], stdout=dev_null, stderr=dev_null)

	# untar test if not already done and make a default namelist
	if not os.path.exists("%s/trusted_tests/%s"%(world.basedir, world.test)):
		command = "tar"
		arg1 = "xzf"
		arg2 = "%s-2.0.tar.gz"%world.test  # TODO Need to deal with version numbers
		subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)
		command = "cp"
		arg1 = "%s/namelist.input"%world.test
		arg2 = "%s/namelist.input.default"%world.test
		subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	# go into the test directory
	os.chdir("%s/trusted_tests/%s"%(world.basedir,world.test))

	# link executable
	command = "ln"
	arg1 = "-s"
	arg2 = "%s/trusted/landice_model"%(world.basedir)
	arg3 = "landice_model_trusted"
	subprocess.call([command, arg1, arg2, arg3], stdout=dev_null, stderr=dev_null)

	# copy default namelist to standard namelist
	command = "cp"
	arg1 = "namelist.input.default"
	arg2 = "namelist.input"
	subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	# remove any output files
	command = "rm"
	arg1 = "-f"
	arg2 = '\*.output.nc'
	subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	os.chdir(world.basedir)

	# ===============
	#Setup testing...
	# ===============

	# make testing_tests directory it it doesn't already exist and cd to it.
	if not os.path.exists("%s/testing_tests"%(world.basedir)):
		command = "mkdir"
		arg1 = "-p"
		arg2 = "%s/testing_tests"%(world.basedir)
		subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	os.chdir("%s/testing_tests"%(world.basedir))

	# get test tarball if we don't already have it
	if not os.path.exists("%s/testing_tests/%s-2.0.tar.gz"%(world.basedir, world.test)):   # TODO Need to deal with version numbers
		command = "wget"
		arg1 = "%s/%s-2.0.tar.gz"%(world.testing_url, world.test)  # TODO Need to deal with version numbers
		subprocess.call([command, arg1], stdout=dev_null, stderr=dev_null)

	# untar test if not already done and make a default namelist
	if not os.path.exists("%s/testing_tests/%s"%(world.basedir, world.test)):
		command = "tar"
		arg1 = "xzf"
		arg2 = "%s-2.0.tar.gz"%world.test  # TODO Need to deal with version numbers
		subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)
		command = "cp"
		arg1 = "%s/namelist.input"%world.test
		arg2 = "%s/namelist.input.default"%world.test
		subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	# go into the test directory
	os.chdir("%s/testing_tests/%s"%(world.basedir,world.test))

	# link executable
	command = "ln"
	arg1 = "-s"
	arg2 = "%s/testing/landice_model"%(world.basedir)
	arg3 = "landice_model_testing"
	subprocess.call([command, arg1, arg2, arg3], stdout=dev_null, stderr=dev_null)

	# copy default namelist to standard namelist
	command = "cp"
	arg1 = "namelist.input.default"
	arg2 = "namelist.input"
	subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	# remove any output files
	command = "rm"
	arg1 = "-f"
	arg2 = '\*.output.nc'
	subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

	os.chdir(world.basedir)


# ==============================================================================
@step('I compute the Halfar RMS')
def compute_rms(step):
	world.halfarRMS=float(subprocess.check_output('python ' + world.run1dir + '/halfar.py -f ' + world.run1 + ' -n | grep "^* RMS error =" | cut -d "=" -f 2 \n', shell='/bin/bash'))
	world.message = "      -- Halfar RMS (m) = " + str(world.halfarRMS) + " --"


# ==============================================================================
@step('I see Halfar thickness RMS of <10m')
def check_rms_values(step):
	if world.halfarRMS == []:
		assert False, 'Calculation of Halfar RMS failed.'
	else:
		assert world.halfarRMS < 10.0, 'Halfar RMS of %s is greater than 10.0 m'%world.halfarRMS



