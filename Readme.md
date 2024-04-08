<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2023-11-24 15:48:26
 * @LastEditTime: 2024-04-07 17:37:21
 * @LastEditors: Suez_kip
 * @Description: 
-->
# BACD

## 流程图分析

![图 2](images2/3a5d1cf8d491e9f40652640363490dd0df046830f1fdb714b21d510289bfa9e8.png)  

## 文件结构和流程图对比

![图 1](images2/e440c5c7b35d6c614d96b307f8b1fad89a0b3f25adece0618848b16a6f4623de.png)  

## TODO List

- WebFSM

  - [ ] UserGroupMap.py
  - [ ] WebFlow.py
  - [ ] WebFSM.py
  - [ ] WebFSMAnalysis.py
  - [ ] SourceCodeAnalysis.py
  - [ ] TestCaseGenerator.py
  - [ ] TestCaseExecutor.py
  - [ ] TestResultAnalysis.py
  - [ ] Report.py

- Tools

  - [ ] FlowGenerator.py
  - [ ] WebSiteTemplateAnalysis.py
  - [ ] WebSourceLoader.py

## 数据库设计

数据库共会维护七张表，其中第一张是唯一的，后面几张可以根据性能扩展：

- meta表，记录有哪些域名等以及其数据库的分布情况，这张表在小数据量中可以省略；
- 请求全数据记录，对应到响应和相应统计；
- 响应全数据记录，对应到请求和接口；
- 请求统计（接口）表，记录请求的相关信息用于重放对应，基于uri（可以包括参数键）hash形成uuid；
- 参数记录表，附属于某个接口的参数组，其中参数组会被对应到全请求数据表；
- 响应统计表，附属于某个请求下的结果，结构一致的会被重新存储；
- 敏感参数，以及通用数据记录表；
