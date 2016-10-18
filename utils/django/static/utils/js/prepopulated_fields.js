
(function($){

    $.fn.prepopulated_field = function(ids){

        var $this_field = $(this);

        $(ids).bind('input', function(e){
            var val = $(this).val();
            $this_field.val(val);
        });
    };

})(jQuery);
