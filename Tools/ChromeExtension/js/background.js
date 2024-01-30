/*
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2024-01-18 14:09:48
 * @LastEditTime: 2024-01-30 10:41:57
 * @LastEditors: Suez_kip
 * @Description: 
 */
// 首次安装插件、插件更新、chrome浏览器更新时触发
chrome.runtime.onInstalled.addListener(() => {
  console.log("Extention has been installed!");
  console.log("Please check the logs whether they stand for correct proccesses.");
  chrome.storage.local.set({'result': [1,2,3]});
});

//保证用户的行为能够定位到某个网址，也即页面上
// const WRITEABLE_FLAG = true;
// var jsonStructure = {
//   "time": "",
//   "Timestamp": -1,
//   "ActivatedWindowID": -1,
//   "ActivatedURL": ""
// };
// var temp_list = [1, 2, 3];
// const NO_WINDOW_CHANGE_REPLACE_ID = -1;
// chrome.storage.local.clear();
// chrome.storage.local.set({"result_list": temp_list});

chrome.tabs.onActivated.addListener(function(activeInfo){
  console.log("NEW_LOG_START");
  console.log("Time: {" + Date.now() + "}");
  console.log("TabID: {" + activeInfo.tabId + "}");
  console.log("WindowsID: {" + activeInfo.windowId + "}");
  chrome.tabs.get(activeInfo.tabId, function(tab) {
    console.log('ActivatedURL: {', tab.url + "}");
  //   jsonStructure["time"] = new Date(Date.now());
  //   jsonStructure["Timestamp"] = Date.now();
  //   jsonStructure["ActivatedWindowID"] = activeInfo.windowId;
  //   jsonStructure["ActivatedURL"] = tab.url;

  //   console.log(jsonStructure);
  //   chrome.storage.local.get("result_list", function(result){
  //     temp_list = result.result_list;
  //     temp_list.push(jsonStructure);
  //   });
  //   chrome.storage.local.set({"result_list": temp_list}, function(){
  //     console.log(temp_list);
  //   });
  });

});

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.url) {
    console.log("NEW_LOG_START");
    console.log("Time: {" + Date.now() + "}");
    console.log("TabID: {" + tabId + "}");
    console.log("URLChanged: {" + changeInfo.url + "}");

    // jsonStructure["time"] = new Date(Date.now());
    // jsonStructure["Timestamp"] = Date.now();
    // jsonStructure["ActivatedURL"] = tab.url;
    // jsonStructure["ActivatedWindowID"] = NO_WINDOW_CHANGE_REPLACE_ID;

    // console.log(jsonStructure);
    // chrome.storage.local.get("result_list", function(result){
    //   temp_list = result.result_list;
    //   temp_list.push(jsonStructure);
    // });
    // chrome.storage.local.set({"result_list": temp_list}, function(){
    //   console.log(temp_list);
    // });
  }
});

// 监听点击事件
chrome.action.onClicked.addListener((tab) => {
  console.log("-----------CLICKED-----------");
});