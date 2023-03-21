import sys
import os


def printHelp():
    print("usage: python3 [option] ... [-c cmd | -m mod | file | -] [arg] ...\n"
          "Options and arguments (and corresponding environment variables):")
    print("-get asst-<#>  : issues a wget on the CS730 web page for the specified Assignment\n"
          "\t     use asst-# where \'#\' is the number assignment you want")
    print("-make\t  : issue a make command to create both a make.sh and a run.sh file")
    print("-test\t  : issue a test command based on found tar files from pulled -get cmd")
    print("-submit\t  : issue a submit command to the CS730 repository on agate")
    exit(0)


if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    if '-help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
        printHelp()