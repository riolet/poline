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
#include <unistd.h>
#include <stdio.h>
#include <Python.h>

void usage(void)
{
    printf ("pol [options] string\n");
}

int main(int argc, char *argv[])
{
    unsigned int i;
    char opt;

    char *args, *python_source;

    char * header = "from __future__ import print_function\n"
             "import sys\n"
             "sortedbycount = lambda l, reverse=False: sorted([{'e':e, 'c':l.count(e)} for e in sorted(set(l))], key=lambda k: k['c'], reverse=reverse)\n"
             "_=[line.strip().split() for line in sys.stdin.readlines()]\n";

    while ((opt = getopt (argc, argv, "h")) != -1) {
        switch (opt) {
          case 'h':
            usage();
            exit(0);
            break;
          default:
            usage();
            exit(1);
         }
     }

    size_t len = strlen(header);

    if (argv[optind] == NULL || argv[optind + 1] == NULL) {
      usage();
      exit(1);
    }

    for(i=optind; i<argc; i++) {
        len += strlen(argv[i]);
    }

    args = python_source = (char *)malloc(len+argc-1);

    memcpy(args, header, strlen(header));
    args += strlen(header);

    for(i=optind; i<argc; i++) {
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