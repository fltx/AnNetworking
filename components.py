#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.append("..")
from _me_os import xxnetos;

def __generateURLResponse(module,folder):
    selffolder = folder + "/URLResponse"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "$MODULE$URLResponse"

    h_content = """//
//  AXURLResponse.h
//  RTNetworking
//
//  Created by casa on 14-5-18.
//  Copyright (c) 2014年 casatwy. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, $MODULE$URLResponseStatus)
{
    $MODULE$URLResponseStatusSuccess, //作为底层，请求是否成功只考虑是否成功收到服务器反馈。至于签名是否正确，返回的数据是否完整，由上层的$MODULE$APIBaseManager来决定。
    $MODULE$URLResponseStatusErrorTimeout,
    $MODULE$URLResponseStatusErrorCancel,
    $MODULE$URLResponseStatusErrorNoNetwork // 默认除了超时以外的错误都是无网络错误。
};

@interface $MODULE$URLResponse : NSObject

@property (nonatomic, assign, readonly) $MODULE$URLResponseStatus status;
@property (nonatomic, copy, readonly) NSString *contentString;
@property (nonatomic, copy, readonly) NSDictionary *content;
@property (nonatomic, assign, readonly) NSInteger requestId;
@property (nonatomic, copy, readonly) NSURLRequest *request;
@property (nonatomic, copy, readonly) NSData *responseData;
@property (nonatomic, strong, readonly) NSString *errorMessage;

@property (nonatomic, copy) NSDictionary *acturlRequestParams;
@property (nonatomic, copy) NSDictionary *originRequestParams;
@property (nonatomic, strong) NSString *logString;

@property (nonatomic, assign, readonly) BOOL isCache;

- (instancetype)initWithResponseString:(NSString *)responseString requestId:(NSNumber *)requestId request:(NSURLRequest *)request responseContent:(NSDictionary *)responseContent error:(NSError *)error;

// 使用initWithData的response，它的isCache是YES，上面两个函数生成的response的isCache是NO
- (instancetype)initWithData:(NSData *)data;

@end
"""
    m_content = """//
//  AXURLResponse.m
//  RTNetworking
//
//  Created by casa on 14-5-18.
//  Copyright (c) 2014年 casatwy. All rights reserved.
//

#import "$MODULE$URLResponse.h"
#import "NSObject+$MODULE$NetworkingMethods.h"
#import "NSURLRequest+$MODULE$NetworkingMethods.h"

@interface $MODULE$URLResponse ()

@property (nonatomic, assign, readwrite) $MODULE$URLResponseStatus status;
@property (nonatomic, copy, readwrite) NSString *contentString;
@property (nonatomic, copy, readwrite) id content;
@property (nonatomic, copy, readwrite) NSURLRequest *request;
@property (nonatomic, assign, readwrite) NSInteger requestId;
@property (nonatomic, copy, readwrite) NSData *responseData;
@property (nonatomic, assign, readwrite) BOOL isCache;
@property (nonatomic, strong, readwrite) NSString *errorMessage;

@end

@implementation $MODULE$URLResponse

#pragma mark - life cycle
- (instancetype)initWithResponseString:(NSString *)responseString requestId:(NSNumber *)requestId request:(NSURLRequest *)request responseContent:(NSDictionary *)responseContent error:(NSError *)error
{
    self = [super init];
    if (self) {
        self.contentString = [responseString $MODULE$_defaultValue:@""];
        self.requestId = [requestId integerValue];
        self.request = request;
        self.acturlRequestParams = request.actualRequestParams;
        self.originRequestParams = request.originRequestParams;
        self.isCache = NO;
        self.status = [self responseStatusWithError:error];
        self.content = responseContent ? responseContent : @{};
        self.errorMessage = [NSString stringWithFormat:@"%@", error];
    }
    return self;
}

- (instancetype)initWithData:(NSData *)data
{
    self = [super init];
    if (self) {
        self.contentString = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
        self.status = [self responseStatusWithError:nil];
        self.requestId = 0;
        self.request = nil;
        self.responseData = data;
        self.content = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingMutableContainers error:NULL];
        self.isCache = YES;
    }
    return self;
}

#pragma mark - private methods
- ($MODULE$URLResponseStatus)responseStatusWithError:(NSError *)error
{
    if (error) {
        $MODULE$URLResponseStatus result = $MODULE$URLResponseStatusErrorNoNetwork;
        
        // 除了超时以外，所有错误都当成是无网络
        if (error.code == NSURLErrorTimedOut) {
            result = $MODULE$URLResponseStatusErrorTimeout;
        }
        if (error.code == NSURLErrorCancelled) {
            result = $MODULE$URLResponseStatusErrorCancel;
        }
        if (error.code == NSURLErrorNotConnectedToInternet) {
            result = $MODULE$URLResponseStatusErrorNoNetwork;
        }
        return result;
    } else {
        return $MODULE$URLResponseStatusSuccess;
    }
}

#pragma mark - getters and setters
- (NSData *)responseData
{
    if (_responseData == nil) {
        NSError *error = nil;
        _responseData = [NSJSONSerialization dataWithJSONObject:self.content options:0 error:&error];
        if (error) {
            _responseData = [@"" dataUsingEncoding:NSUTF8StringEncoding];
        }
    }
    return _responseData;
}

@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)

def __generateAPIProxy(module,folder):
    selffolder = folder + "/APIProxy"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "$MODULE$APIProxy"

    h_content = """//
//  $MODULE$APIProxy.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$NetworkingDefines.h"

typedef void(^$MODULE$Callback)($MODULE$URLResponse *response);

@interface $MODULE$ApiProxy : NSObject

$MODULE$_SINGLETON_DEF($MODULE$ApiProxy);

- (NSNumber *)callApiWithRequest:(NSURLRequest *)request success:($MODULE$Callback)success fail:($MODULE$Callback)fail;
- (void)cancelRequestWithRequestID:(NSNumber *)requestID;
- (void)cancelRequestWithRequestIDList:(NSArray *)requestIDList;


@end
"""
    m_content = """//
//  $MODULE$APIProxy.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "$MODULE$APIProxy.h"
#import <AFNetworking/AFNetworking.h>
#import "$MODULE$URLResponse.h"
#import "$MODULE$Logger.h"
#import "$MODULE$ServiceFactory.h"
#import "NSURLRequest+$MODULE$NetworkingMethods.h"
#import "NSString+$MODULE$NetworkingMethods.h"
#import "NSObject+$MODULE$NetworkingMethods.h"

static NSString * const kAXApiProxyDispatchItemKeyCallbackSuccess = @"kAXApiProxyDispatchItemCallbackSuccess";
static NSString * const kAXApiProxyDispatchItemKeyCallbackFail = @"kAXApiProxyDispatchItemCallbackFail";

NSString * const k$MODULE$ApiProxyValidateResultKeyResponseJSONObject = @"k$MODULE$ApiProxyValidateResultKeyResponseJSONObject";
NSString * const k$MODULE$ApiProxyValidateResultKeyResponseJSONString = @"k$MODULE$ApiProxyValidateResultKeyResponseJSONString";
NSString * const k$MODULE$ApiProxyValidateResultKeyResponseData = @"k$MODULE$ApiProxyValidateResultKeyResponseData";

@interface $MODULE$ApiProxy ()

@property (nonatomic, strong) NSMutableDictionary *dispatchTable;
@property (nonatomic, strong) NSNumber *recordedRequestId;
@property (nonatomic, strong) AFHTTPSessionManager *sessionManager;

@end
@implementation $MODULE$ApiProxy

$MODULE$_SINGLETON_IMP($MODULE$ApiProxy);

#pragma mark - getters and setters
- (NSMutableDictionary *)dispatchTable
{
    if (_dispatchTable == nil) {
        _dispatchTable = [[NSMutableDictionary alloc] init];
    }
    return _dispatchTable;
}

- (AFHTTPSessionManager *)sessionManager
{
    if (_sessionManager == nil) {
        _sessionManager = [AFHTTPSessionManager manager];
        _sessionManager.responseSerializer = [AFHTTPResponseSerializer serializer];
        _sessionManager.securityPolicy.allowInvalidCertificates = YES;
        _sessionManager.securityPolicy.validatesDomainName = NO;
    }
    return _sessionManager;
}


#pragma mark - public methods
- (void)cancelRequestWithRequestID:(NSNumber *)requestID
{
    NSURLSessionDataTask *requestOperation = self.dispatchTable[requestID];
    [requestOperation cancel];
    [self.dispatchTable removeObjectForKey:requestID];
}

- (void)cancelRequestWithRequestIDList:(NSArray *)requestIDList
{
    for (NSNumber *requestId in requestIDList) {
        [self cancelRequestWithRequestID:requestId];
    }
}

/** 这个函数存在的意义在于，如果将来要把AFNetworking换掉，只要修改这个函数的实现即可。 */
- (NSNumber *)callApiWithRequest:(NSURLRequest *)request success:($MODULE$Callback)success fail:($MODULE$Callback)fail
{
    // 跑到这里的block的时候，就已经是主线程了。
    __block NSURLSessionDataTask *dataTask = nil;
    void (^completionHandler)(NSURLResponse *response, id _Nullable responseObject,  NSError * _Nullable error) = ^(NSURLResponse * _Nonnull response, NSData * _Nullable responseData, NSError * _Nullable error) {
        NSNumber *requestID = @([dataTask taskIdentifier]);
        [self.dispatchTable removeObjectForKey:requestID];
        
        NSDictionary *result = [request.service resultWithResponseData:responseData response:response request:request error:&error];
        // 输出返回数据
        $MODULE$URLResponse *$MODULE$Response = [[$MODULE$URLResponse alloc] initWithResponseString:result[k$MODULE$ApiProxyValidateResultKeyResponseJSONString]
                                                                        requestId:requestID
                                                                          request:request
                                                                  responseContent:result[k$MODULE$ApiProxyValidateResultKeyResponseJSONObject]
                                                                            error:error];
        
        $MODULE$Response.logString = [$MODULE$Logger logDebugInfoWithResponse:(NSHTTPURLResponse *)response
                                                  rawResponseData:responseData
                                                   responseString:result[k$MODULE$ApiProxyValidateResultKeyResponseJSONString]
                                                          request:request
                                                            error:error];
        
        if (error) {
            fail?fail($MODULE$Response):nil;
        } else {
            success?success($MODULE$Response):nil;
        }
    };
    dataTask = [self.sessionManager dataTaskWithRequest:request
                                         uploadProgress:nil
                                       downloadProgress:nil
                                      completionHandler:completionHandler];
    NSNumber *requestId = @([dataTask taskIdentifier]);
    
    self.dispatchTable[requestId] = dataTask;
    [dataTask resume];
    
    return requestId;
}



@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)
def __generateGroupRequest(module, folder):
    selffolder = folder + "/APIProxy"

    filename = "$MODULE$GroupRequest"

    h_content = """//
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/26.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$APIProxy.h"

@interface $MODULE$GroupRequest : NSObject
- (instancetype)init NS_UNAVAILABLE;
- (instancetype)initWithURLRequest:(NSURLRequest *)request;
- ($MODULE$GroupRequest *(^)(NSURLRequest *req))link;
/**迭代器
 */
- (void)resetIndex;
- (NSURLRequest *)nextUrlRequest;


/**给个机会重置参数
 返回值： 根据response 期望的下一级request
 */
@property (nonatomic,copy) NSURLRequest *(^aRequestSuccess)($MODULE$URLResponse *response,NSURLRequest *request);
@property (nonatomic,copy) void(^aRequestFailure)($MODULE$URLResponse *response,NSURLRequest *request);
- ($MODULE$URLResponse *)responseOfCacheForRequest:(NSURLRequest *)request;
- (void)cleanCache;

@end

@interface $MODULE$ApiProxy (ApiLinker)
- (void)callApiWithGroupRequest:($MODULE$GroupRequest *)request success:($MODULE$Callback)success fail:($MODULE$Callback)fail;
- (void)cancleGroupRequest:($MODULE$GroupRequest *)request;
@end

"""
    m_content = """//
//  $MODULE$ApiLinker.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/26.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "$MODULE$GroupRequest.h"
#import "$MODULE$URLResponse.h"


@interface __$MODULE$GroupRequestTuple: NSObject{
    @package NSNumber *_taskID;
}
@property (nonatomic,strong) NSURLRequest *request;
@property (nonatomic,strong) $MODULE$URLResponse *response;
@end

@implementation __$MODULE$GroupRequestTuple
@end
@interface $MODULE$GroupRequest()
@property (nonatomic,strong) NSMutableArray<__$MODULE$GroupRequestTuple *> *req_respTable;
@property (nonatomic,assign) int iterationIndex;
@end
@implementation $MODULE$GroupRequest
- (instancetype)initWithURLRequest:(NSURLRequest *)request
{
    if (!(self = [super init])) return self;
    self.link(request);
    self.iterationIndex = -1;
    return self;
}
- ($MODULE$GroupRequest *(^)(NSURLRequest *))link
{
    __weak typeof(self) self_weak = self;
    return ^(NSURLRequest *req){
        __strong typeof(self_weak) self_strong = self_weak;
        __$MODULE$GroupRequestTuple *tuple = [[__$MODULE$GroupRequestTuple alloc] init];
        tuple.request = req.copy;
        [self_strong.req_respTable addObject:tuple];
        return self_strong;
    };
}
- (void)resetIndex
{
    self.iterationIndex = -1;
}
- (NSURLRequest *)nextUrlRequest
{
    int index = self.iterationIndex + 1;
    if (index >= self.req_respTable.count){
        return nil;
    }
    NSURLRequest *result = [self.req_respTable[index] request];
    if (result){
        self.iterationIndex = index;
    }
    return result;
}

- ($MODULE$URLResponse *)responseOfCacheForRequest:(NSURLRequest *)request
{
    for (__$MODULE$GroupRequestTuple *tuple in self.req_respTable) {
        if ([tuple isEqual:request]){
            return tuple.response;
        }
    }
    return nil;
}

- (void)cleanCache
{
    for (__$MODULE$GroupRequestTuple *tuple in self.req_respTable) {
        if (tuple.response){
            tuple.response = nil;
            tuple->_taskID = nil;
        }
    }
}


- (void)__resetTaskID:(NSNumber *)taskID forRequese:(NSURLRequest *)urlRequest{
    for (__$MODULE$GroupRequestTuple *tuple in self.req_respTable) {
        if ([tuple isEqual:urlRequest]){
            tuple->_taskID = taskID;
            return;
        }
    }
}

- (NSMutableArray<__$MODULE$GroupRequestTuple *> *)req_respTable{
    if (!_req_respTable) {
        _req_respTable = @[].mutableCopy;
    }
    return _req_respTable;
}
@end

@implementation $MODULE$ApiProxy (ApiLinker)

/**
 递归 出队 urlrequest
 */
- (void)callApiWithGroupRequest:($MODULE$GroupRequest *)request success:($MODULE$Callback)success fail:($MODULE$Callback)fail
{
    NSURLRequest *aReq = [request nextUrlRequest];
    if (aReq == nil){
        return;
    }
    $MODULE$Callback linkSuccess = ^($MODULE$URLResponse *response){
        if (request.aRequestSuccess){
            request.aRequestSuccess(response,aReq);
        }
        [self callApiWithGroupRequest:request success:success fail:fail];
    };
    $MODULE$Callback linkFail = ^($MODULE$URLResponse *response){
        if (request.aRequestFailure){
            request.aRequestFailure(response,aReq);
        }
        if (fail){fail(response);}
    };
    
    $MODULE$URLResponse *aResp = [request responseOfCacheForRequest:aReq];
    if (aResp && aResp.status == $MODULE$URLResponseStatusSuccess){
        linkSuccess(aResp);
    }else{
        NSNumber *taskID = [self callApiWithRequest:aReq success:linkSuccess fail:linkFail];
        [request __resetTaskID:taskID forRequese:aReq];
    }
}

- (void)cancleGroupRequest:($MODULE$GroupRequest *)request
{
    for (__$MODULE$GroupRequestTuple *tuple in request.req_respTable) {
        if (tuple->_taskID){
            [self cancelRequestWithRequestID:tuple->_taskID];
        }
    }
}
@end

"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)



def __generateLog(module,folder):
    selffolder = folder + "/Log"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "$MODULE$Logger"

    h_content = """//
//  $MODULE$Logger.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$URLResponse.h"
#import "$MODULE$ServiceProtocol.h"

@interface $MODULE$Logger : NSObject

+ (NSString *)logDebugInfoWithRequest:(NSURLRequest *)request apiName:(NSString *)apiName service:(id <$MODULE$ServiceProtocol>)service;
+ (NSString *)logDebugInfoWithResponse:(NSHTTPURLResponse *)response rawResponseData:(NSData *)rawResponseData responseString:(NSString *)responseString request:(NSURLRequest *)request error:(NSError *)error;
+ (NSString *)logDebugInfoWithCachedResponse:($MODULE$URLResponse *)response methodName:(NSString *)methodName service:(id <$MODULE$ServiceProtocol>)service params:(NSDictionary *)params;

@end
"""
    m_content = """//
//  $MODULE$Logger.m
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#import "$MODULE$Logger.h"
#import "NSObject+$MODULE$NetworkingMethods.h"
#import "NSMutableString+$MODULE$NetworkingMethods.h"
#import "NSArray+$MODULE$NetworkingMethods.h"
#import "NSURLRequest+$MODULE$NetworkingMethods.h"
#import "NSDictionary+$MODULE$NetworkingMethods.h"

@implementation $MODULE$Logger

+ (NSString *)logDebugInfoWithRequest:(NSURLRequest *)request apiName:(NSString *)apiName service:(id <$MODULE$ServiceProtocol>)service
{
    NSMutableString *logString = nil;
#ifdef DEBUG
//    if ([$MODULE$Mediator sharedInstance].$MODULE$Networking_shouldPrintNetworkingLog == NO) {
//        return @"";
//    }
    
    $MODULE$ServiceAPIEnvironment enviroment = request.service.apiEnvironment;
    NSString *enviromentString = nil;
    if (enviroment == $MODULE$ServiceAPIEnvironmentDevelop) {
        enviromentString = @"Develop";
    }
    if (enviroment == $MODULE$ServiceAPIEnvironmentReleaseCandidate) {
        enviromentString = @"Pre Release";
    }
    if (enviroment == $MODULE$ServiceAPIEnvironmentRelease) {
        enviromentString = @"Release";
    }
    
    logString = [NSMutableString stringWithString:@"\\n\\n********************************************************\\nRequest Start\\n********************************************************\\n\\n"];
    
    [logString appendFormat:@"API Name:\\t\\t%@\\n", [apiName $MODULE$_defaultValue:@"N/A"]];
    [logString appendFormat:@"Method:\\t\\t\\t%@\\n", request.HTTPMethod];
    [logString appendFormat:@"Service:\\t\\t%@\\n", [service class]];
    [logString appendFormat:@"Status:\\t\\t\\t%@\\n", enviromentString];
    [logString appendURLRequest:request];
    
    [logString appendFormat:@"\\n\\n********************************************************\\nRequest End\\n********************************************************\\n\\n\\n\\n"];
    NSLog(@"%@", logString);
#endif
    return logString;
}

+ (NSString *)logDebugInfoWithResponse:(NSHTTPURLResponse *)response rawResponseData:(NSData *)rawResponseData responseString:(NSString *)responseString request:(NSURLRequest *)request error:(NSError *)error
{
    NSMutableString *logString = nil;
#ifdef DEBUG
//    if ([$MODULE$Mediator sharedInstance].$MODULE$Networking_shouldPrintNetworkingLog == NO) {
//        return @"";
//    }
    
    BOOL isSuccess = error ? NO : YES;
    
    logString = [NSMutableString stringWithString:@"\\n\\n=========================================\\nAPI Response\\n=========================================\\n\\n"];
    
    [logString appendFormat:@"Status:\\t%ld\\t(%@)\\n\\n", (long)response.statusCode, [NSHTTPURLResponse localizedStringForStatusCode:response.statusCode]];
    [logString appendFormat:@"Content:\\n\\t%@\\n\\n", responseString];
    [logString appendFormat:@"Request URL:\\n\\t%@\\n\\n", request.URL];
    [logString appendFormat:@"Request Data:\\n\\t%@\\n\\n",request.originRequestParams.$MODULE$_jsonString];
    [logString appendFormat:@"Raw Response String:\\n\\t%@\\n\\n", [[NSString alloc] initWithData:rawResponseData encoding:NSUTF8StringEncoding]];
    [logString appendFormat:@"Raw Response Header:\\n\\t%@\\n\\n", response.allHeaderFields];
    if (isSuccess == NO) {
        [logString appendFormat:@"Error Domain:\\t\\t\\t\\t\\t\\t\\t%@\\n", error.domain];
        [logString appendFormat:@"Error Domain Code:\\t\\t\\t\\t\\t\\t%ld\\n", (long)error.code];
        [logString appendFormat:@"Error Localized Description:\\t\\t\\t%@\\n", error.localizedDescription];
        [logString appendFormat:@"Error Localized Failure Reason:\\t\\t\\t%@\\n", error.localizedFailureReason];
        [logString appendFormat:@"Error Localized Recovery Suggestion:\\t%@\\n\\n", error.localizedRecoverySuggestion];
    }
    
    [logString appendString:@"\\n---------------  Related Request Content  --------------\\n"];
    
    [logString appendURLRequest:request];
    
    [logString appendFormat:@"\\n\\n=========================================\\nResponse End\\n=========================================\\n\\n"];
    
    NSLog(@"%@", logString);
#endif
    
    return logString;
}

+(NSString *)logDebugInfoWithCachedResponse:($MODULE$URLResponse *)response methodName:(NSString *)methodName service:(id <$MODULE$ServiceProtocol>)service params:(NSDictionary *)params
{
    NSMutableString *logString = nil;
#ifdef DEBUG
//    if ([$MODULE$Mediator sharedInstance].$MODULE$Networking_shouldPrintNetworkingLog == NO) {
//        return @"";
//    }
    
    logString = [NSMutableString stringWithString:@"\\n\\n=========================================\\nCached Response                             \\n=========================================\\n\\n"];
    
    [logString appendFormat:@"API Name:\\t\\t%@\\n", [methodName $MODULE$_defaultValue:@"N/A"]];
    [logString appendFormat:@"Service:\\t\\t%@\\n", [service class]];
    [logString appendFormat:@"Method Name:\\t%@\\n", methodName];
    [logString appendFormat:@"Params:\\n%@\\n\\n", params];
    [logString appendFormat:@"Origin Params:\\n%@\\n\\n", response.originRequestParams];
    [logString appendFormat:@"A$MODULE$ual Params:\\n%@\\n\\n", response.acturlRequestParams];
    [logString appendFormat:@"Content:\\n\\t%@\\n\\n", response.contentString];
    
    [logString appendFormat:@"\\n\\n=========================================\\nResponse End\\n=========================================\\n\\n"];
    NSLog(@"%@", logString);
#endif
    
    return logString;
}

@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)

def __generateAPIBaseManager(module,folder):
    selffolder = folder + "/APIBaseManager"
    if xxnetos.mkdir(selffolder) == False:
        return False;

    filename = "$MODULE$APIBaseManager"

    h_content = """//
//  AJKBaseManager.h
//  casatwy2
//
//  Created by casa on 13-12-2.
//  Copyright (c) 2013年 casatwy inc. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "$MODULE$URLResponse.h"
#import "$MODULE$NetworkingDefines.h"

@interface $MODULE$APIBaseManager : NSObject <NSCopying>

// outter functions
@property (nonatomic, weak) id <$MODULE$APIManagerCallBackDelegate> _Nullable delegate;
@property (nonatomic, weak) id <$MODULE$APIManagerParamSource> _Nullable paramSource;
@property (nonatomic, weak) id <$MODULE$APIManagerValidator> _Nullable validator;
@property (nonatomic, weak) NSObject<$MODULE$APIManager> * _Nullable child; //里面会调用到NSObject的方法，所以这里不用id
@property (nonatomic, weak) id <$MODULE$APIManagerInterceptor> _Nullable interceptor;


// response
@property (nonatomic, strong) $MODULE$URLResponse * _Nonnull response;
@property (nonatomic, readonly) $MODULE$APIManagerErrorType errorType;
@property (nonatomic, copy, readonly) NSString * _Nullable errorMessage;

// before loading
@property (nonatomic, assign, readonly) BOOL isReachable;
@property (nonatomic, assign, readonly) BOOL isLoading;

// start
- (NSInteger)loadData;
+ (NSInteger)loadDataWithParams:(NSDictionary * _Nullable)params success:(void (^ _Nullable)($MODULE$APIBaseManager * _Nonnull apiManager))successCallback fail:(void (^ _Nullable)($MODULE$APIBaseManager * _Nonnull apiManager))failCallback;

// cancel
- (void)cancelAllRequests;
- (void)cancelRequestWithRequestId:(NSInteger)requestID;

// finish
- (id _Nullable )fetchDataWithReformer:(id <$MODULE$APIManagerDataReformer> _Nullable)reformer;
- (void)cleanData;

@end

@interface $MODULE$APIBaseManager (InnerInterceptor)

- (BOOL)beforePerformSuccessWithResponse:($MODULE$URLResponse *_Nullable)response;
- (void)afterPerformSuccessWithResponse:($MODULE$URLResponse *_Nullable)response;

- (BOOL)beforePerformFailWithResponse:($MODULE$URLResponse *_Nullable)response;
- (void)afterPerformFailWithResponse:($MODULE$URLResponse *_Nullable)response;

- (BOOL)shouldCallAPIWithParams:(NSDictionary *_Nullable)params;
- (void)afterCallingAPIWithParams:(NSDictionary *_Nullable)params;

@end

"""
    m_content = """//
//  AJKBaseManager.m
//  casatwy2
//
//  Created by casa on 13-12-2.
//  Copyright (c) 2013年 casatwy inc. All rights reserved.
//

#import "$MODULE$APIBaseManager.h"
#import "NSURLRequest+$MODULE$NetworkingMethods.h"
#import "$MODULE$Logger.h"
#import "$MODULE$ServiceFactory.h"
#import "$MODULE$ApiProxy.h"


NSString * const k$MODULE$UserTokenInvalidNotification = @"k$MODULE$UserTokenInvalidNotification";
NSString * const k$MODULE$UserTokenIllegalNotification = @"k$MODULE$UserTokenIllegalNotification";

NSString * const k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue = @"k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue";
NSString * const k$MODULE$APIBaseManagerRequestID = @"k$MODULE$APIBaseManagerRequestID";


@interface $MODULE$APIBaseManager ()

@property (nonatomic, strong, readwrite) id fetchedRawData;
@property (nonatomic, assign, readwrite) BOOL isLoading;
@property (nonatomic, copy, readwrite) NSString *errorMessage;

@property (nonatomic, readwrite) $MODULE$APIManagerErrorType errorType;
@property (nonatomic, strong) NSMutableArray *requestIdList;

@property (nonatomic, strong, nullable) void (^successBlock)($MODULE$APIBaseManager *apimanager);
@property (nonatomic, strong, nullable) void (^failBlock)($MODULE$APIBaseManager *apimanager);

@end

@implementation $MODULE$APIBaseManager

#pragma mark - life cycle
- (instancetype)init
{
    self = [super init];
    if (self) {
        _delegate = nil;
        _validator = nil;
        _paramSource = nil;
        
        _fetchedRawData = nil;
        
        _errorMessage = nil;
        _errorType = $MODULE$APIManagerErrorTypeDefault;

        
        if ([self conformsToProtocol:@protocol($MODULE$APIManager)]) {
            self.child = (id <$MODULE$APIManager>)self;
        } else {
            NSException *exception = [[NSException alloc] init];
            @throw exception;
        }
    }
    return self;
}

- (void)dealloc
{
    [self cancelAllRequests];
    self.requestIdList = nil;
}

#pragma mark - NSCopying
- (id)copyWithZone:(NSZone *)zone
{
    return self;
}

#pragma mark - public methods
- (void)cancelAllRequests
{
    [[$MODULE$ApiProxy sharedInstance] cancelRequestWithRequestIDList:self.requestIdList];
    [self.requestIdList removeAllObjects];
}

- (void)cancelRequestWithRequestId:(NSInteger)requestID
{
    [self removeRequestIdWithRequestID:requestID];
    [[$MODULE$ApiProxy sharedInstance] cancelRequestWithRequestID:@(requestID)];
}

- (id)fetchDataWithReformer:(id<$MODULE$APIManagerDataReformer>)reformer
{
    id resultData = nil;
    if ([reformer respondsToSelector:@selector(manager:reformData:)]) {
        resultData = [reformer manager:self reformData:self.fetchedRawData];
    } else {
        resultData = [self.fetchedRawData mutableCopy];
    }
    return resultData;
}

#pragma mark - calling api
- (NSInteger)loadData
{
    NSDictionary *params = [self.paramSource paramsForApi:self];
    NSInteger requestId = [self loadDataWithParams:params];
    return requestId;
}

+ (NSInteger)loadDataWithParams:(NSDictionary *)params success:(void (^)($MODULE$APIBaseManager *))successCallback fail:(void (^)($MODULE$APIBaseManager *))failCallback
{
    return [[[self alloc] init] loadDataWithParams:params success:successCallback fail:failCallback];
}

- (NSInteger)loadDataWithParams:(NSDictionary *)params success:(void (^)($MODULE$APIBaseManager *))successCallback fail:(void (^)($MODULE$APIBaseManager *))failCallback
{
    self.successBlock = successCallback;
    self.failBlock = failCallback;

    return [self loadDataWithParams:params];
}

- (NSInteger)loadDataWithParams:(NSDictionary *)params
{
    NSInteger requestId = 0;
    NSDictionary *reformedParams = [self reformParams:params];
    if (reformedParams == nil) {
        reformedParams = @{};
    }
    if ([self shouldCallAPIWithParams:reformedParams]) {
        $MODULE$APIManagerErrorType errorType = [self.validator manager:self isCorrectWithParamsData:reformedParams];
        if (errorType == $MODULE$APIManagerErrorTypeNoError) {
            
            $MODULE$URLResponse *response = nil;
            // 先检查一下是否有内存缓存
            // 再检查是否有磁盘缓存
            //为什么要缓存???
            if (response != nil) {
                [self successedOnCallingAPI:response];
                return 0;
            }
            
            // 实际的网络请求
            if ([self isReachable]) {
                self.isLoading = YES;
                
                id <$MODULE$ServiceProtocol> service = [[$MODULE$ServiceFactory sharedInstance] serviceWithIdentifier:self.child.serviceIdentifier];
                NSURLRequest *request = [service requestWithParams:reformedParams methodName:self.child.methodName requestType:self.child.requestType];
                request.service = service;
                [$MODULE$Logger logDebugInfoWithRequest:request apiName:self.child.methodName service:service];
                
                NSNumber *requestId = [[$MODULE$ApiProxy sharedInstance] callApiWithRequest:request success:^($MODULE$URLResponse *response) {
                    [self successedOnCallingAPI:response];
                } fail:^($MODULE$URLResponse *response) {
                    $MODULE$APIManagerErrorType errorType = $MODULE$APIManagerErrorTypeDefault;
                    if (response.status == $MODULE$URLResponseStatusErrorCancel) {
                        errorType = $MODULE$APIManagerErrorTypeCanceled;
                    }
                    if (response.status == $MODULE$URLResponseStatusErrorTimeout) {
                        errorType = $MODULE$APIManagerErrorTypeTimeout;
                    }
                    if (response.status == $MODULE$URLResponseStatusErrorNoNetwork) {
                        errorType = $MODULE$APIManagerErrorTypeNoNetWork;
                    }
                    [self failedOnCallingAPI:response withErrorType:errorType];
                }];
                [self.requestIdList addObject:requestId];
                
                NSMutableDictionary *params = [reformedParams mutableCopy];
                params[k$MODULE$APIBaseManagerRequestID] = requestId;
                [self afterCallingAPIWithParams:params];
                return [requestId integerValue];
            
            } else {
                [self failedOnCallingAPI:nil withErrorType:$MODULE$APIManagerErrorTypeNoNetWork];
                return requestId;
            }
        } else {
            [self failedOnCallingAPI:nil withErrorType:errorType];
            return requestId;
        }
    }
    return requestId;
}

#pragma mark - api callbacks
- (void)successedOnCallingAPI:($MODULE$URLResponse *)response
{

    self.isLoading = NO;
    self.response = response;
    
    if (response.content) {
        self.fetchedRawData = [response.content copy];
    } else {
        self.fetchedRawData = [response.responseData copy];
    }
    
    [self removeRequestIdWithRequestID:response.requestId];
    
    $MODULE$APIManagerErrorType errorType = [self.validator manager:self isCorrectWithCallBackData:response.content];
    if (errorType == $MODULE$APIManagerErrorTypeNoError) {
        
        //先缓存???
        
        if ([self.interceptor respondsToSelector:@selector(manager:didReceiveResponse:)]) {
            [self.interceptor manager:self didReceiveResponse:response];
        }
        if ([self beforePerformSuccessWithResponse:response]) {
            dispatch_async(dispatch_get_main_queue(), ^{
                if ([self.delegate respondsToSelector:@selector(managerCallAPIDidSuccess:)]) {
                    [self.delegate managerCallAPIDidSuccess:self];
                }
                if (self.successBlock) {
                    self.successBlock(self);
                }
            });
        }
        [self afterPerformSuccessWithResponse:response];
    } else {
        [self failedOnCallingAPI:response withErrorType:errorType];
    }
}

- (void)failedOnCallingAPI:($MODULE$URLResponse *)response withErrorType:($MODULE$APIManagerErrorType)errorType
{
    self.isLoading = NO;
    if (response) {
        self.response = response;
    }
    self.errorType = errorType;
    [self removeRequestIdWithRequestID:response.requestId];

        // user token 无效，重新登录
        if (errorType == $MODULE$APIManagerErrorTypeNeedLogin) {
            [[NSNotificationCenter defaultCenter] postNotificationName:k$MODULE$UserTokenIllegalNotification
                                                                object:nil
                                                              userInfo:@{
                                                                         k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue:self
                                                                         }];
            return;
        }

        NSString *resCode = [NSString stringWithFormat:@"%@", response.content[@"resCode"]];
        if ([resCode isEqualToString:@"00100009"]
            || [resCode isEqualToString:@"05111001"]
            || [resCode isEqualToString:@"05111002"]
            || [resCode isEqualToString:@"1080002"]
            ) {
            [[NSNotificationCenter defaultCenter] postNotificationName:k$MODULE$UserTokenIllegalNotification
                                                                object:nil
                                                              userInfo:@{
                                                                         k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue:self
                                                                         }];
            return;
        }

    // 可以自动处理的错误
    if (errorType == $MODULE$APIManagerErrorTypeNeedAccessToken) {
        [[NSNotificationCenter defaultCenter] postNotificationName:k$MODULE$UserTokenInvalidNotification
                                                            object:nil
                                                          userInfo:@{
                                                                     k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue:self
                                                                     }];
        return;
    }

    NSString *errorCode = [NSString stringWithFormat:@"%@", response.content[@"errorCode"]];
    if ([response.content[@"errorMsg"] isEqualToString:@"invalid token"]
        || [response.content[@"errorMsg"] isEqualToString:@"access_token is required"]
        || [errorCode isEqualToString:@"BL10015"]
        ) {
        // token 失效
        [[NSNotificationCenter defaultCenter] postNotificationName:k$MODULE$UserTokenInvalidNotification
                                                            object:nil
                                                          userInfo:@{
                                                                     k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue:self
                                                                     }];
        return;
    }

    // 常规错误
    if (errorType == $MODULE$APIManagerErrorTypeNoNetWork) {
        self.errorMessage = @"无网络连接，请检查网络";
    }
    if (errorType == $MODULE$APIManagerErrorTypeTimeout) {
        self.errorMessage = @"请求超时";
    }
    if (errorType == $MODULE$APIManagerErrorTypeCanceled) {
        self.errorMessage = @"您已取消";
    }
    if (errorType == $MODULE$APIManagerErrorTypeDownGrade) {
        self.errorMessage = @"网络拥塞";
    }
    
    // 其他错误
    dispatch_async(dispatch_get_main_queue(), ^{
        if ([self.interceptor respondsToSelector:@selector(manager:didReceiveResponse:)]) {
            [self.interceptor manager:self didReceiveResponse:response];
        }
        if ([self beforePerformFailWithResponse:response]) {
            [self.delegate managerCallAPIDidFailed:self];
        }
        if (self.failBlock) {
            self.failBlock(self);
        }
        [self afterPerformFailWithResponse:response];
    });
}

#pragma mark - method for interceptor

/*
    拦截器的功能可以由子类通过继承实现，也可以由其它对象实现,两种做法可以共存
    当两种情况共存的时候，子类重载的方法一定要调用一下super
    然后它们的调用顺序是BaseManager会先调用子类重载的实现，再调用外部interceptor的实现
    
    notes:
        正常情况下，拦截器是通过代理的方式实现的，因此可以不需要以下这些代码
        但是为了将来拓展方便，如果在调用拦截器之前manager又希望自己能够先做一些事情，所以这些方法还是需要能够被继承重载的
        所有重载的方法，都要调用一下super,这样才能保证外部interceptor能够被调到
        这就是decorate pattern
 */
- (BOOL)beforePerformSuccessWithResponse:($MODULE$URLResponse *)response
{
    BOOL result = YES;
    
    self.errorType = $MODULE$APIManagerErrorTypeSuccess;
    if ((NSInteger)self != (NSInteger)self.interceptor && [self.interceptor respondsToSelector:@selector(manager: beforePerformSuccessWithResponse:)]) {
        result = [self.interceptor manager:self beforePerformSuccessWithResponse:response];
    }
    return result;
}

- (void)afterPerformSuccessWithResponse:($MODULE$URLResponse *)response
{
    if ((NSInteger)self != (NSInteger)self.interceptor && [self.interceptor respondsToSelector:@selector(manager:afterPerformSuccessWithResponse:)]) {
        [self.interceptor manager:self afterPerformSuccessWithResponse:response];
    }
}

- (BOOL)beforePerformFailWithResponse:($MODULE$URLResponse *)response
{
    BOOL result = YES;
    if ((NSInteger)self != (NSInteger)self.interceptor && [self.interceptor respondsToSelector:@selector(manager:beforePerformFailWithResponse:)]) {
        result = [self.interceptor manager:self beforePerformFailWithResponse:response];
    }
    return result;
}

- (void)afterPerformFailWithResponse:($MODULE$URLResponse *)response
{
    if ((NSInteger)self != (NSInteger)self.interceptor && [self.interceptor respondsToSelector:@selector(manager:afterPerformFailWithResponse:)]) {
        [self.interceptor manager:self afterPerformFailWithResponse:response];
    }
}

//只有返回YES才会继续调用API
- (BOOL)shouldCallAPIWithParams:(NSDictionary *)params
{
    if ((NSInteger)self != (NSInteger)self.interceptor && [self.interceptor respondsToSelector:@selector(manager:shouldCallAPIWithParams:)]) {
        return [self.interceptor manager:self shouldCallAPIWithParams:params];
    } else {
        return YES;
    }
}

- (void)afterCallingAPIWithParams:(NSDictionary *)params
{
    if ((NSInteger)self != (NSInteger)self.interceptor && [self.interceptor respondsToSelector:@selector(manager:afterCallingAPIWithParams:)]) {
        [self.interceptor manager:self afterCallingAPIWithParams:params];
    }
}

#pragma mark - method for child
- (void)cleanData
{
    self.fetchedRawData = nil;
    self.errorType = $MODULE$APIManagerErrorTypeDefault;
}

//如果需要在调用API之前额外添加一些参数，比如pageNumber和pageSize之类的就在这里添加
//子类中覆盖这个函数的时候就不需要调用[super reformParams:params]了
- (NSDictionary *)reformParams:(NSDictionary *)params
{
    IMP childIMP = [self.child methodForSelector:@selector(reformParams:)];
    IMP selfIMP = [self methodForSelector:@selector(reformParams:)];
    
    if (childIMP == selfIMP) {
        return params;
    } else {
        // 如果child是继承得来的，那么这里就不会跑到，会直接跑子类中的IMP。
        // 如果child是另一个对象，就会跑到这里
        NSDictionary *result = nil;
        result = [self.child reformParams:params];
        if (result) {
            return result;
        } else {
            return params;
        }
    }
}

#pragma mark - private methods
- (void)removeRequestIdWithRequestID:(NSInteger)requestId
{
    NSNumber *requestIDToRemove = nil;
    for (NSNumber *storedRequestId in self.requestIdList) {
        if ([storedRequestId integerValue] == requestId) {
            requestIDToRemove = storedRequestId;
        }
    }
    if (requestIDToRemove) {
        [self.requestIdList removeObject:requestIDToRemove];
    }
}

#pragma mark - getters and setters
- (NSMutableArray *)requestIdList
{
    if (_requestIdList == nil) {
        _requestIdList = [[NSMutableArray alloc] init];
    }
    return _requestIdList;
}

- (BOOL)isReachable
{
    return YES;
//    BOOL isReachability = [[$MODULE$Mediator sharedInstance] $MODULE$Networking_isReachable];
//    if (!isReachability) {
//        self.errorType = $MODULE$APIManagerErrorTypeNoNetWork;
//    }
//    return isReachability;
}

- (BOOL)isLoading
{
    if (self.requestIdList.count == 0) {
        _isLoading = NO;
    }
    return _isLoading;
}

@end
"""
    xxnetos.mkclass(h_content, m_content, filename, module, "$MODULE$", selffolder)




def generateConponents(module,folder):
    subfolder = folder.rstrip("\\") + "/Components"

    __generateAPIProxy(module,subfolder);
    __generateURLResponse(module,subfolder);
    __generateLog(module,subfolder);
    __generateAPIBaseManager(module,subfolder);

    __generateGroupRequest(module,subfolder);