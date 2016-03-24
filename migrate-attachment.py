#!/usr/bin/env python
import xmlrpclib

username = '' #adminuser
pwd = '' #passs
dbname = '' #dbname

sock_common = xmlrpclib.ServerProxy ('http://192.168.0.2:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://192.168.0.2:8069/xmlrpc/object')

def migrate_attachment(att_id):
    att = sock.execute(dbname, uid, pwd, 'ir.attachment', 'read', att_id, ['datas'])
    data = att[0]['datas']

    a = sock.execute(dbname, uid, pwd, 'ir.attachment', 'write', [att_id], {'datas': data})

att_ids = sock.execute(dbname, uid, pwd, 'ir.attachment', 'search', [('store_fname','=',False)])

cnt = len(att_ids)
i = 0
for id in att_ids:
    migrate_attachment(id)
    print 'Migrated ID %d (attachment %d of %d)' % (id,i,cnt)
    i = i + 1

print 'done'
