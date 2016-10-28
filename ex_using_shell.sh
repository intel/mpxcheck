#!/bin/bash

# Copyright (c) 2016, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# If you want to monitor MPX #BR messages without MpxCheck tool,
# you can still execute your workload as normal but with these MPX
# environment variables set accordingly.

# Generate an output and error file for each process [default:no]
# The format will be CHKP_RT_{OUT,ERR}_FILE.pid
#CHKP_RT_ADDPID=no

# Set value for the BNDPRESERVE bit [default:0]
# 0: Flush bounds on unprefixed call/ret/jmp
# 1: Do not flush founds
#CHKP_RT_BNDPRESERVE=0

# Set output file for error messages [default:stderr]
#CHKP_RT_ERR_FILE=stderr.log

# Print help message and exit [default:0]
#CHKP_RT_HELP=0

# Set output file for info and debug messages [default:stdout]
#CHKP_RT_OUT_FILE=stdout.log

# Print summary at the end of a run [default:yes]
#CHKP_RT_PRINT_SUMMARY=no

# Set verbose level  [default:2]
#  0 - Print only internal run time errors
#  1 - Print summary
#  2 - Print summary and bound violation information
#  3 - Print debug information
#CHKP_RT_VERBOSE=2

# Set MPX runtime behavior on bound range (#BR) exception [default:stop]
# stop
# count
#CHKP_RT_MODE=stop

rm -f *.log.*

# Show help. Help gets displayed at the end of execution
export CHKP_RT_HELP=yes
./test/test01 10
export CHKP_RT_HELP=no

# Run workload and print summary
export CHKP_RT_PRINT_SUMMARY=yes
./test/test01 10

# Run workload and set out/error log paths and print summary to out log
export CHKP_RT_ERR_FILE=stderr.log
export CHKP_RT_OUT_FILE=stdout.log
./test/test01 10

# Run workload and set out/error log paths for each process id
export CHKP_RT_ADDPID=yes
./test/test01 10
./test/test01 10

# Run workload that should not generate any errors
./test/test03

# Set MPX runtime behavior on bound range stop
unset CHKP_RT_ERR_FILE
unset CHKP_RT_OUT_FILE
export CHKP_RT_PRINT_SUMMARY=no
export CHKP_RT_MODE=stop
./test/test01 10

# Flush bounds
export CHKP_RT_PRINT_SUMMARY=yes
export CHKP_RT_MODE=count
export CHKP_RT_BNDPRESERVE=1
./test/test01 10

# Preserve bounds
export CHKP_RT_BNDPRESERVE=0
./test/test01 10

