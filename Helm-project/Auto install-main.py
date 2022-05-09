from base64 import encode
from codecs import ignore_errors
from genericpath import isfile
import os,shutil,glob,sys,re
from platform import release
from pydoc import describe
import subprocess
import fnmatch,yaml,jinja2,time
from unicodedata import name
from jinja2 import Template
#
action = sys.argv[1]
release_name = sys.argv[2]
chart_dir = sys.argv[3]
env = sys.argv[4]
mod_nginx = sys.argv[5]
pattern = "%s*"%chart_dir
print(pattern)
project_dir = ".\\Helm-project\\"
def uninstall():
        print("Executing command: helm uninstall %s"%release_name )
        subprocess.call("helm uninstall %s"%release_name)
while True:
    if action == "uninstall":
        uninstall()
        break
    def get_root_app():
        global pattern,project_dir
        for root, dirs, files in os.walk(project_dir + "Helm-app\\"):
            for dirname in fnmatch.filter(dirs, pattern):
                path_app = os.path.join(root,dirname) # Path from specified directory
                root_app = os.path.abspath(path_app)  # Path from root directory
                return root_app
    # def get_input_file():
    #     global chart_dir, env, project_dir
    #     input_dir =project_dir + "Input\\%s\\%s\\"%(env,chart_dir)
    #     # pattern = "input-%s-%s*.yaml"%(env,chart_dir)
    #     for file in glob.glob(input_dir + "*.yaml"):
    #         # print("Input file directory: " + os.path.abspath(file))
    #         file_locate = str(os.path.abspath(file))
    #         return file_locate
    def get_input_file():
        global chart_dir, env, project_dir
        input_dir =project_dir + "Input\\"
        # pattern = "input-%s-%s*.yaml"%(env,chart_dir)
        for root,dirs,files in os.walk(input_dir + "\\%s\\%s\\"%(chart_dir,env)):
            for file in files:
                if file.endswith("yaml"):
                    file_locate = str(os.path.join(root,file))
                    print(file_locate)
                return file_locate
    print("File locate: " + str(get_input_file()))
    def get_custom_value(value_dir,run_dir,conf_dir):
        global chart_dir, env, project_dir
        path_value_file = ""
        path_conf_file = ""
        path_run_file = ""
        list_file_run = []
        # value_dir = project_dir +  "Custom-value-template\\%s\\%s\\"%(env,chart_dir)
        for file in glob.glob(value_dir + "*.j2"):
            path_value_file = os.path.abspath(file)
        # for conf_file in glob.glob(value_dir + "conf\\*.conf.j2"):
        for conf_file in glob.glob(conf_dir + "*.j2"):
            path_conf_file = os.path.abspath(conf_file)
        for root,dirs,run_file in os.walk(run_dir):
            for file in run_file:
                if file.endswith("j2"):
                    path_run_file = os.path.join(root,file)
                    list_file_run.append(path_run_file)    
        return path_value_file,path_conf_file,list_file_run
    root_app = str(get_root_app()) + "\\"
    input_file = str(get_input_file())
    ### Template file directory ###
    value_dir = project_dir +  "Custom-value-template\\%s\\%s\\"%(env,chart_dir)
    run_dir = project_dir +  "Run-template\\%s\\%s\\"%(env,chart_dir)
    conf_dir = project_dir +  "Config-template\\%s\\%s\\"%(env,chart_dir)
    ###
    value_file_tem = str(get_custom_value(value_dir,run_dir,conf_dir)[0])
    run_file_tem = get_custom_value(value_dir,run_dir,conf_dir)[2]
    #get_custom_value()
    print("App:  "+ root_app)
    print("Input file: "+ input_file)
    print("Value file:  " + value_file_tem)
    print("Run file:  " + str(run_file_tem))
    # def get_input_open():
    #         data = {}
    #         for per_input_file in input_file:
    #             with open(per_input_file, 'r', encoding='UTF-8') as file:
    #                 # return file.read()
    #                 yaml_data_input = yaml.safe_load(file)
    #                 for key,value in yaml_data_input.items():
    #                     data.update({key:value})
    #                     data_input = yaml.dump(data).replace("null","")
    #                     print(data_input)
    #                     return data_input
    def get_input_file():
        global chart_dir, env, project_dir
        input_dir =project_dir + "Input\\"
        data = {}
        for root,dir,files in os.walk(input_dir + "\\%s\\%s\\"%(chart_dir,env)):
            for file in files:
                if file.endswith("yaml"):
                    file_locate = str(os.path.join(root,file))
                    a = open(file_locate, "r")   
                    input = yaml.safe_load(a)
                    for key,value in input.items():
                        data.update({key:value})
        data_input = yaml.dump(data).replace("null", "")
        print(yaml.dump(data).replace("null", ""))
        return data_input
    yaml_input_dumped  = get_input_file()
    def change_values_file(render_to,tem_file):
        global value_file_tem, input_file, root_app,run_file_tem, yaml_input_dumped
        # render_to = project_dir + "Custom-value-complete\\value\\%s\\%s\\"%(chart_dir,env) + os.path.basename(value_file_tem)
        name_split = render_to.split(".j2")[0]
        # value_file_tem_yaml =root_app + name_split 
        def save_values(out_put):
            with open(name_split, 'w', encoding='UTF-8') as file:
                file.write(out_put)
                print("New file generated " + name_split)    
        def get_template_values():
            for file in tem_file:
                with open(tem_file , 'r', encoding='UTF-8') as file:
                    return file.read()   
        data_input_final = yaml.safe_load(yaml_input_dumped)
        template_input = get_template_values()
        template_values = Template(template_input) 
        out_put = template_values.render(**data_input_final)
        save_values(out_put)
        return name_split

    if mod_nginx=="--mod-nginx":
        # conf_file = str(get_custom_value(render_config)[1])
        conf_file_tem =  str(get_custom_value(value_dir,run_dir,conf_dir)[1])
        helm_chart_folder = project_dir + "Helm-app\\%s\\config\\"%chart_dir 
        print("Config file: "+ conf_file_tem)
        def change_nginx(render_config):
            global conf_file_tem, input_file, root_app, project_dir, env, yaml_input_dumped
            # render_config = project_dir + "Config\\%s\\%s\\"%(env,chart_dir) + os.path.basename(conf_file_tem)
            name_split = render_config.split(".j2")[0]
            def save_nginx(out_put):                                  ## Save output rendered
                with open(name_split , 'w', encoding='UTF-8') as file:
                    return file.write(out_put)                        ## Get template
            def get_template_nginx():
                with open(conf_file_tem, 'r', encoding='UTF-8') as file:
                    return file.read()
            data_input_final = yaml.safe_load(yaml_input_dumped)
            nginx_template = get_template_nginx()
            template = Template(nginx_template)
            out_put = template.render(**data_input_final)
            save_nginx(out_put)
            shutil.copy2(name_split, helm_chart_folder)
            return name_split
        
    else: print("No nginx config") 


    # run_dir = project_dir +  "Run-template\\%s\\%s\\"%(env,chart_dir)
    ## Template file
    value_file_tem = str(get_custom_value(value_dir,run_dir,conf_dir)[0])
    run_file_tem = get_custom_value(value_dir,run_dir,conf_dir)[2] 
    ## Conf_file_tem define in change__nginx()
    ## Render to
    render_value = project_dir + "Custom-value-complete\\value\\%s\\%s\\"%(env,chart_dir) + os.path.basename(value_file_tem)
    for file in run_file_tem:
        render_run = project_dir + "Custom-value-complete\\run\\%s\\%s\\"%(env,chart_dir) + os.path.basename(file)  
        run_file = change_values_file(render_run,file)
    if mod_nginx == "--mod-nginx":
        render_config = project_dir + "Custom-value-complete\\config\\%s\\%s\\"%(env,chart_dir) + os.path.basename(conf_file_tem)
        conf_file = change_nginx(render_config)
    else:
        print(" ")
    ## Value file complete
    value_file = change_values_file(render_value,value_file_tem)
    def install():
        global env, action, chart_dir, root_app, value_file, run_file, release_name
        # os.chdir(root_app)   s
        run_dir = project_dir +  "Custom-value-complete\\run\\" + env + "\\" +chart_dir +"\\"
        print("Executing command: kubectl apply -f " + run_dir )
        time.sleep(0.25)
        subprocess.call("kubectl apply -f " + run_dir)
        
        ## Action
        print("Executing command: helm " + action + " " + release_name + " "  + project_dir + "Helm-app\\%s\\ -f "%chart_dir + value_file )
        time.sleep(0.5)
        subprocess.call("helm " + action + " " + release_name + " " + project_dir + "Helm-app\\%s\\ -f "%chart_dir + value_file)
    def uninstall():
            print("Executing command: helm uninstall %s"%release_name )
            subprocess.call("helm uninstall %s"%release_name)

    install()
    break