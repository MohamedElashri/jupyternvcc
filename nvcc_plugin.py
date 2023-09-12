from jupyternvcc.jupyternvcc_plugin import nvccplugin 
def load_ipython_extension(ip):
    #initialize the  plugin
    nvcc_plugin = nvccplugin(ip) 
    ip.register_magics(nvcc_plugin)
