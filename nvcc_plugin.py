from jupyternvcc.jupyternvcc_plugin import NVCCPLUGIN 
def load_ipython_extension(ip):
    #initialize the  plugin
    nvcc_plugin = NVCCPLUGIN(ip) 
    ip.register_magics(nvcc_plugin)
