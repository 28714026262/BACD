/*
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2024-01-28 20:09:13
 * @LastEditTime: 2024-01-28 20:09:18
 * @LastEditors: Suez_kip
 * @Description: 
 */
heatMapData_init = [];
chrome.storage.local.set({"heatMapData": heatMapData_init});

var isMapHas = (pid) =>{
	var heatMapData = []
	chrome.storage.local.get(['heatMapData'], function(result){
		heatMapData = result
	})
	for (var i = heatMapData.length - 1; i >= 0; i--) {
		if(heatMapData[i].pid == pid) return i;
	}
	chrome.storage.local.set({"heatMapData": heatMapData});
	return false;
}

var addClickMaptoArr = (index,clickData) =>{
	var heatMapData = []
	chrome.storage.local.get(['heatMapData'], function(result){
		heatMapData = result
	})
	heatMapData[index].clickData.push(clickData);
	chrome.storage.local.set({"heatMapData": heatMapData});
}

chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
	  	if(request.type == 9)
	  	{
			var value = request.value;
			var index = isMapHas(value.pid);
			if(index)
				addClickMaptoArr(index, [value.X,value.Y])
			else 
			{
				index = addMapArr(value.pid, value.url, value.title, value.isSearch);
				addClickMaptoArr(index, [value.X,value.Y]);
			}
			console.log("已记录点击",value.X,value.Y,value.width,value.height);
		}
	}
);
