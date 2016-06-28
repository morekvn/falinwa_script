import openerplib  # sudo pip install openerp-client-lib
import datetime
import base64
from os import listdir
from os.path import isfile, join
import sys

#Folder where image are stored, can be absolute path
FOLDER = "/home/falinwa/folder_picture_to_import/"
#In this example the matching is done with the default_code but could be any field that is a unique key on product.product
MATCH_FIELD = 'name'


#need openerp-client-lib installed, initialized the connection, pass the uid to avoid useless login call
connection = openerplib.get_connection(hostname="xxx.xxx.xxx.xxx",  # Change hostname address
                                               port=8069,  # Change to the port that used by Odoo
                                               database="DATABASE_NAME",  # Change database name
                                               login="admin",
                                               password="ADMIN_PASSWORD",  # Change to admin's password
                                               protocol="jsonrpc",
                                               user_id=1)

#get model proxy
emp = connection.get_model('hr.employee')

#Get all the file in the folder and product reference
onlyfiles = [ f for f in listdir(FOLDER) if isfile(join(FOLDER,f)) ]
refs = [f.split('.')[0] for f in onlyfiles]


#Read all information needed on product, performing this outside the loop for performance reason O(1) query instead of O(n) query
emp_info = emp.search_read([(MATCH_FIELD, 'in', refs)], [MATCH_FIELD])

#generate a mapping between default_code and id to get the id info when we needed in the loop, same for filename and reference
emp_per_ref = { r[MATCH_FIELD] : r['id'] for r in emp_info }
filename_per_ref = dict(zip(refs, onlyfiles))

for reference in refs:
    #Don't do anything if there is no product with this reference
    if not emp_per_ref.get(reference):
        #Send error tout stderr instead of stdout
        print >> sys.stderr, "Missing employee", reference
        continue

    #Read the file of the current reference and encode it in base64 string
    with open(FOLDER + filename_per_ref[reference], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_file.close()

    #Values to create line
    image_data = {
        'image' : encoded_string,
    }

    emp.write([emp_per_ref[reference]], image_data)
    print "Imported", reference
