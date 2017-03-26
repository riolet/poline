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
    printf ("pol [options] one-liner\n");
    printf ("Options\n");
    printf ("-F separator \t\t: Field Separator \n");
}

int main(int argc, char *argv[])
{
    unsigned int i;
    char opt;

    char *args, *python_source;


    char *field_separator=NULL;
    size_t optarg_len;

    while ((opt = getopt (argc, argv, "hF:")) != -1) {
        switch (opt) {
          case 'h':
            usage();
            exit(0);
            break;
          case 'F':
            optarg_len = strlen(optarg);
            if (optarg_len<1) {
                fprintf(stderr,"Field separator must not be empty\n");
                exit(1);
            }
            field_separator = (char *) malloc(optarg_len+3);
            snprintf(field_separator, optarg_len + 3, "'%s'", optarg);
            break;
          default:
            usage();
            exit(1);
         }
     }

    if (argv[optind] == NULL) {
      usage();
      if (field_separator)
           free(field_separator);
      exit(1);
    }

    char * header = "from __future__ import print_function\n"
             "import sys\n"
             "sortedbycount = lambda l, reverse=False: sorted([{'e':e, 'c':l.count(e)} for e in sorted(set(l))], key=lambda k: k['c'], reverse=reverse)\n";


    size_t header_len = strlen(header);

    char * split_line_format = "_=[line.strip().split(%s) for line in sys.stdin.readlines()]\n";
    char * split_line;

    size_t split_line_len;

    if (field_separator) {
        split_line_len = strlen(split_line_format) + strlen(field_separator);
        split_line = (char *)malloc(split_line_len + 1);
        snprintf(split_line, split_line_len + 1, split_line_format, field_separator);
    } else {
        split_line_len = strlen(split_line_format);
        split_line = (char *)malloc(split_line_len + 1);
        snprintf(split_line, split_line_len + 1, split_line_format, "");
    }


    size_t len = header_len + split_line_len + argc-1;

    for(i = optind; i<argc; i++) {
        len += strlen(argv[i]);
    }

    args = python_source = (char *)malloc(len +argc-1);

    memcpy(args, header, header_len);
    args += header_len;

    memcpy(args, split_line, strlen(split_line));
    args += strlen(split_line);

    for(i = optind; i<argc; i++) {
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
    free(split_line);
    if (field_separator)
        free(field_separator);
    return 0;
}