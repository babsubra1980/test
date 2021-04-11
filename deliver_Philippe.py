import json
from datetime import datetime
import os
import shutil
import zipfile
import hashlib

def file_as_bytes(file):
    with file:
        return file.read()
				
# PPO20190628 begin
def copystk( rootdir, stkDir, stkKey, extension, folderkey, folder=""):
	# PPO20190628 end

	#print rootdir, stkDir, stkKey, extension, folderkey
	# Copy related stk file
	for inputgcc in os.listdir('.\\'+rootdir):
		# print inputgcc
		if inputgcc.find(folderkey)>=0:
			# print "folderkey found"
			
			currentinputgccDir='.\\'+rootdir+'\\'+inputgcc
			
			# PPO20190628 begin
 			if folder!="":
				for foldername in os.listdir(currentinputgccDir):
					if foldername.find(folder)>=0:
						currentinputgccDir = currentinputgccDir + '\\' +foldername
						break
			# PPO20190628 end

			#print currentinputgccDir
			for stkfile in os.listdir(currentinputgccDir):
				# print stkfile
				if (stkfile.find(stkKey)>=0) and (stkfile[-4:]==extension):
					print 'From: '+currentinputgccDir+'\\'+stkfile
					print 'To: '+stkDir
					shutil.copy(currentinputgccDir+'\\'+stkfile, stkDir)
					
with open('.\config\OS6_delivery.json') as f:
  config = json.load(f)

#print config

# create folder 
rootdirName = '.\\output\\'+datetime.today().strftime('%Y%m%d%H%M')
zipDir = rootdirName+'\\zip'
# Create target Directory
try:
	os.mkdir(rootdirName)
	print("Results will be in " , rootdirName ,  " Created ") 
	
	os.mkdir(zipDir)
except:
	shutil.rmtree(rootdirName)
	os.mkdir(rootdirName)

for platform in config['platforms']:
	print "################# ", platform['name']
	platformDir = rootdirName+'\\'+platform['name']+'v'+platform['os6 release']+'.'+platform['agile rev']
	# Create platform Directory
	os.mkdir(platformDir)

	#=====================================================================
	# ONIE files
	#=====================================================================
	if "ONIE name" in platform:
 
		ONIEDir = platformDir+'\\ONIE_Files'
		os.mkdir(ONIEDir)
		
		# Copy platform related ONIE files
		for oniedir in os.listdir('.\\input_Broadcom'):
			
			if oniedir.find('ONIE')>=0:
				# PPO20190628 begin
				currentOnieDir='.\\input_Broadcom\\'+oniedir+'\\ONIE'
				# PPO20190628 end

				for oniefile in os.listdir(currentOnieDir):
					
					if oniefile.find(platform['ONIE name'])>0:
						shutil.copy(currentOnieDir+'\\'+oniefile,ONIEDir)
 
	#=====================================================================
	# Mibs files
	#=====================================================================
	if platform['mibs'] == 'Yes':
 
		mibsDir = platformDir+'\\'+platform['name']+'_mibs'
		#os.mkdir(mibsDir)
		
		# Copy related mibs files
		for inputgcc in os.listdir('.\\input_Broadcom'):
			
			if inputgcc.find('GCC')>0:
				currentinputgccDir='.\\input_Broadcom\\'+inputgcc
				#print currentinputgccDir
				
				# PPO20190628 begin
				for stkfolder in os.listdir(currentinputgccDir):
					#print mibsfilefolder
					
					if stkfolder.find('STK')>=0:
						for mibsfilefolder in os.listdir(currentinputgccDir+"\\"+stkfolder):
						# PPO20190628 end

							if mibsfilefolder.find('mibs')>=0:
								print 'From: '+currentinputgccDir+'\\'+mibsfilefolder
								print 'To: '+mibsDir
								# PPO20190628 begin
								shutil.copytree(currentinputgccDir+'\\'+stkfolder+'\\'+mibsfilefolder,mibsDir)
								# PPO20190628 end

						
	#=====================================================================
	# Drivers files
	#=====================================================================
	try:
		for driver in platform['drivers']:
	 
			driverDir = platformDir

			# Copy related drivers files
			for inputdriverfolder in os.listdir('.\\input_Dell\\drivers\\'):
				
				if inputdriverfolder == platform['name']:
						
					currentinputdriverDir='.\\input_Dell\\drivers\\'+inputdriverfolder
					#print currentinputdriverDir
					for driverfile in os.listdir(currentinputdriverDir):
						if driverfile.find(driver)>=0:
							print 'From: '+currentinputdriverDir+'\\'+driverfile
							print 'To: '+driverDir
							shutil.copy(currentinputdriverDir+'\\'+driverfile, driverDir)
	except:
		print "No drivers required"

	#=====================================================================
	# Other folders
	#=====================================================================
	try:
		for otherfolder in platform['other folders']:
			print otherfolder
			otherfolderDir = platformDir

			# Copy related other folders
			for inputotherfolderfolder in os.listdir('.\\input_Dell\\other folders\\'):
				print inputotherfolderfolder
				if inputotherfolderfolder == platform['name']:
						
					currentinputotherfolderDir='.\\input_Dell\\other folders\\'+inputotherfolderfolder
					#print currentinputotherfolderDir
					for otherfolder in os.listdir(currentinputotherfolderDir):
						if otherfolder.find(otherfolder)>=0:
							print 'From: '+currentinputotherfolderDir+'\\'+otherfolder
							print 'To: '+otherfolderDir
							shutil.copytree(currentinputotherfolderDir+'\\'+otherfolder, otherfolderDir+'\\'+otherfolder)
	except:
		print "No other folder required"



	#=====================================================================
	# stk files
	#=====================================================================
	# PPO20190628 begin
	copystk( "input_Broadcom", platformDir, platform['stk'], ".stk", "GCC", "STK")
	# PPO20190628 end

	#=====================================================================
	# upgrade document files
	#=====================================================================
	
	copystk( "input_Dell", platformDir, platform['upgrade document'], ".pdf", "upgrade")

	#=====================================================================
	# release note files
	#=====================================================================
	
	copystk( "input_Dell", platformDir, platform['release note'], ".pdf", "release")

					
	#=====================================================================
	# mixed stacking files
	#=====================================================================
	try:
		mixedDir = platformDir+'\\'+platform['mixed stacking']['folder']
		os.mkdir(mixedDir)
		
		# copy stacked stk
		for platformStk in config['platforms']:
			if platformStk['name'] in platform['mixed stacking']['platforms']:
				# PPO20190628 begin
				copystk("input_Broadcom", mixedDir,platformStk['stk'], ".stk", "GCC", "STK")
				# PPO20190628 end

		# Copy related mibs files
		for inputitb in os.listdir('.\\input_Broadcom'):
				
				if inputitb.find('itb')>0:
					# PPO20190628 begin
					currentinputitbDir='.\\input_Broadcom\\'+inputitb+'\\ITB'
					# PPO20190628 end
					#print currentinputitbDir
					for itbfile in os.listdir(currentinputitbDir):
						#print itbfile
						if (itbfile.find(platform['mixed stacking']['itb'])>=0) and (itbfile[-4:]=='.itb'):
							print 'From: '+currentinputitbDir+'\\'+itbfile
							print 'To: '+mixedDir
							shutil.copy(currentinputitbDir+'\\'+itbfile, mixedDir)
		
	except:
		print "No mixed stacking"
		
	# Zipping and MD5 the zip

	print 'creating archive'
	zf = zipfile.ZipFile(zipDir+"\\"+platform['name']+'v'+platform['os6 release']+'.'+platform['agile rev']+'.zip', compression=zipfile.ZIP_DEFLATED, mode='w')
	delivery_path_content = os.walk(platformDir)
	try:
		for root, folders, files in delivery_path_content:
						
			# Include all subfolders, including empty ones.
			for folder_name in folders:
				absolute_path = os.path.join(root, folder_name)
				relative_path = absolute_path.replace(rootdirName + "\\"+platform['name']+'v'+platform['os6 release']+'.'+platform['agile rev']+ '\\','')
				zf.write(absolute_path, relative_path)
			for file_name in files:
				print root
				absolute_path = os.path.join(root, file_name)
				print absolute_path
				relative_path = absolute_path.replace(rootdirName + "\\"+platform['name']+'v'+platform['os6 release']+'.'+platform['agile rev']+ '\\','')
				print relative_path
				zf.write(absolute_path, relative_path)

	finally:
		print 'closing'
		zf.close()
		
	#create MD5

	textFile = open(zipDir+"\\"+platform['name']+'v'+platform['os6 release']+'.'+platform['agile rev']+'.md5', "w+")
	textFile.write(hashlib.md5(file_as_bytes(open(zipDir+"\\"+platform['name']+'v'+platform['os6 release']+'.'+platform['agile rev']+'.zip', 'rb'))).hexdigest())
	textFile.close()
	
		