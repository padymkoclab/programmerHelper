
var sum = function(x, y){
    return x + " + " + y + " = " + x + y
};


function closure(func, ...args){
    old_args = args
    function _w(...args){
        args = args.concat(old_args)
        return func.apply(this, args)
    }
    return _w
}

sum = closure(sum, 3)

console.log(sum(y=9));
console.log(sum(y=-9));
console.log(sum(y=0));
