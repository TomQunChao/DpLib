gcc -fPIC -shared mt19937-64.c RandGen.c -o librandgen.so
gcc -fPIC -shared -lrandgen -L./ cal.c -o libcal.so