/*
* Author: Rohana Rezel
*
* MIT License
* Copyright (c) 2017 Riolet Corporation
*
* Acknowledgements
* Argument concatenation
* http://stackoverflow.com/questions/3126882/concatenate-all-arguments-except-the-executable-name
*/
#include <Python.h>

int
main(int argc, char *argv[])
{
    unsigned int i;

    char *args, *python_source;

    char * header = "from __future__ import print_function\n"
             "import sys\n"
             "_=[line.strip().split() for line in sys.stdin.readlines()]\n";

    size_t len = strlen(header);

    for(i=1; i<argc; i++) {
        len += strlen(argv[i]);
    }

    args = python_source = (char *)malloc(len+argc-1);

    memcpy(args, header, strlen(header));
    args += strlen(header);

    for(i=1; i<argc; i++) {
        memcpy(args, argv[i], strlen(argv[i]));
        args += strlen(argv[i])+1;
        *(args-1) = ' ';
    }

    *(args-1) = 0;

    Py_SetProgramName(argv[0]);  /* optional but recommended */
    Py_Initialize();

    PyRun_SimpleString(python_source);

    Py_Finalize();
    free(python_source);
    return 0;
}