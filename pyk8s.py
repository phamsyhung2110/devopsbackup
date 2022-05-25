from base64 import encode
from genericpath import isfile
import os,shutil,glob,sys,re
from pydoc import describe
import subprocess
import fnmatch,yaml,jinja2,time
from unicodedata import name
from jinja2 import Template
from yaml.representer import Representer
from yaml.dumper import Dumper
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver
#
value_tem = "./Helm-project/Custom-value-template/dev/lhc-install/lhc-install-value-dev.j2"































# action = "install"
# app_name = "lhc-install"
# env = "dev"
# pattern = app_name
# project_dir = "./Helm-Project/"

# def get_root_app():
#     global pattern,project_dir
#     for root, dirs, files in os.walk(project_dir + "Helm-app/"):
#         for dirname in fnmatch.filter(dirs, pattern):
#             path_app = os.path.join(root,dirname) # Path from specified directory
#             root_app = os.path.abspath(path_app)  # Path from root directory
#             return root_app
# def get_input_file():
#     global app_name, env, project_dir
#     input_dir =project_dir + "Input/"
#     file_list = []
#     for root,dir,files in os.walk(input_dir + "/%s/%s/"%(app_name,env)):
#         for file in files:
#             if file.endswith("yaml"):
#                 file_locate = str(os.path.join(root,file))
#                 file_list.append(file_locate)
#     print(file_list)
#     return file_list
# def get_custom_value(value_dir):
#     global app_name, env, project_dir
#     path_conf_file = ""
#     path_run_file = ""
#     value_tem_file = ''
#     for file in glob.glob(value_dir + "*.j2"):
#         value_tem_file = os.path.abspath(file)
#     for conf_file in glob.glob(value_dir + "conf/*.j2"):
#         path_conf_file = os.path.abspath(conf_file)
#     for conf_file in glob.glob(value_dir + "*.j2"):
#         path_run_file = os.path.abspath(conf_file)
#     return value_tem_file,path_conf_file,path_run_file
# root_app = str(get_root_app()) + "/"
# input_file_list = get_input_file()
# value_dir = project_dir +  "Custom-value-template/%s/%s/"%(env,app_name)
# run_dir = project_dir +  "Run-template/%s/%s/"%(env,app_name)  
# value_file_tem = str(get_custom_value(value_dir)[0])
# run_file_tem = str(get_custom_value(run_dir)[2])
# def change_values_file(render_to,tem_dir):
#     global  input_file_list, root_app  
#     name_split = render_to.split(".j2")[0]
#     def save_values(out_put):
#         with open(name_split, 'w', encoding='UTF-8') as file:
#             file.write(out_put)
#             print("Name split " + name_split)    
#     def get_template_values():
#         with open(tem_dir , 'r', encoding='UTF-8') as file:
#             return file.read() 
#     for file in input_file_list: 
#         with open(file, 'r', encoding='UTF-8') as data:    
#             input = yaml.safe_load(data)
#             template_input = get_template_values()
#             template_values = Template(template_input) 
#             out_put = template_values.render(**input)
#             save_values(out_put)
            
      
# render_value = project_dir + "Custom-value-complete/value/%s/%s/"%(env,app_name) + os.path.basename(value_file_tem)
# render_run = project_dir + "Custom-value-complete/run/%s/%s/"%(env,app_name) + os.path.basename(run_file_tem)
# value_file = change_values_file(render_value,value_file_tem)
# run_file = change_values_file(render_run,run_file_tem)