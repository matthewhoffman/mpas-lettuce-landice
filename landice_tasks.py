import sys, os, glob, shutil, numpy, math
import subprocess
from netCDF4 import Dataset as NetCDFFile
from lettuce import *


dev_null = open(os.devnull, 'w')
#dev_null = None  # for debugging to see all errors

# ==============================================================================
@step('A "([^"]*)" test')
def get_test_case(step, test):
	world.basedir = os.getcwd()
	world.test = "%s"%(test)
	world.num_runs = 0

	# Setup both "trusted_tests" and "testing_tests" directories.  This loop ensures they are setup identically.
	for testtype in ('trusted', 'testing'):

			if testtype == 'trusted':
				test_url = world.trusted_url
			elif testtype == 'testing':
				test_url = world.testing_url

			# make trusted/testing_tests directory it it doesn't already exist and cd to it.
			testpath = world.basedir + '/' + testtype + '_tests'
			try: 
				os.makedirs(testpath)
			except OSError:
				if not os.path.isdir(testpath):  # if the directory already exists, don't raise an error
					raise
			os.chdir(testpath)

			# get test tarball if we don't already have it
			if not os.path.exists(world.basedir + '/' + testtype + '_tests/' + world.test + '-2.0.tar.gz'):
				try:
					command = "wget"
					arg1 = test_url+"/"+world.test+"-2.0.tar.gz"  # TODO Need to deal with version numbers
					arg2 = "--trust-server-names"  # if the server redirects to an error page, this prevents that page from being named the test archive name - which is confusing!
					subprocess.check_call([command, arg2, arg1], stdout=dev_null, stderr=dev_null)
				except:
					print "Error: unable to get test case archive\n"
					raise

			# delete test dir if it already exists.  Then untar it
			thistestpath = world.basedir + '/' + testtype + '_tests/' + world.test
			if os.path.exists(thistestpath):
				shutil.rmtree(thistestpath)
			try:
				command = "tar"
				arg1 = "xzf"
				arg2 = world.test + "-2.0.tar.gz"  # TODO Need to deal with version numbers
				subprocess.check_call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)
			except:
				print "Error: unable to untar the archive file\n"
				raise
			#		try:
			#			command = "cp"
			#			arg1 = "%s/namelist.input"%world.test
			#			arg2 = "%s/namelist.input.default"%world.test
			#			subprocess.check_call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)
			#		except:
			#			print "Error: unable to backup namelist\n"
			#			raise

			# go into the test directory
			os.chdir(world.basedir + "/" + testtype + "_tests/" + world.test)

			# link executable
			os.symlink(world.basedir+'/' + testtype + '/landice_model', 'landice_model_'+testtype)

			#	# copy default namelist to standard namelist
			#	command = "cp"
			#	arg1 = "namelist.input.default"
			#	arg2 = "namelist.input"
			#	subprocess.call([command, arg1, arg2], stdout=dev_null, stderr=dev_null)

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



