document.addEventListener('DOMContentLoaded', function () {
    var noteTextarea = document.getElementById('note');
    var saveButton = document.getElementById('save');
    var loadButton = document.getElementById('load');
  
    // 保存笔记
    saveButton.addEventListener('click', function () {
        var note = noteTextarea.value;
        chrome.storage.local.set({ 'note': note }, function () {
            console.log('Note saved');
        });
    });
  
    // 加载笔记
    loadButton.addEventListener('click', function () {
        chrome.storage.local.get('note', function (result) {
            if (result.note) {
                noteTextarea.value = result.note;
            } else {
                noteTextarea.value = '';
            }
        });
    });
});