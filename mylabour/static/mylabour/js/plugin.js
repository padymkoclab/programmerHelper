
// jQuery plugin

(function($) {
    var author = 'Seti Volkylany';

    /**
     *
     */
    function show_author() {
        console.log(author);
    };

    $.fn.alone_function = function() {
        $('body').css('background-color', 'red');
    };

    $.fn.function_with_each = function() {
        this.each(function() {
            var text = $(this).text();
            $(this).text('--> ' + text);
        });

        $.fn.chain_function = function() {
            return this.each(function() {
                $('body').append('<h1>Header</h1>');
            });
        };

        $.fn.configurable_function = function(options) {
            var styles = $.extend({
                'color': 'blue',
                'background-color': 'green'
            }, options);

            el = '<p style="color: ' + styles['color'] + ';' + '">Text</p>';
            $('body').prepend(el);
        };
    };
}(jQuery));


// Module JS reuse functions

var Module = (function() {

    var author = 'Seti Volkylany';

  /*
  Variable for public methods
   */
    var public_methods = {};

    /**
    It is private method
     */
    function make_beauty_brackets(text) {
        return '**** ' + text + ' ****';
    }

    // make method as public
    public_methods.show_author = function show_author() {
        console.log(make_beauty_brackets(author));
    };

    public_methods.get_jquery_script_tag = function(){
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.async = true;
        script.src = "https://code.jquery.com/jquery-2.2.4.min.js";
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(script);
    };

    return public_methods

})();
