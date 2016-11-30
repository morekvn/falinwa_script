import openerplib  # sudo pip install openerp-client-lib
import base64
from os import listdir
from os.path import isfile, join
import sys

# Folder where image are stored, can be absolute path
# CHANGE THIS FOLDER RELATED TO FOLDER
FOLDER = "E:\/test_image\/"
# In this example the matching is done with the default_code but could be
# any field that is a unique key on product.product
MATCH_FIELD = 'fal_old_ref'


# need openerp-client-lib installed, initialized the connection, pass the
# uid to avoid useless login call

connection = openerplib.get_connection(hostname="xxx.xxx.xxx.xxx",
                                       port=1234,
                                       database="YOURDATABASENAME",
                                       login="admin",
                                       password="YOURPASSWORD",
                                       protocol="jsonrpc",
                                       user_id=1)

# get model proxy
product_model = connection.get_model('product.template')

# Get all the file in the folder and product reference
onlyfiles = [f for f in listdir(FOLDER) if isfile(join(FOLDER, f))]
refs = [f.split('.')[0] for f in onlyfiles]


# Read all information needed on product, performing this outside the loop
# for performance reason O(1) query instead of O(n) query
product_infos = product_model.search_read(
    [(MATCH_FIELD, 'in', refs)], [MATCH_FIELD])

# generate a mapping between default_code and id to get the id info when
# we needed in the loop, same for filename and reference
product_id_per_ref = {r['id']: r[MATCH_FIELD] for r in product_infos}
filename_per_ref = dict(zip(refs, onlyfiles))


for product_info in product_infos:
    # Don't do anything if there is no product with this reference
    if not product_id_per_ref.get(product_info['id']):
        # Send error tout stderr instead of stdout
        print >> sys.stderr, "#", product_info[MATCH_FIELD]
        continue

    # Read the file of the current reference and encode it in base64 string
    with open(
      FOLDER + filename_per_ref[
          product_info[MATCH_FIELD]], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_file.close()

    # Values to create line
    product_model.write([product_info["id"]], {
        'image': encoded_string
    })

    print "PERFECT", product_info[MATCH_FIELD]
