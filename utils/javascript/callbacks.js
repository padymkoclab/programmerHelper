

var show_usage_js_promises = function(){

    var function1 = function(){
        for (var i = 0; i < 500000000; i++) {}
        console.log('Function1 is done');
    }

    var function2 = function(){
        for (var i = 0; i < 500000000; i++) {}
        console.log('Function2 is done');
    }

    var function3 = function(){
        for (var i = 0; i < 500000000; i++) {}
        console.log('Function3 is done');
    }

    new Promise(function(resolve, reject){
            function3();
            return new Promise(function(resolve, reject){
                function2();
                return new Promise(function(resolve, reject){
                    function1();
                })
        })
    })
}


var show_usage_js_callback = function(){

    var function1 = function (callback, callback_for_callback){

        // Do something (as an example is a loop)
        for (var i = 0; i < 500000000; i++) {}

        console.log('Function1 is completed')
        callback(callback_for_callback);
    }


    var function2 = function (callback){

        // Do something (as an example is a loop)
        for (var i = 0; i < 500000000; i++) {}

        console.log('Function2 is completed')
        callback();
    }


    var function3 = function(){

        // Do something (as an example is a loop)
        for (var i = 0; i < 500000000; i++) {}

        console.log('Function3 is completed')
    }

    function1(function2, function3)
}


// show_usage_js_callback();
show_usage_js_promises()
