# Automated Runtime Buffer Overflow Checker Using Intel® Memory Protection Extensions (MPX) MpxCheck


## Introduction
Intel® Memory Protection Extensions (MPX) is a set of processor features which, with compiler, runtime library and OS support, brings increased robustness to software by checking pointer references whose compile time normal intentions are usurped at runtime due to buffer overflow. 

MpxCheck is an automated Python framework that uses Intel ® MPX technology to monitor for buffer overflows while you run your application.

## Background
Let's say that you want to check whether your application is susceptible to buffer overflows. You have already done due diligence by running static code analysis tools against the source and fixed those issues. Now you want to test your application to verify that everything works. You build your source using the MPX compiler switches supported in GCC. You provide the command line to execute your tests to the *mpxcheck.py* script or the *MpxCheck.py* module. While executing your tests MpxCheck detects bound range (#BR) exception messages, if any, and records them in a timestamped log. If no such messages are found, MpxCheck returns 0 otherwise the #BR count. This makes MpxCheck an ideal tool for integration into an automated, continuous build and test environment where buffer overflows can be detected earlier than later. Even if you decide not to enable MPX support in your final product, it can still be used as a valuable security tool to find runtime vulnerabilities where other mechanisms have failed.

## Prerequisites
You will need these components in place before you can use Intel® MPX and MpxCheck:

 - Linux kernel >= 3.19 required, 4.1 recommended with CONFIG_X86_INTEL_MPX enabled in build
 - binutils >= 2.24 required (objdump, ld, etc.)
 - gcc: >= 5.0 required, >= 5.2 recommended
 - gdb >= 7.9 required, >= 7.10 recommended
 - glibc >= 2.20 required
 - 6th Generation Intel® Core™ processor or newer supported processors
 - Python >= 3.0

## Installation
  - Clone or download the latest source from [01.org](https://01.org/projects)
  - Run *python ./Test.py* to ensure that your environment supports MPX. All tests shoud pass.
  - Compile your source using gcc with the MPX flags that you want to use. For example:
  	- *gcc -Wall -mmpx -fcheck-pointer-bounds -static myapp.c* -o myapp
  	- See all compiler flag options in the [Intel MPX Enabling Guide](https://software.intel.com/en-us/articles/intel-memory-protection-extensions-enabling-guide)

## Execution

You can execute your workload by using the *mpxcheck.py* script, *MpxCheck.py* module or as a simple Bash script:

### As a Python Script
Invoke the *mpxcheck.py* script
```
./mpxcheck.py -c './myapp arg1 arg2'
 if [ $? -ne 0 ]; then
	echo '#BR exception messages were found'
 fi
```
Other options include the following:
```
Usage: python ./mpxcheck.py [-h] [-c 'cmd'] [-l path] [-r path] [-s n] [-V]

	-h, --help               show this help message
    -c 'cmd', --cmd 'cmd'    command to execute the workload
    -l path, --log path      path to output csv results log (default: results.csv)
    -r path, --rlog path     path to read an existing csv results log (default: results.csv)
    -s n, -- stop n          stop after reaching this #BR count (default: 0 (don't stop until done))
    -V                       enable verbose mode to show everything (default: False)

```

See *ex_using_python.sh* for more *mpxcheck.py* script examples

### As a Python Module
Import the *MpxCheck* module into your own python script
```
import MpxCheck import MpxCheck
mpx = MpxCheck(['./myapp', 'arg1', 'arg2'])
ret = mpx.run()
mpx.show_summary()
if ret > 0:
	print('#BR exception messages were found')
```

See the *Test.py* for more *MpxCheck.py* module examples

### As a Bash Script
Run your workload in a Bash shell using MPX environment variables only
```
#!/bin/bash
export CHKP_RT_PRINT_SUMMARY=yes
export CHKP_RT_OUT_FILE=stdout.log
export CHKP_RT_ERR_FILE=stderr.log
./myapp arg1 arg2
```

See *ex_using_shell.sh* for more Bash examples

## Results

Results are stored in a comma delimited file when using the *mpxcheck.py* script or *MpxCheck.py* module. The default file name is *results.csv*, but you can change it with the *-l path* option. Here is an example of a *mpxcheck.py* run using one of the provided test files:
```
python ./mpcheck.py -c './test/test01 10'
[MPX][2016-10-04|13:56:49]: Elapsed: 0, Count: 1
[MPX][2016-10-04|13:56:49]: Elapsed: 0, Count: 2
[MPX][2016-10-04|13:56:49]: Elapsed: 0, Count: 3
[MPX][2016-10-04|13:56:49]: Elapsed: 0, Count: 4
[MPX][2016-10-04|13:56:49]: Elapsed: 0, Count: 5
[MPX][2016-10-04|13:56:49]: Elapsed: 0, Count: 6

MPX #BR Summary
  Count:   6
  Elapsed: 0s
  Begin:   2016-10-04|13:56:49
  End:     2016-10-04|13:56:49
  Log:     results.csv

cat ./results.csv

datetime,elapsed,count,status,address,epoch
2016-10-04|13:56:49,0,1,1,0x401379,1475613219
2016-10-04|13:56:49,0,2,1,0x401379,1475613219
2016-10-04|13:56:49,0,3,1,0x401379,1475613219
2016-10-04|13:56:49,0,4,1,0x401379,1475613219
2016-10-04|13:56:49,0,5,1,0x401379,1475613219
2016-10-04|13:56:49,0,6,1,0x401379,1475613219
```

|Name         |     |Description |
|:------------|-----|:-----------|
|**datetime** |     |*Human friendly timestamp of when #BR exception message was detected*|
|**elapsed**  |     |*Number of seconds since the start of execution*|
|**count**    |     |*Incremental count of #BR messages*|
|**status**   |     |*#BR exception message status flag*|
|**address**  |     |*Address location of the #BR exception*|
|**epoch**    |     |*Same as datetime but as epoch seconds*|


You can also read an existing csv results log without executing a workload:
```
python ./mpcheck.py -r ./results.csv

MPX #BR Summary
  Count:   6
  Elapsed: 0s
  Begin:   2016-10-04|13:56:49
  End:     2016-10-04|13:56:49
  Log:     results.csv
```

If you decide to run your workload in just a Bash shell instead of the MpxCheck framework you can still retrieve useful statistics at the end of each run:

```
#!/bin/bash
export CHKP_RT_PRINT_SUMMARY=yes
./test/test01 10

... output ...

MPX runtime summary:
   Number of bounds violations: 6.
   Size of allocated L1: 2147483648B
```

## License
BSD 3-clause license ("Revised BSD License", "New BSD License", or "Modified BSD License")


### References

 - [Intel® Memory Protection Extensions Enabling Guide](https://software.intel.com/en-us/articles/intel-memory-protection-extensions-enabling-guide)
 - [Intel® Architecture Instruction SAet Extensions Programming Reference](https://software.intel.com/sites/default/files/managed/07/b7/319433-023.pdf)
 - [Intel® Memory Protection Extensions (Intel® MPX) for Linux*](https://01.org/blogs/2016/intel-mpx-linux)
 - [Intel® Memory Protection Extensions (Intel® MPX) support in the GCC compiler](https://gcc.gnu.org/wiki/Intel%20MPX%20support%20in%20the%20GCC%20compiler)
