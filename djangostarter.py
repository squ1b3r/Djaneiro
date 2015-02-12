import sublime,sublime_plugin,os

try:
	from .djangoFileCode import *
except:
	from djangoFileCode import *

class DjangoCreate:
	@staticmethod
	def createMainFolder(path,project,app):
		path=path[0]+'\\'+ project
		if not os.path.exists(path):
			os.makedirs(path)
		return path
	@staticmethod 
	def createProjectFiles(location,project,app):
		pathsToCreate = [location+'\\'+a for a in [project,app,'templates']]
		for path in pathsToCreate:
			if not os.path.exists(path):
				os.makedirs(path)
		with open(location+'\\manage.py','w') as f:
			f.write(MANAGE_PY(project))
		projectSitePath = location + '\\' + project
		projectSiteFiles={'__init__.py':'','settings.py':SETTINGS_PY(project,app),'urls.py':URLS_PY(),'wsgi.py':WSGI_PY(project)}
		for key in projectSiteFiles.keys():
			with open(projectSitePath+'\\'+key,'w') as f:
				f.write(projectSiteFiles[key])
		appPath = location + '\\' + app 
		if not os.path.exists(appPath+'\\migrations'):
			os.makedirs(appPath+'\\migrations')
		appFiles={'__init__.py':'','admin.py':APP_ADMIN(),'models.py':APP_MODELS(),'tests.py':APP_TESTS(),'views.py':APP_VIEWS()}
		for key in appFiles.keys():
			with open(appPath+'\\'+key,'w') as f:
				f.write(appFiles[key])
		return location+'\\manage.py'

class NewdjangoCommand(sublime_plugin.WindowCommand):
	def run(self,paths=[]):
		self.path=paths 
		self.window.show_input_panel("Django Project Name:", '', lambda s: self.getAppName(s), None, None)
	def getAppName(self,project):
		self.project=project
		self.window.show_input_panel("Django App Name:", '', lambda s: self.doRest(s), None, None)
	def doRest(self,appName):
		for index,elem in enumerate(self.path):
			if '.' in elem:
				self.path[index]=elem.replace(elem.split('\\')[-1],'')
		p = DjangoCreate.createMainFolder(self.path,self.project,appName)
		manage = DjangoCreate.createProjectFiles(p,self.project,appName)
		self.window.open_file(manage)
		
class RelativedjangoCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		f=self.view.file_name()
		self.path=[self.getFolderName(f)]
		sublime.active_window().show_input_panel("Django Project Name:", '', lambda s: self.rest(s), None, None)
	def rest(self,project):
		self.project=project 
		sublime.active_window().show_input_panel("Django App Name:", '', lambda s: self.final(s), None, None)
	def final(self,app):
		self.app=app 
		p = DjangoCreate.createMainFolder(self.path,self.project,self.app)
		manage = DjangoCreate.createProjectFiles(p,self.project,self.app)
		sublime.active_window().open_file(manage)
	def getFolderName(self,file):
		return file.replace(file.split('\\')[-1],'')