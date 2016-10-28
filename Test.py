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

"""This is the MpxCheck test module"""
import os
import unittest
from Env import Env
from MpxCheck import MpxCheck
from Utl import Utl

class Test(unittest.TestCase):
    """This is the MpxCheck test class"""

    def test_can_build(self):
        """Verify that test source can build with MPX flags
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        os.chdir("./test")
        result = Utl.exe(["make", "clean"])
        result = Utl.exe(["make"])
        file_exists = os.path.isfile("test01")
        os.chdir("../")
        self.assertTrue(
            result["valid"] and
            file_exists,
            "Test suite build failed")

    def test_has_binutils(self):
        """Verify that binutils of supported version exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking binutils")
        self.assertTrue(
            Env.has_binutils(),
            "binutils is not supported")

    def test_has_cpu_family(self):
        """Verify that cpu family of supported type exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking cpu family")
        self.assertTrue(
            Env.has_cpu_family(),
            "cpu family not supported")

    def test_has_cpu_vendor_id(self):
        """Verify that cpu vendor id of supported type exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking cpu vendor id")
        self.assertTrue(
            Env.has_cpu_vendor_id(),
            "cpu vendor id not supported")

    def test_has_gcc(self):
        """Verify that gcc of supported version exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking gcc")
        self.assertTrue(
            Env.has_gcc(),
            "gcc not supported")

    def test_has_gdb(self):
        """Verify that gdb of supported version exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking gdb")
        self.assertTrue(
            Env.has_gdb(),
            "gdb not supported")

    def test_has_glibc(self):
        """Verify that glibc of supported version exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking glibc")
        self.assertTrue(
            Env.has_glibc(),
            "glibc not supported")

    def test_has_kernel(self):
        """Verify that kernel of supported version exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking kernel")
        self.assertTrue(
            Env.has_kernel(),
            "kernel not supported")

    def test_has_mpx_instr(self):
        """Verify that MPX instructions exist in binary image
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking instr")
        self.assertTrue(
            Env.has_mpx_instr("./test/test01"),
            "missing mpx instructions in ./test/test01")

    def test_has_mpx(self):
        """Verify that that MPX is fully hw/sw supported
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking mpx")
        self.assertTrue(
            Env.has_mpx_cpu(),
            "mpx not supported in cpu")
        self.assertTrue(
            Env.has_mpx_kernel(),
            "mpx not supported in kernel")
        self.assertTrue(
            Env.has_mpx(),
            "mpx not supported")

    def test_has_objdump(self):
        """Verify that objdump with supported version exists
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking objdump")
        self.assertTrue(
            Env.has_objdump(),
            "objdump not supported")

    def test_test01a(self):
        """Verify that test01 works correctly
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking test01")
        path = "./test/test01"
        log = "./test01a.csv"
        Utl.remove(log)
        cmd = [path, "10"]
        mpx = MpxCheck(cmd=cmd, log=log)
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(6 == mpx.run())
        self.assertTrue(os.path.isfile(log))
        self.assertTrue(6 == mpx.sts["cnt"])
        self.assertTrue(0 != mpx.sts["begin"])
        self.assertTrue(0 != mpx.sts["end"])
        self.assertTrue(3 > mpx.sts["elapsed"])
        self.assertTrue(not Utl.is_none(mpx.sts["dt"]))
        Utl.remove(log)

    def test_test01b(self):
        """Verify that test01 log reading works correctly
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking test01 log parsing")
        path = "./test/test01"
        log = "./test01b.csv"
        Utl.remove(log)
        cmd = [path, "10"]
        mpx = MpxCheck(cmd=cmd, log=log)
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(6 == mpx.run())
        self.assertTrue(os.path.isfile(log))
        mpx = MpxCheck(cmd=None)
        self.assertTrue(6 == mpx.read(log))
        self.assertTrue(6 == mpx.sts["cnt"])
        self.assertTrue(0 != mpx.sts["begin"])
        self.assertTrue(0 != mpx.sts["end"])
        self.assertTrue(3 > mpx.sts["elapsed"])
        self.assertTrue(not Utl.is_none(mpx.sts["dt"]))
        Utl.remove(log)

    def test_test01c(self):
        """Verify that stop count option works
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking test01")
        path = "./test/test01"
        log = "./test01c.csv"
        Utl.remove(log)
        cmd = [path, "100"]
        mpx = MpxCheck(cmd=cmd, log=log, stop_cnt=1)
        self.assertTrue(os.path.isfile(path))
        ret = mpx.run()
        self.assertTrue(1 == ret)
        self.assertTrue(os.path.isfile(log))
        self.assertTrue(1 == mpx.sts["cnt"])
        self.assertTrue(0 != mpx.sts["begin"])
        self.assertTrue(0 != mpx.sts["end"])
        self.assertTrue(3 > mpx.sts["elapsed"])
        self.assertTrue(not Utl.is_none(mpx.sts["dt"]))
        Utl.remove(log)

    def test_test03(self):
        """Verify that test03 doesn't generate false positives
        Args:
            None
        Returns:
            Pass if successful, Fail otherwise
        """
        print("Checking test03")
        path = "./test/test03"
        log = "./test03.csv"
        Utl.remove(log)
        cmd = [path]
        mpx = MpxCheck(cmd=cmd, log=log)
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(0 == mpx.run())
        self.assertTrue(os.path.isfile(log))
        self.assertTrue(0 == mpx.sts["cnt"])
        self.assertTrue(0 != mpx.sts["begin"])
        self.assertTrue(0 != mpx.sts["end"])
        self.assertTrue(3 > mpx.sts["elapsed"])
        self.assertTrue(not Utl.is_none(mpx.sts["dt"]))
        mpx = MpxCheck(cmd=None)
        self.assertTrue(0 == mpx.read(log))
        self.assertTrue(0 == mpx.sts["cnt"])
        self.assertTrue(0 == mpx.sts["begin"])
        self.assertTrue(0 == mpx.sts["end"])
        self.assertTrue(0 == mpx.sts["elapsed"])
        self.assertTrue(Utl.is_none(mpx.sts["dt"]))
        Utl.remove(log)

if __name__ == '__main__':
    unittest.main()
