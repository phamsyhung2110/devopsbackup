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
    for root, dirs, files in os.walk(project_dir + "Helm-app/"):
        for dirname in fnmatch.filter(dirs, pattern):
            path_app = os.path.join(root,dirname) # Path from specified directory
            root_app = os.path.abspath(path_app)  # Path from root directory
            return root_app
def get_input_file():
    global app_name, env, project_dir
    input_dir =project_dir + "Input/%s/%s/"%(env,app_name)
    # pattern = "input-%s-%s*.yaml"%(env,app_name)
    for file in glob.glob(input_dir + "*.yaml"):
        # print("Input file directory: " + os.path.abspath(file))
        file_locate = str(os.path.abspath(file))
        return file_locate
def get_custom_value(value_dir,run_dir,conf_dir):
    global app_name, env, project_dir
    path_value_file = ""
    path_conf_file = ""
    path_run_file = ""
    # value_dir = project_dir +  "Custom-value-template/%s/%s/"%(env,app_name)
    for file in glob.glob(value_dir + "*.j2"):
        path_value_file = os.path.abspath(file)
    # for conf_file in glob.glob(value_dir + "conf/*.conf.j2"):
    for conf_file in glob.glob(conf_dir + "*.j2"):
        path_conf_file = os.path.abspath(conf_file)
    for conf_file in glob.glob(run_dir + "*.j2"):
        path_run_file = os.path.abspath(conf_file)
    # print("hung123" +path_conf_file)
    return path_value_file,path_conf_file,path_run_file
root_app = str(get_root_app()) + "/"
input_file = str(get_input_file())
### Template file directory ###
value_dir = project_dir +  "Custom-value-template/%s/%s/"%(env,app_name)
run_dir = project_dir +  "Run-template/%s/%s/"%(env,app_name)
conf_dir = project_dir +  "Config-template/%s/%s/"%(env,app_name)
###
value_file_tem = str(get_custom_value(value_dir,run_dir,conf_dir)[0])
run_file_tem = str(get_custom_value(value_dir,run_dir,conf_dir)[2])
#get_custom_value()
print("App:  "+ root_app)
print("Input file: "+ input_file)
print("Value file:  " + value_file_tem)
def get_input_open():
        with open(input_file, 'r', encoding='UTF-8') as file:
            return file.read()

def change_values_file(render_to,tem_file):
    global value_file_tem, input_file, root_app,run_file_tem
    # render_to = project_dir + "Custom-value-complete/value/%s/%s/"%(app_name,env) + os.path.basename(value_file_tem)
    name_split = render_to.split(".j2")[0]
    # value_file_tem_yaml =root_app + name_split 
    def save_values(out_put):
        with open(name_split, 'w', encoding='UTF-8') as file:
            file.write(out_put)
            print("New file generated " + name_split)    
    def get_template_values():
        with open(tem_file , 'r', encoding='UTF-8') as file:
            return file.read()  
    # def get_template_run():
    #     with open(value_file_tem , 'r', encoding='UTF-8') as file:
    #         return file.read()  
    input = yaml.safe_load(get_input_open())
    template_input = get_template_values()
    template_values = Template(template_input) 
    out_put = template_values.render(**input)
    save_values(out_put)
    return name_split

if mod_nginx=="--mod-nginx":
    # conf_file = str(get_custom_value(render_config)[1])
    conf_file_tem =  str(get_custom_value(value_dir,run_dir,conf_dir)[1])
    helm_chart_folder = project_dir + "Helm-app/%s/config/"%app_name 
    print("Config file: "+ conf_file_tem)
    def change_nginx(render_config):
        global conf_file_tem, input_file, root_app, project_dir, env
        # render_config = project_dir + "Config/%s/%s/"%(env,app_name) + os.path.basename(conf_file_tem)
        name_split = render_config.split(".j2")[0]
        def save_nginx(out_put):                                  ## Save output rendered
            with open(name_split , 'w', encoding='UTF-8') as file:
                return file.write(out_put)                        ## Get template
        def get_template_nginx():
            with open(conf_file_tem, 'r', encoding='UTF-8') as file:
                return file.read()
        input = yaml.safe_load(get_input_open())
        nginx_template = get_template_nginx()
        template = Template(nginx_template)
        out_put = template.render(**input)
        save_nginx(out_put)
        shutil.copy2(name_split, helm_chart_folder)
        return name_split
    
else: print("No nginx config") 


# run_dir = project_dir +  "Run-template/%s/%s/"%(env,app_name)
## Template file
value_file_tem = str(get_custom_value(value_dir,run_dir,conf_dir)[0])
run_file_tem = str(get_custom_value(value_dir,run_dir,conf_dir)[2])  
## Conf_file_tem define in change__nginx()
## Render to
render_value = project_dir + "Custom-value-complete/value/%s/%s/"%(env,app_name) + os.path.basename(value_file_tem)
render_run = project_dir + "Custom-value-complete/run/%s/%s/"%(env,app_name) + os.path.basename(run_file_tem)
if mod_nginx == "--mod-nginx":
    render_config = project_dir + "Custom-value-complete/config/%s/%s/"%(env,app_name) + os.path.basename(conf_file_tem)
    conf_file = change_nginx(render_config)
else:
    print(" ")
## Value file complete
value_file = change_values_file(render_value,value_file_tem)
run_file = change_values_file(render_run,run_file_tem)


def install():
    global env, action, app_name, root_app, value_file, run_file
    # os.chdir(root_app)   
    run_dir = project_dir +  "Custom-value-template/%s/%s/"%(env,app_name) + "run"
    print("Executing command: kubectl apply -f " + run_file)
    time.sleep(0.25)
    subprocess.call("kubectl apply -f " + run_file)
    
    ## Action
    print("Executing command: helm " + action + " " + app_name + " "  + project_dir + "Helm-app/%s/ -f "%app_name + value_file )
    time.sleep(0.5)
    subprocess.call("helm " + action + " " + app_name + " " + project_dir + "Helm-app/%s/ -f "%app_name + value_file)
def uninstall():
        print("Executing command: helm uninstall %s"%app_name )
        subprocess.call("helm uninstall %s"%app_name)
if action == "uninstall":
    uninstall()
else:
    install()