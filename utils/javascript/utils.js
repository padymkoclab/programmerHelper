
String.prototype.rsplit = function(sep){
    var array = this.split(sep);
    var last_el = array.pop();
    rest_array = array.join(sep);
    return [rest_array, last_el]
}


// Override console.log (version 1)
var console=(function(oldCons){
    return {
        log: function(text){
            text = JSON.stringify(text)
            oldCons.log(text);
        },
    };
}(window.console));
window.console = console;

// Override console.log (version 2)
(function(){
    log = console.log;
    console.log = function(){
        log.apply(this, arguments);
        log.apply(this, arguments);
    }
})()
