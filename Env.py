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

"""This is the Env module

This module a collection of tools to determine whether MPX is supported
"""
import platform
import re
from Utl import Utl

class Env(object):
    """This is the Env class"""

    @staticmethod
    def get_binutils_ver():
        """get binutils version
        Args:
            None
        Returns:
            binutils version as string
        """
        result = Utl.exe(["ld", "--version"])
        if not result["valid"]:
            return None
        tokens = result["output"].split()
        if len(tokens) < 7:
            return None
        return tokens[6]

    @staticmethod
    def get_cpuinfo():
        """get cpuinfo
        Args:
            None
        Returns:
            cpuinfo as string
        """
        result = Utl.exe(["cat", "/proc/cpuinfo"])
        if not result["valid"]:
            return None
        return result['output']

    @staticmethod
    def get_cpuinfo_item(name):
        """get value for specific cpuinfo attribute
        Args:
            None
        Returns:
            cpuinfo value as a string
        """
        for output in Env.get_cpuinfo().split("\n"):
            if re.search(name, output):
                tokens = output.split(":")
                if len(tokens) == 2:
                    return tokens[1].strip()
        return None

    @staticmethod
    def get_cpu_family():
        """get cpu family
        Args:
            None
        Returns:
            cpu family as string
        """
        return Env.get_cpuinfo_item("cpu family")

    @staticmethod
    def get_cpu_vendor_id():
        """get cpu vendor id
        Args:
            None
        Returns:
            cpu vendor as string
        """
        return Env.get_cpuinfo_item("vendor_id")

    @staticmethod
    def get_gcc_ver():
        """get gcc version
        Args:
            None
        Returns:
            gcc version as string
        """
        result = Utl.exe(["gcc", "--version"])
        if not result["valid"]:
            return None
        tokens = result["output"].split()
        if len(tokens) < 4:
            return None
        return tokens[3]

    @staticmethod
    def get_gdb_ver():
        """get gdb version
        Args:
            None
        Returns:
            gdb version as string
        """
        result = Utl.exe(["gdb", "--version"])
        if not result["valid"]:
            return None
        tokens = result["output"].split()
        if len(tokens) < 5:
            return None
        return tokens[4]

    @staticmethod
    def get_glibc_ver():
        """get glibc version
        Args:
            None
        Returns:
            glibc version as string
        """
        result = Utl.exe(["ldd", "--version"])
        if not result["valid"]:
            return None
        tokens = result["output"].split()
        if len(tokens) < 5:
            return None
        return tokens[4]

    @staticmethod
    def get_kernel_config():
        """get kernel configuration
        Args:
            None
        Returns:
            kernel configuration as string
        """
        k_ver = Env.get_kernel_ver()
        if k_ver is None:
            return False
        result = Utl.exe(["cat", "/boot/config-%s" %(k_ver)])
        if not result["valid"]:
            return None
        config = {}
        tokens = result["output"].split("\n")
        for token in tokens:
            token = token.strip()
            if re.search("=", token):
                name, value = token.split("=")
                config[name.strip()] = value.strip()
        if len(config) < 1:
            return None
        return config

    @staticmethod
    def get_kernel_ver():
        """get kernel version
        Args:
            None
        Returns:
            kernel version as string
        """
        return platform.release()

    @staticmethod
    def get_objdump_ver():
        """get objdump version
        Args:
            None
        Returns:
            objdump version as string
        """
        result = Utl.exe(["objdump", "--version"])
        if not result["valid"]:
            return None
        tokens = result["output"].split()
        if len(tokens) < 7:
            return None
        return tokens[6]

    @staticmethod
    def has_binutils():
        """check if binutils of supported version exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        ver = Env.get_binutils_ver()
        if ver is None:
            return False
        tokens = [int(i) for i in ver.split(".")[:2]]
        if tokens[0] >= 3:
            return True
        return tokens[0] >= 2 and tokens[1] >= 24

    @staticmethod
    def has_cpu_family():
        """check if supported cpu family exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        try:
            return int(Env.get_cpu_family()) >= 6
        except ValueError:
            return False

    @staticmethod
    def has_cpu_vendor_id():
        """check if supported cpu vendor id exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        vendor_id = Env.get_cpu_vendor_id()
        return vendor_id is not None and vendor_id == "GenuineIntel"

    @staticmethod
    def has_gcc():
        """check if gcc of supported version exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        ver = Env.get_gcc_ver()
        if ver is None:
            return False
        tokens = [int(i) for i in ver.split(".")[:1]]
        if tokens[0] >= 5:
            return True

    @staticmethod
    def has_gdb():
        """check if gdb of supported version exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        ver = Env.get_gdb_ver()
        if ver is None:
            return False
        tokens = [int(i) for i in ver.split(".")[:2]]
        if tokens[0] > 7:
            return True
        return tokens[0] >= 7 and tokens[1] >= 10

    @staticmethod
    def has_glibc():
        """check if glibc of supported version exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        ver = Env.get_glibc_ver()
        if ver is None:
            return False
        tokens = [int(i) for i in ver.split(".")[:2]]
        if tokens[0] > 2:
            return True
        return tokens[0] >= 2 and tokens[1] >= 20

    @staticmethod
    def has_kernel():
        """check if Linux kernel of supported version exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        ver = Env.get_kernel_ver()
        if ver is None:
            return False
        tokens = [int(i) for i in ver.split(".")[:2]]
        if tokens[0] > 4:
            return True
        return tokens[0] >= 4 and Env.has_mpx_kernel()

    @staticmethod
    def has_mpx():
        """check for mpx support in cpu and Linux kernel
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        return Env.has_mpx_cpu() and Env.has_mpx_kernel()

    @staticmethod
    def has_mpx_cpu():
        """check for mpx support in cpu
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        output = Env.get_cpuinfo()
        if output is None:
            return False
        return re.search(" mpx ", output) is not None

    @staticmethod
    def has_mpx_kernel():
        """check if mpx is enabled in kernel
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        k_cfg = Env.get_kernel_config()
        if k_cfg is None:
            return False
        if 'CONFIG_X86_INTEL_MPX' not in k_cfg:
            return False
        return k_cfg['CONFIG_X86_INTEL_MPX'].lower() == 'y'

    @staticmethod
    def has_mpx_instr(path):
        """Check if compiled object contains MPX instructions
        Args:
            path (str): path to binary
        Returns:
            True if successful, False otherwise
        Raises:
            Exception if missing objdump or output is missing
        """
        if not Env.has_objdump():
            raise Exception("[MPX]: Missing/invalid objdump")
        result = Utl.exe(["objdump", "-d", path])
        if not result["valid"]:
            raise Exception("[MPX]: %s" %(result["error"]))
        instr = {"bndmov":False, "bndcl":False, "bndcu":False, "bnd retq":False}
        for output in result["output"].split("\n"):
            for i in instr.keys():
                if re.search(i, output):
                    instr[i] = True
                if False not in set(instr.values()):
                    return True
        return False

    @staticmethod
    def has_objdump():
        """check if objdump of supported version exists
        Args:
            None
        Returns:
            True if yes, False otherwise
        """
        ver = Env.get_objdump_ver()
        if ver is None:
            return False
        tokens = [int(i) for i in ver.split(".")[:2]]
        if tokens[0] > 3:
            return True
        return tokens[0] >= 2 and tokens[1] >= 25
