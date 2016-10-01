(function($){

    // http://stephanwagner.me/auto-resizing-textarea
    $.fn.AutoResize = function(){

        $(this).bind('input', function(event) {
            offset = this.offsetHeight - this.clientHeight;
            $(this).css('height', 'auto').css('height', this.scrollHeight + offset);
        });
    }

})(jQuery);
