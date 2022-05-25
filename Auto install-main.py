from base64 import encode
import os,shutil,glob,sys,re
from pydoc import describe
import subprocess
import fnmatch,yaml,jinja2,time
from unicodedata import name
from jinja2 import Template
#
action = sys.argv[1]
app_name = sys.argv[2]
env = sys.argv[3]
mod_nginx = sys.argv[4]
pattern = app_name
project_dir = "./Helm-Project/"
def get_root_app():
    global pattern,project_dir
    for root, dirs, files in os.walk(project_dir + "/Helm-app/"):
        for dirname in fnmatch.filter(dirs, pattern):
            path_app = os.path.join(root,dirname) # Path from specified directory
            root_app = os.path.abspath(path_app)  # Path from root directory
            return root_app


def get_custom_value(value_dir):
    global app_name, env, project_dir
    path_conf_file = ""
    path_run_file = ""
    value_tem_file = ''
    for file in glob.glob(value_dir + "*.j2"):
        value_tem_file = os.path.abspath(file)
    for conf_file in glob.glob(value_dir + "conf/*.j2"):
        path_conf_file = os.path.abspath(conf_file)
    for conf_file in glob.glob(value_dir + "run/*.j2"):
        path_run_file = os.path.abspath(conf_file)
    return value_tem_file,path_conf_file,path_run_file
root_app = str(get_root_app()) + "/"

value_dir = project_dir +  "Custom-value-template/%s/%s/"%(env,app_name)
run_dir = project_dir +  "Run/%s/%s/"%(env,app_name)
value_file_tem = str(get_custom_value(value_dir)[0])
run_file_tem = str(get_custom_value(run_dir)[2])

print("App:  "+root_app)
print("Value file:  " + value_file_tem)
print("Run file: " + run_file_tem)
input_dir = project_dir+"Input/"
def get_input_open():
    for root,dir,files in os.walk(input_dir + "/%s/%s/"%(app_name,env)):
        for file in files:
            if file.endswith("yaml"):
                file_locate = str(os.path.join(root,file))
                print(file_locate)
                with open(file_locate, 'r', encoding='UTF-8') as data:
                    return data.read()
input_file = get_input_open()
print("Input file: "+ input_file)
def change_values_file(render_to,tem_dir):
    global  input_file, root_app
    # render_to = project_dir + "Custom-value-complete/value/%s/%s/"%(app_name,env) + os.path.basename(value_file_tem)
    name_split = render_to.split(".j2")[0]
    # value_file_tem_yaml =root_app + name_split 
    def save_values(out_put):
        with open(name_split, 'w', encoding='UTF-8') as file:
            file.write(out_put)
            print("Name split " + name_split)    
    def get_template_values():
        with open(tem_dir , 'r', encoding='UTF-8') as file:
            return file.read() 
    for file in input_file:   
        input = yaml.safe_load(file)
        template_input = get_template_values()
        template_values = Template(template_input) 
        out_put = template_values.render(**input)
        save_values(out_put)
        return name_split

if mod_nginx=="--mod-nginx":
    conf_file = str(get_custom_value()[1])
    print("Config file: "+conf_file)
    def change_nginx():
        global conf_file, input_file, root_app, project_dir, env
        render_to_conf = project_dir + "Config/%s/%s/"%(env,app_name) + os.path.basename(conf_file)
        name_split = render_to_conf.split(".j2")[0]
        def save_nginx(out_put):                                  ## Save output rendered
            with open(name_split , 'w', encoding='UTF-8') as file:
                return file.write(out_put)                        ## Get template
        def get_template_nginx():
            with open(conf_file, 'r', encoding='UTF-8') as file:
                return file.read()
        input = yaml.safe_load(get_input_open())
        nginx_template = get_template_nginx()
        template = Template(nginx_template)
        out_put = template.render(**input)
        save_nginx(out_put)
        return name_split
    change_nginx()
else: print("No nginx config")    
render_value = project_dir + "Custom-value-complete/value/%s/%s/"%(env,app_name) + os.path.basename(value_file_tem)
render_run = project_dir + "Custom-value-complete/run/%s/%s/"%(env,app_name) + os.path.basename(value_file_tem)
value_file = change_values_file(render_value,value_dir)
run_file = change_values_file(render_run,run_dir)
def install():
    global env, action, app_name, root_app, value_file, run_file
    os.chdir(root_app)   
    run_dir = project_dir +  "Custom-value-template/%s/%s/"%(env,app_name) + "run"
    print("Executing command: kubectl apply -f " + run_file)
    print("hung" + run_dir + "conf/*.j2")
    ## Action
    print("Executing command: helm " + action + " " + app_name + " .  -f " + value_file )
    #subprocess.call("helm " + action + " " + app_name + " .  -f " + value_file) 

install()