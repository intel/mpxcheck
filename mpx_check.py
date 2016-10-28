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

"""Use this module to execute the MpxCheck framework"""

import argparse
import shlex
import sys
from MpxCheck import MpxCheck

def main():
    """This is the main entry point"""
    parser = argparse.ArgumentParser( \
             prog="mpx_check.py",
             description="Detect MPX #BR messages while running a workload",
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--cmd", metavar="'cmd'", type=str,
                        help="command to execute the workload")
    parser.add_argument("-l", "--log", metavar="path", type=str,
                        default="results.csv",
                        help="path to output csv results log")
    parser.add_argument("-r", "--rlog", metavar="path", type=str,
                        default="results.csv",
                        help="path to read an existing csv results log")
    parser.add_argument("-s", "--stop", metavar="n", type=int,
                        default=0,
                        help="stop after reaching this #BR count")
    parser.add_argument("-V",
                        action="store_true",
                        help="enable verbose mode to show everything")
    args = parser.parse_args()
    ret = 1
    mpx = None
    if args.cmd:
        cmd = shlex.split(args.cmd)
        mpx = MpxCheck(cmd=cmd, stop_cnt=args.stop,
                       verbose=args.V, log=args.log)
        ret = mpx.run()
    elif args.rlog:
        mpx = MpxCheck(cmd=None)
        ret = mpx.read(args.rlog)
    if ret > -1:
        mpx.show_summary()
    return ret

if __name__ == "__main__":
    sys.exit(main())
