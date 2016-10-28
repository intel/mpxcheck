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

"""This is the Utl module

This module a collection of tools to support commonly used functions
"""
import os
import subprocess

class Utl(object):
    """A collection of static utility methods"""

    @staticmethod
    def exe(cmd):
        """Execute a command
        Args:
            cmd (list): command to execute as a list (e.g.)['ls','-al']
        Returns:
            a dictionary containing the following keys:
            output: output of the executed command, includes stderr
            exit: exit status of executed command
            valid: if exit status was 0 and output exists
            error: error from an exception if occurs
        """
        try:
            proc = subprocess.Popen(
                cmd, shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.communicate()[0].decode(encoding="iso8859_1")
            valid = not Utl.is_none(output) and proc.returncode == 0
            proc.stdout.close()
            proc.stderr.close()
            return {"output":output, "exit":proc.returncode,
                    "valid":valid, "error":None}
        except (ValueError, OSError) as ex:
            return {"output":str(ex), "exit":-1,
                    "error":str(ex), "valid":False}

    @staticmethod
    def is_none(token):
        """Check if string object is None or empty
        Args:
            token (str): string object
        Returns:
            True if empty, False otherwise
        """
        return token is None or str(token).strip() == ''

    @staticmethod
    def remove(path):
        """Delete file if exists
        Args:
            path (str): path to file
        Returns:
            None
        """
        if os.path.isfile(path):
            os.unlink(path)
