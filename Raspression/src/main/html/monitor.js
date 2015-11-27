host = "192.168.0.123";

sensorCount = 2;

function onload() {

    console.log("onload");

    for ( var i=0; i<sensorCount; i++) {
        createSensorPanel(i);
        getVal(i, "min");
        getVal(i, "max");
        getVal(i, "def");
        getVal(i, "sens");
        getVal(i, "time");
        getVal(i, "cc");
    }

    setInterval(monitorValues, 100)
}

function createSensorPanel(s) {

    main = element("main")

    inner = document.createElement("DIV");
    inner.className = "inner";
    main.appendChild(inner);

    h1 = createWithText("H1", "Sensor " + s);
    inner.appendChild(h1);

    sensorContainer = document.createElement("DIV");
    sensorContainer.className = "sensorContainer"
    inner.appendChild(sensorContainer);

    sensorBar = document.createElement("DIV");
    sensorBar.className = "sensorBar"
    sensorBar.id = "sensor" + s;
    sensorContainer.appendChild(sensorBar);
    sensorBar.style.width = 0;

    inner.appendChild(createValueControl(s, "Min", "min", 0, 127));
    inner.appendChild(createValueControl(s, "Max", "max", 0, 127));
    inner.appendChild(createValueControl(s, "Def", "def", -1, 127));
    inner.appendChild(createValueControl(s, "Slide", "time", 0, 2000));
    inner.appendChild(createValueControl(s, "Sens", "sens", 0, 20000));
    inner.appendChild(createValueControl(s, "CC", "cc", 0, 127));

}

function createValueControl(s, label, name, min, max) {

    var inner = document.createElement("DIV");

    lbl = createWithText("P", label);
    lbl.className = "label";
    lbl.style.width = "40px";
    inner.appendChild(lbl);

    slider = document.createElement("INPUT");
    slider.id = "sensor"+s+"-"+name+"-slider";
    slider.type = "range";
    slider.className = "slider";
    slider.onchange = createChangeFunction(s, name);
    slider.min = min;
    slider.max = max;
    inner.appendChild(slider);

    num = createWithText("P", "---");
    num.id = "sensor"+s+"-"+name+"-value";
    num.className = "label";
    num.style.marginLeft = "15px";
    inner.appendChild(num);
    inner.className = "valuePanel";

    inner.appendChild(document.createElement("BR"));

    return inner;

}

function createChangeFunction(sensor, name) {
    return function() {
        val = element("sensor"+sensor+"-"+name+"-slider").value;
        target = clearChildren("sensor"+sensor+"-"+name+"-value");
        var t = document.createTextNode(val);
        target.appendChild(t);
        setVal(sensor, name);
    }
}


function monitorValues() {

    for ( var i=0; i<sensorCount; i++) {
        get(host, "value/"+i,
        createUpdateFunction(i),
        errorAlert("Failed"))
    }

}

function createUpdateFunction(sensor) {
    return function(req) {
        e = element("sensor"+sensor)
        w = (parseInt(req.responseText)/127) * 200
        e.style.width = w + "px"
    }
}

function shutdownServer() {

    get(host, "shutdown", null, null)

}

function getVal(sensor, name) {
    get(host, name + "/"+sensor,
        function(req) {
            v = parseInt(req.responseText)
            e = element("sensor"+sensor+"-"+name+"-slider")
            e.value = v
            e.onchange();
        }
    , null)
}

function setVal(sensor, name) {
    e = element("sensor"+sensor+"-"+name+"-slider");
    get(host, name + "/"+sensor+"/"+e.value, null, null);
}

function saveValues() {
    get(host, "save", null, null);
}
