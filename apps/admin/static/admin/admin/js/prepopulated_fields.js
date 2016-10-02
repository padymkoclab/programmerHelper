
(function($){

    slugify = function(val){
        return val.toString().
            toLowerCase().
            replace(/\ +/g, '-').
            replace(/[^\w\-]+/g, '').
            replace(/\-\-+/g, '');
    };

    $.fn.prepopulated_field = function(ids){

        var $this_field = $(this);

        $(ids).bind('input', function(e){
            var val = $(this).val();

            val = slugify(val);

            $this_field.val(val);
        });

        $(ids).trigger('input');

    };

})(jQuery);
