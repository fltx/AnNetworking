#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.append("..")
from _me_os import xxnetos;


def generateDefines(module,folder):
    selffolder = folder
    xxnetos.mkdir(selffolder)


    filename = "$MODULE$NetworkingDefines"

    content = """//
//  $MODULE$NetworkingDefines.h
//  $MODULE$Networking
//
//  Created by JoeXu on 2018/4/24.
//  Copyright © 2018年 JoeXu. All rights reserved.
//

#ifndef $MODULE$NetworkingDefines_h
#define $MODULE$NetworkingDefines_h

#import <UIKit/UIKit.h>

@class $MODULE$APIBaseManager;
@class $MODULE$URLResponse;



typedef NS_ENUM(NSUInteger,$MODULE$ServiceAPIEnvironment) {
    $MODULE$ServiceAPIEnvironmentDevelop,
    $MODULE$ServiceAPIEnvironmentReleaseCandidate,
    $MODULE$ServiceAPIEnvironmentRelease
};

typedef NS_ENUM(NSUInteger,$MODULE$APIManagerRequestType){
    $MODULE$APIManagerRequestTypePOST,
    $MODULE$APIManagerRequestTypeGET
};

typedef NS_ENUM (NSUInteger, $MODULE$APIManagerErrorType){
    $MODULE$APIManagerErrorTypeNeedAccessToken, // 需要重新刷新accessToken
    $MODULE$APIManagerErrorTypeNeedLogin,       // 需要登陆
    $MODULE$APIManagerErrorTypeDefault,         // 没有产生过API请求，这个是manager的默认状态。
    $MODULE$APIManagerErrorTypeLoginCanceled,   // 调用API需要登陆态，弹出登陆页面之后用户取消登陆了
    $MODULE$APIManagerErrorTypeSuccess,         // API请求成功且返回数据正确，此时manager的数据是可以直接拿来使用的。
    $MODULE$APIManagerErrorTypeNoContent,       // API请求成功但返回数据不正确。如果回调数据验证函数返回值为NO，manager的状态就会是这个。
    $MODULE$APIManagerErrorTypeParamsError,     // 参数错误，此时manager不会调用API，因为参数验证是在调用API之前做的。
    $MODULE$APIManagerErrorTypeTimeout,         // 请求超时。CTAPIProxy设置的是20秒超时，具体超时时间的设置请自己去看CTAPIProxy的相关代码。
    $MODULE$APIManagerErrorTypeNoNetWork,       // 网络不通。在调用API之前会判断一下当前网络是否通畅，这个也是在调用API之前验证的，和上面超时的状态是有区别的。
    $MODULE$APIManagerErrorTypeCanceled,        // 取消请求
    $MODULE$APIManagerErrorTypeNoError,         // 无错误
    $MODULE$APIManagerErrorTypeDownGrade,       // APIManager被降级了
};

typedef NS_OPTIONS(NSUInteger, $MODULE$APIManagerCachePolicy) {
    $MODULE$APIManagerCachePolicyNoCache = 0,
    $MODULE$APIManagerCachePolicyMemory = 1 << 0,
    $MODULE$APIManagerCachePolicyDisk = 1 << 1,
};


extern NSString * _Nonnull const k$MODULE$APIBaseManagerRequestID;

// notification name
extern NSString * _Nonnull const k$MODULE$UserTokenInvalidNotification;
extern NSString * _Nonnull const k$MODULE$UserTokenIllegalNotification;
extern NSString * _Nonnull const k$MODULE$UserTokenNotificationUserInfoKeyManagerToContinue;

// result
extern NSString * _Nonnull const k$MODULE$ApiProxyValidateResultKeyResponseJSONObject;
extern NSString * _Nonnull const k$MODULE$ApiProxyValidateResultKeyResponseJSONString;
extern NSString * _Nonnull const k$MODULE$ApiProxyValidateResultKeyResponseData;

/*************************************************************************************/
@protocol $MODULE$APIManager <NSObject>

@required
- (NSString *_Nonnull)methodName;
- (NSString *_Nonnull)serviceIdentifier;
- ($MODULE$APIManagerRequestType)requestType;

@optional
- (void)cleanData;
- (NSDictionary *_Nullable)reformParams:(NSDictionary *_Nullable)params;
- (NSInteger)loadDataWithParams:(NSDictionary *_Nullable)params;

@end

/*************************************************************************************/
@protocol $MODULE$APIManagerInterceptor <NSObject>

@optional
- (BOOL)manager:($MODULE$APIBaseManager *_Nonnull)manager beforePerformSuccessWithResponse:($MODULE$URLResponse *_Nonnull)response;
- (void)manager:($MODULE$APIBaseManager *_Nonnull)manager afterPerformSuccessWithResponse:($MODULE$URLResponse *_Nonnull)response;

- (BOOL)manager:($MODULE$APIBaseManager *_Nonnull)manager beforePerformFailWithResponse:($MODULE$URLResponse *_Nonnull)response;
- (void)manager:($MODULE$APIBaseManager *_Nonnull)manager afterPerformFailWithResponse:($MODULE$URLResponse *_Nonnull)response;

- (BOOL)manager:($MODULE$APIBaseManager *_Nonnull)manager shouldCallAPIWithParams:(NSDictionary *_Nullable)params;
- (void)manager:($MODULE$APIBaseManager *_Nonnull)manager afterCallingAPIWithParams:(NSDictionary *_Nullable)params;
- (void)manager:($MODULE$APIBaseManager *_Nonnull)manager didReceiveResponse:($MODULE$URLResponse *_Nullable)response;

@end

/*************************************************************************************/

@protocol $MODULE$APIManagerCallBackDelegate <NSObject>
@required
- (void)managerCallAPIDidSuccess:($MODULE$APIBaseManager * _Nonnull)manager;
- (void)managerCallAPIDidFailed:($MODULE$APIBaseManager * _Nonnull)manager;
@end

@protocol CTPagableAPIManager <NSObject>

@property (nonatomic, assign) NSInteger pageSize;
@property (nonatomic, assign, readonly) NSUInteger currentPageNumber;
@property (nonatomic, assign, readonly) BOOL isFirstPage;
@property (nonatomic, assign, readonly) BOOL isLastPage;

- (void)loadNextPage;

@end

/*************************************************************************************/

@protocol $MODULE$APIManagerDataReformer <NSObject>
@required
- (id _Nullable)manager:($MODULE$APIBaseManager * _Nonnull)manager reformData:(NSDictionary * _Nullable)data;
@end

/*************************************************************************************/

@protocol $MODULE$APIManagerValidator <NSObject>
@required
- ($MODULE$APIManagerErrorType)manager:($MODULE$APIBaseManager *_Nonnull)manager isCorrectWithCallBackData:(NSDictionary *_Nullable)data;
- ($MODULE$APIManagerErrorType)manager:($MODULE$APIBaseManager *_Nonnull)manager isCorrectWithParamsData:(NSDictionary *_Nullable)data;
@end

/*************************************************************************************/

@protocol $MODULE$APIManagerParamSource <NSObject>
@required
- (NSDictionary *_Nullable)paramsForApi:($MODULE$APIBaseManager *_Nonnull)manager;
@end


//Tools
#define _$MODULE$_SINGLETON_DEF(_type_,_func_) + (_type_ *)_func_;\
+(instancetype) alloc __attribute__((unavailable("call sharedInstance instead")));\
+(instancetype) new __attribute__((unavailable("call sharedInstance instead")));\
-(instancetype) copy __attribute__((unavailable("call sharedInstance instead")));\
-(instancetype) mutableCopy __attribute__((unavailable("call sharedInstance instead")));\

#define _$MODULE$_SINGLETON_IMP(_type_,_func_) + (_type_ *)_func_{\
static _type_ *theSharedInstance = nil;\
static dispatch_once_t onceToken;\
dispatch_once(&onceToken, ^{\
theSharedInstance = [[super alloc] init];\
});\
return theSharedInstance;\
}

#define $MODULE$_SINGLETON_DEF(_type_) _$MODULE$_SINGLETON_DEF(_type_,sharedInstance)
#define $MODULE$_SINGLETON_IMP(_type_) _$MODULE$_SINGLETON_IMP(_type_,sharedInstance)




#endif /* $MODULE$NetworkingDefines_h */
"""

    xxnetos.mkdefines(content, filename, module, "$MODULE$", selffolder)