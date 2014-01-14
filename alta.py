# ­*­ coding: utf­8 ­*­

import os
import sys

user_name = sys.argv[1]

domain_name = sys.argv[2]


linea1 = '\nzone ' +'"' +  domain_name +'"'  +'{\ntype master;\nfile "db.'+ domain_name +'"' +' ;\n}; '
linea2 = '\nzone "45.168.192.in-addr-arpa" {\ntype master;\nfile "db.45.168.192";\n};\n'
fichero = open("/etc/bind/named.conf.local","a")
fichero.write(linea1) 
fichero.write(linea2)
fichero.close 



