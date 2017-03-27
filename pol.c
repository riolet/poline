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


size_t escape_chars (char *dst, const char *src, size_t size)
{
    char escapees[] = {'\\','\''};
    size_t dstlen = strlen(dst);

    while(*src) {
        int i;
        for (i=0;i<sizeof(escapees);i++) {
            if (*src == escapees[i]) {
                *dst = '\\';
                if (dstlen >= size-1) {
                    *dst = 0;
                    return dstlen;
                }
                dstlen++;
                dst ++;

                *dst = escapees[i];
                if (dstlen>=size-1) {
                    *dst = 0;
                    return dstlen;
                }
                dstlen++;
                dst ++;
                src ++;

            }
        }
         if (i==sizeof(escapees)) {
            *dst = *src;
            if (dstlen >= size-1) {
                dst = 0;
                return dstlen;
            }
            dstlen++;
            dst ++;
            src ++;
        }
    }
    *dst = *src;
    return dstlen;
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
            char * escaped_optarg = (char *) malloc(optarg_len*2+1);
            size_t escaped_optarg_len = escape_chars(escaped_optarg, optarg, optarg_len*2+1);
            field_separator = (char *) malloc(escaped_optarg_len+3);
            snprintf(field_separator, escaped_optarg_len + 3, "'%s'", escaped_optarg);
            free(escaped_optarg);
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

    char * header =
             "from __future__ import print_function\n"
             "import sys\n"
             "import os\n"
             "sortedbycount = lambda l, reverse=False: sorted([{'e':e, 'c':l.count(e)} for e in sorted(set(l))], key=lambda k: k['c'], reverse=reverse)\n"
             "sh = lambda c, F = None: [line.strip().split(F) for line in os.popen(c).readlines()]\n"
             "get = lambda l, i, d = None: l[i] if len(l)>i else d\n"
             "def bytesize(x):\n"
             "    units = ['P', 'T', 'G', 'M', 'K', 'B']\n"
             "    for i in range(len(units)):\n"
             "        if x == 0:\n"
             "            return '{:6.2f} {}'.format(0,units[-1])\n"
             "        if x/1024 ** (len(units) - i - 1) > 0:\n"
             "            return '{:6.2f} {}'.format(x/float(1024 ** (len(units) - i - 1)), units[i])\n";


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