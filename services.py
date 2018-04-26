#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.append("..")
from _me_os import xxnetos;

def __generateProtocol(module,folder):
    filename = module + "ServiceProtocol.h";
    h_content = """//
//  $MODULE$ServiceProtocol.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$NetworkingDefines.h"

@protocol $MODULE$ServiceProtocol <NSObject>

@property (nonatomic, assign) $MODULE$ServiceAPIEnvironment apiEnvironment;

- (NSURLRequest *)requestWithParams:(NSDictionary *)params methodName:(NSString *)methodName requestType:($MODULE$APIManagerRequestType)requestType;
- (NSDictionary *)resultWithResponseData:(NSData *)responseData response:(NSURLResponse *)response request:(NSURLRequest *)request error:(NSError **)error;

@end
"""
    h_content = h_content.replace("$MODULE$", module);
    xxnetos.mkfile(folder,filename,h_content);


def __generateFactory(module,folder):
    filename = "$MODULE$ServiceFactory"
    h_content = """//
//  AXServiceFactory.h
//  RTNetworking
//
//  Created by casa on 14-5-12.
//  Copyright (c) 2014年 casatwy. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$ServiceProtocol.h"

@interface $MODULE$ServiceFactory : NSObject

+ (instancetype)sharedInstance;

- (id <$MODULE$ServiceProtocol>)serviceWithIdentifier:(NSString *)identifier;

@end
"""
    m_content = """//
//  AXServiceFactory.m
//  RTNetworking
//
//  Created by casa on 14-5-12.
//  Copyright (c) 2014年 casatwy. All rights reserved.
//

#import "$MODULE$ServiceFactory.h"
#import "$MODULE$DemoService.h"

/*************************************************************************/

@interface $MODULE$ServiceFactory ()

@property (nonatomic, strong) NSMutableDictionary *serviceStorage;

@end

@implementation $MODULE$ServiceFactory

#pragma mark - getters and setters
- (NSMutableDictionary *)serviceStorage
{
    if (_serviceStorage == nil) {
        _serviceStorage = [[NSMutableDictionary alloc] init];
    }
    return _serviceStorage;
}

#pragma mark - life cycle
+ (instancetype)sharedInstance
{
    static dispatch_once_t onceToken;
    static $MODULE$ServiceFactory *sharedInstance;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[$MODULE$ServiceFactory alloc] init];
    });
    return sharedInstance;
}

#pragma mark - public methods
- (id <$MODULE$ServiceProtocol>)serviceWithIdentifier:(NSString *)identifier
{
    if (self.serviceStorage[identifier] == nil) {
        self.serviceStorage[identifier] = [self newServiceWithIdentifier:identifier];
    }
    return self.serviceStorage[identifier];
}

#pragma mark - private methods
- (id <$MODULE$ServiceProtocol>)newServiceWithIdentifier:(NSString *)identifier
{
    //demo service
    
    return [[$MODULE$DemoService alloc] init];
    
    
}

@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", folder)


def generateConponents(module,folder):
    __folder = folder.rstrip("\\") + "/Services"
    if xxnetos.mkdir(__folder) == False:
        return False;

    __generateProtocol(module,__folder);
    __generateFactory(module,__folder);




