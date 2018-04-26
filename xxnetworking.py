#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")
import getopt
import categories;
import defines;
import components;
import services;
from _me_os import xxnetos;
import demo;



def __generateH(module,folder):
    filename = module + "Networking.h"

    h_content = """//
//  $MODULE$Networking.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#ifndef $MODULE$Networking_h
#define $MODULE$Networking_h

#import "$MODULE$ServiceProtocol.h"
#import "$MODULE$NetworkingDefines.h"

#import "NSURLRequest+$MODULE$NetworkingMethods.h"
#import "NSString+$MODULE$NetworkingMethods.h"


#endif /* $MODULE$Networking_h */
"""
    h_content = h_content.replace("$MODULE$", module);
    xxnetos.mkfile(folder,filename,h_content);

def main(argv):
    if argv.count == 0:
        sys.exit();

    try:
        opts,args = getopt.getopt(argv, "hn:f:", ["help","name=","folder"]);
    except getopt.GetoptError:
        sys.exit();

    module = ""
    folder = ""
    for opt,arg in opts:
        if opt in ("-h","--help"):
            print (".py -n <module name>");
            sys.exit();
        elif opt in ("-n","--name"):
            module = arg;
        elif opt in ("-f", "--folder"):
            folder = arg;
        else:
            sys.exit();
    if  module == "" or folder == "":
        print (".py -n <module name>");
        sys.exit();

    folder = folder + "/" + module + "Networking"
    print ("module is <" + module + ">");
    print ("folder is <" + folder + ">");

    defines.generateDefines(module, folder);
    categories.generateCategories(module, folder);
    services.generateConponents(module,folder);
    components.generateConponents(module,folder);

    __generateH(module,folder);

    demo.generateDemos(module,folder);




if __name__ == '__main__':
    main(sys.argv[1:]);
