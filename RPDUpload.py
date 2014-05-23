# ########################################################
#
# Title		: 	RPD自動アップロードツール
# Version	:	Draft0.1A
# Arguments	:	
#		1) 管理サーバホスト名
#		2) 管理サーバポート番号(7001)
#		3) Weblogicユーザ
#		4) Weblogicユーザのパスワード
#		5) RPDファイル名(フルパス)
#		6) RPDパスワード
#
# #########################################################

#import
import sys
import os

#引数チェック
argLen = len(sys.argv)
if argLen -1 != 6:
	print "Error: got ", argLen -1, " args. "
	print "USAGE: wlst.cmd RPDUpload.py WLST_HOST WLST_PORT WLS_USER WLS_PASSWD RPD_LOCATION RPD_PASSWD"
	exit()

#引数セット
WLST_HOST = sys.argv[1]
WLST_PORT = sys.argv[2]
WLST_USER = sys.argv[3]
WLST_PW = sys.argv[4]
RPD_LOC = sys.argv[5]
RPD_PW = sys.argv[6]

#処理開始
#接続
print 'Connecting to ' + WLST_HOST + ':' + WLST_PORT + ' as user: ' + WLST_USER + '...'
connect(WLST_USER, WLST_PW, WLST_HOST + ':' + WLST_PORT);
print 'Connecting to Domain...'
domainCustom()
cd ('oracle.biee.admin')
print 'Connecting to BIDomain MBean...'
#ロック
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs=jarray.array([],java.lang.Object)
strs=jarray.array([],java.lang.String)
print 'Locking the domain...'
invoke('lock',objs,strs)
biinstances = get('BIInstances')
biinstance = biinstances[0]
print ('Connecting to BIInstance MBean')
cd ('..')
cd (biinstance.toString())
print ('Retrieving the name of the MBean for managing the BI Server configuration...')
biserver = get('ServerConfiguration')
print ('Connecting to the ServerConfigurationMBean...')
cd ('..')
cd (biserver.toString())
#アップロード
print ('Uploading RPD...')
argtypes = jarray.array(['java.lang.String','java.lang.String'],java.lang.String)
argvalues = jarray.array([RPD_LOC,RPD_PW],java.lang.Object)
invoke('uploadRepository',argvalues,argtypes)
#コミット
print ('Committing the update...')
cd ('..')
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs=jarray.array([],java.lang.Object)
strs=jarray.array([],java.lang.String)
invoke('commit',objs,strs)
print 'Connecting to BIInstance MBean...'
cd ('..')
cd (biinstance.toString())
print 'Getting instance status'
servicestatus=get('ServiceStatus')
print 'BIInstance MBean; ServiceStatus ' + servicestatus
#停止
print 'Calling stop...'
objs=jarray.array([],java.lang.Object)
strs=jarray.array([],java.lang.String)
invoke('stop',objs,strs)
servicestatus=get('ServiceStatus')
print 'BIInstance MBean; ServiceStatus ' + servicestatus
#開始
print 'Calling start...'
objs=jarray.array([],java.lang.Object)
strs=jarray.array([],java.lang.String)
invoke('start',objs,strs)
servicestatus=get('ServiceStatus')
print 'BIInstance MBean; ServiceStatus ' + servicestatus
print 'RPD uploaded successfully :)'
exit()
