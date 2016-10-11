(function($){

    $('.btn.open_all_panels').bind({
        click: function(){
            var $panels = $(this).parents('.tab-pane').find('.object_panel');
            var $collapsed_panels = $panels.filter(function(){
                var is_opened = $(this).find('.panel-collapse').hasClass('in');
                return is_opened ? false : true
            });
            $collapsed_panels.find('.panel-heading a').trigger('click');
        },
    });

    $('.btn.collapse_all_panels').bind({
        click: function(){
            var $panels = $(this).parents('.tab-pane').find('.object_panel');
            var $opened_panels = $panels.filter(function(){
                return $(this).find('.panel-collapse').hasClass('in')
            });
            $opened_panels.find('.panel-heading a').trigger('click');
        },
    });

})(jQuery);
