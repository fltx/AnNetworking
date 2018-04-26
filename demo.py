#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.append("..")
from _me_os import xxnetos;

def __generateDemoService(module,folder):

    filename = "$MODULE$DemoService"

    h_content = """//
//  $MODULE$DemoService.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$ServiceProtocol.h"

static NSString * const $MODULE$NetworkingDemoServiceIdentifier = @"DemoService";

@interface $MODULE$DemoService : NSObject<$MODULE$ServiceProtocol>

@end
"""
    m_content = """//
//  $MODULE$DemoService.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "$MODULE$DemoService.h"
#import <AFNetworking/AFNetworking.h>
#import "$MODULE$Networking.h"

@interface $MODULE$DemoService ()

@property (nonatomic, strong) NSString *publicKey;
@property (nonatomic, strong) NSString *privateKey;
@property (nonatomic, strong) NSString *baseURL;

@property (nonatomic, strong) AFHTTPRequestSerializer *httpRequestSerializer;

@end
@implementation $MODULE$DemoService

#pragma mark - public methods
- (NSURLRequest *)requestWithParams:(NSDictionary *)params methodName:(NSString *)methodName requestType:($MODULE$APIManagerRequestType)requestType
{
    if (requestType == $MODULE$APIManagerRequestTypeGET) {
        NSString *urlString = [NSString stringWithFormat:@"%@/%@", self.baseURL, methodName];
        NSString *tsString = [NSUUID UUID].UUIDString;
        NSString *md5Hash = [[NSString stringWithFormat:@"%@%@%@", tsString, self.privateKey, self.publicKey] $MODULE$_MD5];
        NSMutableURLRequest *request = [self.httpRequestSerializer requestWithMethod:@"GET"
                                                                           URLString:urlString
                                                                          parameters:@{
                                                                                       @"apikey":self.publicKey,
                                                                                       @"ts":tsString,
                                                                                       @"hash":md5Hash
                                                                                       }
                                                                               error:nil];
        return request;
    }
    
    return nil;
}

- (NSDictionary *)resultWithResponseData:(NSData *)responseData response:(NSURLResponse *)response request:(NSURLRequest *)request error:(NSError **)error
{
    NSMutableDictionary *result = [[NSMutableDictionary alloc] init];
    result[k$MODULE$ApiProxyValidateResultKeyResponseData] = responseData;
    result[k$MODULE$ApiProxyValidateResultKeyResponseJSONString] = [[NSString alloc] initWithData:responseData encoding:NSUTF8StringEncoding];
    result[k$MODULE$ApiProxyValidateResultKeyResponseJSONObject] = [NSJSONSerialization JSONObjectWithData:responseData options:0 error:NULL];
    return result;
}

#pragma mark - getters and setters
- (NSString *)publicKey
{
    return @"d97bab99fa506c7cdf209261ffd06652";
}

- (NSString *)privateKey
{
    return @"31bb736a11cbc10271517816540e626c4ff2279a";
}

- (NSString *)baseURL
{
    if (self.apiEnvironment == $MODULE$ServiceAPIEnvironmentRelease) {
        return @"https://gateway.marvel.com:443/v1";
    }
    if (self.apiEnvironment == $MODULE$ServiceAPIEnvironmentDevelop) {
        return @"https://gateway.marvel.com:443/v1";
    }
    if (self.apiEnvironment == $MODULE$ServiceAPIEnvironmentReleaseCandidate) {
        return @"https://gateway.marvel.com:443/v1";
    }
    return @"https://gateway.marvel.com:443/v1";
}

- ($MODULE$ServiceAPIEnvironment)apiEnvironment
{
    return $MODULE$ServiceAPIEnvironmentRelease;
}

- (AFHTTPRequestSerializer *)httpRequestSerializer
{
    if (_httpRequestSerializer == nil) {
        _httpRequestSerializer = [AFHTTPRequestSerializer serializer];
        [_httpRequestSerializer setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
    }
    return _httpRequestSerializer;
}

@synthesize apiEnvironment;

@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", folder)

def __generateDemoApiManager(module,folder):

    filename = "$MODULE$DemoAPIManager"

    h_content = """//
//  DemoAPIManager.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "$MODULE$APIBaseManager.h"
#import "$MODULE$NetworkingDefines.h"

@interface $MODULE$DemoAPIManager : $MODULE$APIBaseManager<$MODULE$APIManager>

@end
"""
    m_content = """//
//  DemoAPIManager.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "$MODULE$DemoAPIManager.h"
#import "$MODULE$DemoService.h"


@interface $MODULE$DemoAPIManager()<$MODULE$APIManagerParamSource,$MODULE$APIManagerValidator>
@end
@implementation $MODULE$DemoAPIManager

- (instancetype)init{
    if (!(self = [super init])) return self;
    
    self.paramSource = self;
    self.validator = self;
    
    return self;
}
#pragma mark - $MODULE$APIManager
- (NSString *)methodName
{
    return @"public/characters";
}

- (NSString *)serviceIdentifier
{
    return $MODULE$NetworkingDemoServiceIdentifier;
}

- ($MODULE$APIManagerRequestType)requestType
{
    return $MODULE$APIManagerRequestTypeGET;
}

#pragma mark - $MODULE$APIManagerParamSource
- (NSDictionary *)paramsForApi:($MODULE$APIBaseManager *)manager{
    return nil;
}

#pragma mark - $MODULE$APIManagerValidator
- ($MODULE$APIManagerErrorType)manager:($MODULE$APIBaseManager *)manager isCorrectWithParamsData:(NSDictionary *)data{
    return $MODULE$APIManagerErrorTypeNoError;
}
- ($MODULE$APIManagerErrorType)manager:($MODULE$APIBaseManager *)manager isCorrectWithCallBackData:(NSDictionary *)data{
    return $MODULE$APIManagerErrorTypeNoError;
}


@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", folder)

def generateDemos(module,folder):
    __generateDemoService(module,folder);
    __generateDemoApiManager(module,folder);