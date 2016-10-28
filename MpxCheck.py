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

"""The MpxCheck framework module"""
import csv
import re
import subprocess
import sys
import time

class MpxCheck(object):
    """The primary MpxCheck framework class

    Attributes:
        cmd (list): command to execute
        stop_cnt (int): stop execution if MPX #BR events reach this count
        verbose (bool): set to True to see all output
        log (str): path to csv results log
        sts (dict): various statistics generated during runtime
    """
    def __init__(self, cmd, stop_cnt=0, verbose=False, log="results.csv"):
        """Class constructor
        Args:
            cmd (list): command to execute as a list (e.g.)['ls','-al']
            stop_cnt (int): stop execution if MPX #BR events reach this count
            verbose (bool): set to True to see all output
            log (str): path to csv results log
        Returns:
            None
        """
        self.cmd = cmd
        self.stop_cnt = abs(int(stop_cnt))
        self.verbose = verbose
        self.log = log.strip()
        self.sts = None

    @staticmethod
    def __get_dt(epoch):
        """Formats human-friendly string based on epoch seconds
        Args:
            epoch (int): epoch seconds
        Returns:
            a formatted datatime string
        """
        return time.strftime('%Y-%m-%d|%H:%M:%S', time.localtime(epoch))

    def __init_sts(self):
        """Helper method to initialize statistics"""
        self.sts = {"cnt":0, "begin":0, "end":0, "elapsed":0, "dt":""}

    def run(self):
        """Execute the workload
        Args:
            None
        Returns:
            -1 if exception, 0 if no #BR msgs, 0>#BR msg count
        """
        self.__init_sts()
        regex = re.compile("Saw a #BR!")
        fields = ["datetime", "elapsed", "count",
                  "status", "address", "epoch"]
        try:
            with open(self.log, "w") as csv_log:
                csv_writer = csv.writer(csv_log, delimiter=",")
                csv_writer.writerow(fields)
                self.__update_dt(True)
                proc = subprocess.Popen(
                    self.cmd, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=False, universal_newlines=False)
                lines = iter(proc.stdout.readline, "")
                for line in lines:
                    if line == b'':
                        break
                    try:
                        lined = line.decode("utf-8")
                        if self.verbose:
                            sys.stdout.write(lined)
                        if regex.search(lined):
                            self.sts["cnt"] += 1
                            self.__write_log(csv_writer, lined)
                        if self.stop_cnt and self.sts["cnt"] >= self.stop_cnt:
                            print("[MPX]: Reached stop count: %s"
                                  %(self.stop_cnt))
                            break
                    except UnicodeDecodeError:
                        continue
                proc.wait()
                proc.stdout.close()
        except (ValueError, OSError, IOError) as ex:
            sys.stderr.write("[MPX]: Exception: %s\n" %(str(ex)))
            return -1
        return self.sts["cnt"]

    def read(self, log):
        """Reads an existing csv results log
        Args:
            log (str): path to the existing csv results log
        Returns:
            -1 if exception, 0 if no #BR msgs, 0>#BR msg count
        """
        self.log = log.strip()
        self.__init_sts()
        try:
            with open(self.log, "r") as csv_log:
                csv_reader = csv.reader(csv_log, delimiter=",")
                next(csv_reader, None)
                rows = list(csv_reader)
                cnt = len(rows)
                self.sts["cnt"] = cnt
                if cnt > 0:
                    self.sts["begin"] = int(rows[0][5])
                    self.sts["end"] = int(rows[cnt-1][5])
                    self.sts["elapsed"] = int(rows[cnt-1][1])
                    self.sts["dt"] = self.__get_dt(self.sts["end"])
                else:
                    self.sts["begin"] = 0
                    self.sts["end"] = 0
                    self.sts["elapsed"] = 0
                    self.sts["dt"] = ''
        except IOError as ex:
            sys.stderr.write("[MPX]: Exception: %s\n" %(str(ex)))
            return -1
        return self.sts["cnt"]

    def show_summary(self):
        """Displays a summary of results
        Args:
            None
        Returns:
            None
        """
        print("""
MPX #BR Summary
 Count:   %s
 Elapsed: %ss
 Begin:   %s
 End:     %s
 Log:     %s
""" %(self.sts["cnt"], self.sts["elapsed"],
      self.__get_dt(self.sts["begin"]),
      self.__get_dt(self.sts["end"]), self.log))

    def __update_dt(self, begin=True):
        """Helper method to update datetime stats"""
        epoch = int(time.time())
        if begin:
            self.sts["begin"] = epoch
        self.sts["end"] = epoch
        self.sts["elapsed"] = epoch - self.sts["begin"]
        self.sts["dt"] = self.__get_dt(epoch)

    def __write_log(self, csv_writer, br_msg):
        """Helper method to write to the log"""
        self.__update_dt(False)
        tokens = br_msg.split()
        if len(tokens) < 7:
            print("Warning: Invalid MPX BR message: %s", br_msg)
            return
        entry = [self.sts["dt"], self.sts["elapsed"], self.sts["cnt"],
                 tokens[4], tokens[6], self.sts["end"]]
        csv_writer.writerow(entry)
        print("[MPX][%s]: Elapsed: %s, Count: %s"
              %(self.sts["dt"], self.sts["elapsed"], self.sts["cnt"]))

