# SecList Password combiner
A python script to combine the passwords in the [@danielmiessler Seclists](https://github.com/danielmiessler/SecLists).
The passwords are unique and sorted

Usage: `python combiner.py -d [directory with the password files] -o [output file]`

The CSV files and the files with passwords frequencies are not processed!

For me, the output contains around 52 millions passwords (~750 MB).

Personally, I removed the first ~15 lines of the outputed file as they had special characters and spaces.