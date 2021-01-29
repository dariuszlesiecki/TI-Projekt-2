window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || 
window.msIndexedDB;
 
window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || 
window.msIDBTransaction;
window.IDBKeyRange = window.IDBKeyRange || 
window.webkitIDBKeyRange || window.msIDBKeyRange
 
if (!window.indexedDB) {
   window.alert("Your browser doesn't support a stable version of IndexedDB.")
}

var request = window.indexedDB.open("offlineDatabase", 1);

var db;

request.onerror = function(event) {
  console.log("Why didn't you allow my web app to use IndexedDB?!");
};
request.onsuccess = function(event) {
  db = event.target.result;
};

request.onupgradeneeded = function(event) {
  // Save the IDBDatabase interface
  var db = event.target.result;
  var objectStore = db.createObjectStore("post", { keyPath: "id", autoIncrement : true});
  objectStore.createIndex("created", "created");
  objectStore.createIndex("title", "title");
  objectStore.createIndex("body", "body");
};

function showForm(){
    var myDiv = document.getElementById("f");
    myDiv.style.display='block';
}

function addOffline(){
    var myDiv = document.getElementById("f");
    myDiv.style.display='none';
    var title = form.title.value;
    var body = form.body.value;
    var created = new Date()
    var tmp = {
      "created":created,
      "title":title,
      "body":body
    };
    data = JSON.stringify(tmp);

    var transaction = db.transaction(["post"], "readwrite")
    .objectStore("post")
    .add(tmp);

    request.onsuccess = function(event) {
      alert("Success");
   };
   
   request.onerror = function(event) {
      alert("Error");
   };
}

function sendOnline(){
    var counter = 0;
    var transaction = db.transaction("post", "readwrite");
    var obj = transaction.objectStore("post");
    obj.openCursor().onsuccess = function (event) {
      var cursor = event.target.result;
      if (cursor) {
        var tmp = {
          "created":cursor.value.created,
          "title":cursor.value.title,
          "body":cursor.value.body
        };
        
        to_send = JSON.stringify(tmp);
              
        $.post( "/synchronize", {
                  javascript_data: to_send 
        });
        
        cursor.delete();
        counter += 1;
        cursor.continue();
      }
      else if (counter == 0) {
        alert("Brak danych offline.");
      }
    };
}