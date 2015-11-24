var baseUrl = "";
var port = "8080";

/////////
// DOM //
/////////

function element(id) {
    return document.getElementById(id);
}

function clearChildren(id) {
    var panel = document.getElementById(id);
    while (panel.firstChild) {
        panel.removeChild(panel.firstChild);
    }
    return panel;
}

function addChild(parentId, childElement) {
    var parent = document.getElementById(parentId);
    parent.appendChild(childElement);
    return parent;
}

function createWithText(elementType, text) {
    var t = document.createTextNode(text);
    var p = document.createElement(elementType);
    p.appendChild(t);
    return p;
}

function show(id) {
    element(id).style.visibility = "visible";
}

function hide(id) {
    element(id).style.visibility = "hidden";
}


//////////
// HTTP //
//////////

function get(url, path, onsuccess, onfailure) {
    http("GET", url, path, onsuccess, onfailure);
}

function post(url, path, onsuccess, onfailure, content) {
    http("POST", url, path, onsuccess, onfailure, content);
}

function http(method, url, path, onsuccess, onfailure, content) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if ( req.readyState==4 ) {
            if ( req.status==200 ) {
                if ( onsuccess!==null && onsuccess!==undefined ) {
                    onsuccess(req);
                }
            } else {
                if ( onfailure!==null && onfailure!==undefined ) {
                    onfailure(req);
                }
            }
        }
    }
    req.open(method, "http://"+url+":"+port+"/"+path, true);
    if ( content!==null && content!==undefined ) {
        req.send(content);
    } else {
        req.send();
    }
}

function errorAlert(message) {
    return function(req) {
        window.alert(message);
    }
}

function errorInElement(panel, message) {
    return function(req) {
        var p = createWithText("H4", message);
        p.style.clear = "both";
        p.style.textAlign = "center";
        panel.appendChild(p);
    }
}


/////////////
// Utility //
/////////////

function bindFunction(f, i) {
    return f(i);
}




