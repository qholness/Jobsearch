function getTimeStamp(){
    var now = new Date();
    var hours = now.getHours();
    var minutes = "0" + now.getMinutes();
    var seconds = "0" + now.getSeconds();
    return hours + ":" + minutes.substr(-2) +
    ":" + seconds.substr(-2)
}
