API Respone Format
Json Response
1. Definition
{
 code ==> Response status code, Required
 message: success or fail message, Required
 data: API logistic response, Required
 pagination: paging, Optional
}

2. Example
2.1 success response
{
 code: 0,
 message: "success",
 data: [{"bug_id": 1, "summary":"bug 1", ...}, {"bug_id": 2, "summary": "bug 2", ...}, ...]
}

2.2 success response with paging info
{
 code: 0
 message: "success",
 data: [{"bug_id": 1, "summary":"bug 1", ...}, {"bug_id": 2, "summary": "bug 2", ...}, ...],
 pagination:{
   count: 100,
   previous: "http://127.0.0.1:8000/qc/jira/bugs/?limit=10&offset=10",
   next: "http://127.0.0.1:8000/qc/jira/bugs/?limit=10&offset=30"
 }
}

2.3 error response
{
 code: 4001,
 message: "权限不够!"
 data: [],
}

API response code
根据返回码，开发者可以根据返回码信息调试接口，排查错误。
请开发人员继续补充
Response code(返回码)
说明
0	请求成功
4000	请求失败
4001	访问权限不够
4002	用户名错误
4003	密码错误
4004	资源不存在
4005	资源过期
4006	不合法的请求格式
4007	不合法的参数
4008	请求处理超时
4009	参数类型错误
4010	参数不全
4011	SQL语句不允许执行
4012	SQL语法错误
5000	服务器异常
5001	服务器错误配置
9999	未定义的错误（请具体化）

参考：
微信公众平台-返回码(http://mp.weixin.qq.com/wiki/17/fa4e1434e57290788bde25603fa2fcbd.html)
