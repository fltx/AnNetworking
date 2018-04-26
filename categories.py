#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.append("..")
from _me_os import xxnetos;


def __generateDictionary(module,folder):
    selffolder = folder + "/NSDictionary"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "NSDictionary+$MODULE$NetworkingMethods"

    h_content = """//
//  NSDictionary+$MODULE$NetworkingMethods.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSDictionary ($MODULE$NetworkingMethods)

- (NSString *)$MODULE$_jsonString;

@end
"""
    m_content = """//
//  NSDictionary+$MODULE$NetworkingMethods.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "NSDictionary+$MODULE$NetworkingMethods.h"

@implementation NSDictionary ($MODULE$NetworkingMethods)

- (NSString *)$MODULE$_jsonString
{
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:self options:NSJSONWritingPrettyPrinted error:NULL];
    return [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
}

@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)



def __generateArray(module,folder):
    selffolder = folder + "/NSArray"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "NSArray+$MODULE$NetworkingMethods"

    h_content = """//
//  NSArray+$MODULE$NetworkingMethods.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSArray ($MODULE$NetworkingMethods)

- (NSString *)$MODULE$_jsonString;

@end
    """
    m_content = """//
//  NSArray+$MODULE$NetworkingMethods.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "NSArray+$MODULE$NetworkingMethods.h"

@implementation NSArray ($MODULE$NetworkingMethods)

/** 数组变json */
- (NSString *)$MODULE$_jsonString
{
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:self options:NSJSONWritingPrettyPrinted error:NULL];
    return [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
}


@end
    """
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)


def __generateString(module,folder):
    selffolder = folder + "/NSString"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "NSString+$MODULE$NetworkingMethods"
    h_content = """//
//  NSString+$MODULE$NetworkingMethods.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSString ($MODULE$NetworkingMethods)

- (NSString *)$MODULE$_MD5;
- (NSString *)$MODULE$_SHA1;
- (NSString *)$MODULE$_Base64Encode;

@end
        """
    m_content = """//
//  NSString+$MODULE$NetworkingMethods.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "NSString+$MODULE$NetworkingMethods.h"
#include <CommonCrypto/CommonDigest.h>
#import <CommonCrypto/CommonCryptor.h>
#import "NSObject+$MODULE$NetworkingMethods.h"


static char base64EncodingTable[64] = {
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/'
};

@implementation NSString ($MODULE$NetworkingMethods)

- (NSString *)$MODULE$_MD5
{
    NSData* inputData = [self dataUsingEncoding:NSUTF8StringEncoding];
    unsigned char outputData[CC_MD5_DIGEST_LENGTH];
    CC_MD5([inputData bytes], (unsigned int)[inputData length], outputData);
    
    NSMutableString* hashStr = [NSMutableString string];
    int i = 0;
    for (i = 0; i < CC_MD5_DIGEST_LENGTH; ++i)
        [hashStr appendFormat:@"%02x", outputData[i]];
    
    return hashStr;
}

- (NSString *)$MODULE$_SHA1
{
    const char *cstr = [self cStringUsingEncoding:NSUTF8StringEncoding];
    
    NSData *data = [NSData dataWithBytes:cstr length:self.length];
    //使用对应的CC_SHA1,CC_SHA256,CC_SHA384,CC_SHA512的长度分别是20,32,48,64
    uint8_t digest[CC_SHA1_DIGEST_LENGTH];
    //使用对应的CC_SHA256,CC_SHA384,CC_SHA512
    CC_SHA1(data.bytes, (unsigned int)data.length, digest);
    
    NSMutableString* output = [NSMutableString stringWithCapacity:CC_SHA1_DIGEST_LENGTH * 2];
    
    for(int i = 0; i < CC_SHA1_DIGEST_LENGTH; i++)
        [output appendFormat:@"%02x", digest[i]];
    
    return output;
}

- (NSString *)$MODULE$_Base64Encode
{
    NSData *rawData = [self dataUsingEncoding:NSUTF8StringEncoding];
    unsigned long ixtext, lentext;
    long ctremaining;
    unsigned char input[3], output[4];
    short i, charsonline = 0, ctcopy;
    const unsigned char *raw;
    NSMutableString *result;
    
    lentext = [self length];
    if (lentext < 1)
        return @"";
    result = [NSMutableString stringWithCapacity:lentext];
    raw = [rawData bytes];
    ixtext = 0;
    
    while (true) {
        ctremaining = lentext - ixtext;
        if (ctremaining <= 0)
            break;
        for (i = 0; i < 3; i++) {
            unsigned long ix = ixtext + i;
            if (ix < lentext)
                input[i] = raw[ix];
            else
                input[i] = 0;
        }
        output[0] = (input[0] & 0xFC) >> 2;
        output[1] = ((input[0] & 0x03) << 4) | ((input[1] & 0xF0) >> 4);
        output[2] = ((input[1] & 0x0F) << 2) | ((input[2] & 0xC0) >> 6);
        output[3] = input[2] & 0x3F;
        ctcopy = 4;
        switch (ctremaining) {
            case 1:
                ctcopy = 2;
                break;
            case 2:
                ctcopy = 3;
                break;
        }
        
        for (i = 0; i < ctcopy; i++)
            [result appendString: [NSString stringWithFormat:@"%c", base64EncodingTable[output[i]]]];
        
        for (i = ctcopy; i < 4; i++)
            [result appendString:@"="];
        
        ixtext += 3;
        charsonline += 4;
        
        if ((lentext > 0) && (charsonline >= lentext))
            charsonline = 0;
    }
    return result;
}

#pragma mark - private methods
- (int)char2Int:(char)c
{
    if (c >= 'A' && c <= 'Z') {
        return c - 65;
    } else if (c >= 'a' && c <= 'z') {
        return c - 97 + 26;
    } else if (c >= '0' && c <= '9') {
        return c - 48 + 26 + 26;
    } else {
        switch(c) {
            case '+':
                return 62;
            case '/':
                return 63;
            case '=':
                return 0;
            default:
                return -1;
        }
    }
}
@end
        """
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)



def __generateMutableString(module,folder):
    selffolder = folder + "/NSString"

    filename = "NSMutableString+$MODULE$NetworkingMethods"

    h_content = """//
//  NSMutableString+$MODULE$NetworkingMethods.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSMutableString ($MODULE$NetworkingMethods)

- (void)appendURLRequest:(NSURLRequest *)request;

@end
        """
    m_content = """//
//  NSMutableString+$MODULE$NetworkingMethods.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "NSMutableString+$MODULE$NetworkingMethods.h"
#import "NSObject+$MODULE$NetworkingMethods.h"
#import "NSURLRequest+$MODULE$NetworkingMethods.h"
#import "NSDictionary+$MODULE$NetworkingMethods.h"

@implementation NSMutableString ($MODULE$NetworkingMethods)

- (void)appendURLRequest:(NSURLRequest *)request
{
    [self appendFormat:@"\\n\\nHTTP URL:\\n\\t%@", request.URL];
    [self appendFormat:@"\\n\\nHTTP Header:\\n%@", request.allHTTPHeaderFields ? request.allHTTPHeaderFields : @"\\t\\t\\t\\t\\tN/A"];
    [self appendFormat:@"\\n\\nHTTP Origin Params:\\n\\t%@", request.originRequestParams.$MODULE$_jsonString];
    [self appendFormat:@"\\n\\nHTTP Actual Params:\\n\\t%@", request.actualRequestParams.$MODULE$_jsonString];
    [self appendFormat:@"\\n\\nHTTP Body:\\n\\t%@", [[[NSString alloc] initWithData:request.HTTPBody encoding:NSUTF8StringEncoding] $MODULE$_defaultValue:@"\\t\\t\\t\\tN/A"]];
    
    NSMutableString *headerString = [[NSMutableString alloc] init];
    [request.allHTTPHeaderFields enumerateKeysAndObjectsUsingBlock:^(NSString * _Nonnull key, NSString * _Nonnull obj, BOOL * _Nonnull stop) {
        NSString *header = [NSString stringWithFormat:@" -H \\"%@: %@\\"", key, obj];
        [headerString appendString:header];
    }];
    
    [self appendString:@"\\n\\nCURL:\\n\\t curl"];
    [self appendFormat:@" -X %@", request.HTTPMethod];
    
    if (headerString.length > 0) {
        [self appendString:headerString];
    }
    if (request.HTTPBody.length > 0) {
        [self appendFormat:@" -d '%@'", [[[NSString alloc] initWithData:request.HTTPBody encoding:NSUTF8StringEncoding] $MODULE$_defaultValue:@"\\t\\t\\t\\tN/A"]];
    }
    
    [self appendFormat:@" %@", request.URL];
}
@end
        """
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)



def __generateObject(module,folder):
    selffolder = folder + "/NSObject"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "NSObject+$MODULE$NetworkingMethods"

    h_content = """//
//  NSObject+$MODULE$NetworkingMethods.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSObject ($MODULE$NetworkingMethods)

- (id)$MODULE$_defaultValue:(id)defaultData;
- (BOOL)$MODULE$_isEmptyObject;

@end
    """
    m_content = """//
//  NSObject+$MODULE$NetworkingMethods.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "NSObject+$MODULE$NetworkingMethods.h"

@implementation NSObject ($MODULE$NetworkingMethods)

- (id)$MODULE$_defaultValue:(id)defaultData
{
    if (![defaultData isKindOfClass:[self class]]) {
        return defaultData;
    }
    
    if ([self $MODULE$_isEmptyObject]) {
        return defaultData;
    }
    
    return self;
}

- (BOOL)$MODULE$_isEmptyObject
{
    if ([self isEqual:[NSNull null]]) {
        return YES;
    }
    
    if ([self isKindOfClass:[NSString class]]) {
        if ([(NSString *)self length] == 0) {
            return YES;
        }
    }
    
    if ([self isKindOfClass:[NSArray class]]) {
        if ([(NSArray *)self count] == 0) {
            return YES;
        }
    }
    
    if ([self isKindOfClass:[NSDictionary class]]) {
        if ([(NSDictionary *)self count] == 0) {
            return YES;
        }
    }
    
    return NO;
}

@end
    """
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)

def __generateURLRequest(module,folder):
    selffolder = folder + "/NSURLRequest"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "NSURLRequest+$MODULE$NetworkingMethods"

    h_content = """//
//  NSURLRequest+CTNetworkingMethods.h
//  RTNetworking
//
//  Created by casa on 14-5-26.
//  Copyright (c) 2014年 casatwy. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$ServiceProtocol.h"

@interface NSURLRequest ($MODULE$NetworkingMethods)

@property (nonatomic, copy) NSDictionary *actualRequestParams;
@property (nonatomic, copy) NSDictionary *originRequestParams;
@property (nonatomic, strong) id <$MODULE$ServiceProtocol> service;

@end
        """
    m_content = """//
//  NSURLRequest+CTNetworkingMethods.m
//  RTNetworking
//
//  Created by casa on 14-5-26.
//  Copyright (c) 2014年 casatwy. All rights reserved.
//

#import "NSURLRequest+$MODULE$NetworkingMethods.h"
#import <objc/runtime.h>

static void *CTNetworkingActualRequestParams = &CTNetworkingActualRequestParams;
static void *CTNetworkingOriginRequestParams = &CTNetworkingOriginRequestParams;
static void *CTNetworkingRequestService = &CTNetworkingRequestService;

@implementation NSURLRequest ($MODULE$NetworkingMethods)

- (void)setActualRequestParams:(NSDictionary *)actualRequestParams
{
    objc_setAssociatedObject(self, CTNetworkingActualRequestParams, actualRequestParams, OBJC_ASSOCIATION_COPY);
}

- (NSDictionary *)actualRequestParams
{
    return objc_getAssociatedObject(self, CTNetworkingActualRequestParams);
}

- (void)setOriginRequestParams:(NSDictionary *)originRequestParams
{
    objc_setAssociatedObject(self, CTNetworkingOriginRequestParams, originRequestParams, OBJC_ASSOCIATION_COPY);
}

- (NSDictionary *)originRequestParams
{
    return objc_getAssociatedObject(self, CTNetworkingOriginRequestParams);
}

- (void)setService:(id<$MODULE$ServiceProtocol>)service
{
    objc_setAssociatedObject(self, CTNetworkingRequestService, service, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
}

- (id<$MODULE$ServiceProtocol>)service
{
    return objc_getAssociatedObject(self, CTNetworkingRequestService);
}

@end
        """
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)






def generateCategories(module,folder):
    subfolder = folder.rstrip("\\") + "/Categories"

    __generateDictionary(module,subfolder);
    __generateArray(module,subfolder);

    __generateString(module,subfolder);
    __generateMutableString(module,subfolder);

    __generateObject(module,subfolder);
    __generateURLRequest(module,subfolder);
