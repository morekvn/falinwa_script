import openerplib  #sudo pip install openerp-client-lib
import datetime
import base64
from os import listdir
from os.path import isfile, join
import sys

#Folder where image are stored, can be absolute path
FOLDER = "./VBLL1/80/"
#In this example the matching is done with the default_code but could be any field that is a unique key on product.product
MATCH_FIELD = 'name'


#need openerp-client-lib installed, initialized the connection, pass the uid to avoid useless login call
connection = openerplib.get_connection(hostname="120.24.220.138",
                                               port=8069,
                                               database="HPS",
                                               login="admin",
                                               password="clean12admin",
                                               protocol="jsonrpc",
                                               user_id=1)

#get model proxy
product_model = connection.get_model('product.product')
version_model = connection.get_model('fal.product.version')
line_model = connection.get_model('fal.information.line')


#Get all the file in the folder and product reference
onlyfiles = [ f for f in listdir(FOLDER) if isfile(join(FOLDER,f)) ]
refs = [f.split('.')[0] for f in onlyfiles]


#Read all information needed on product, performing this outside the loop for performance reason O(1) query instead of O(n) query
product_info = product_model.search_read([(MATCH_FIELD, 'in', refs)], [MATCH_FIELD])

#generate a mapping between default_code and id to get the id info when we needed in the loop, same for filename and reference
product_id_per_ref = { r[MATCH_FIELD] : r['id'] for r in product_info }
filename_per_ref = dict(zip(refs, onlyfiles))



for reference in refs:
    #Don't do anything if there is no product with this reference
    if not product_id_per_ref.get(reference):
        #Send error tout stderr instead of stdout
        print >> sys.stderr, "Missing product", reference
        continue 

    #Read the file of the current reference and encode it in base64 string
    with open(FOLDER + filename_per_ref[reference], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_file.close()

    #Values to create line
    version_line_value = {
        'name' : reference, #put the line name you want
        'date' :  datetime.date.today().strftime("%Y-%m-%d"),
        'type' : 'drawing', 
        'datas' : encoded_string,
        'datas_fname' : filename_per_ref[reference],
        'filename' : filename_per_ref[reference], #Seems duplicate with datas_fname
    }
    line_id = line_model.create(version_line_value) #Keep the id of the created line we'll need it

    version_values = {
        #'version_name' : 'V1', #put the version name you want
        'fal_information_line_ids' : [(6,0,[line_id])], #use of many2many command to create directly the line
        #'fal_product_version_id' : product_id_per_ref[reference], #Link with the product with the given reference

    }
    #version_model.create(version_values)
    product_model.write([product_id_per_ref[reference]],{
        'fal_product_version_ids': [(0, 0,version_values)]
    })
    print "Imported", reference

#General remarks on fal_plm.py 
"""
  fal_information_line_ids should be a one2many based on fal_information_line_id instead of a Many2Many
  two time the field "Filename" : filename and data_fname
"""
