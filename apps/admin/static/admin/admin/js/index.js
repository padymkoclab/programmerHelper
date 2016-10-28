jQuery(document).ready(function($) {

    /*
    Toggle display/hide the left sidebar
     */
    $('#toggle_sidebar').click(function(event) {
        $('#wrapper').toggleClass('toggle_sidebar');
    });

    /*
    Toggle FA icon chevron
     */
    $('#sidebar_apps ul li.main_list > table .switch_nested_list').click(function(event) {

        var $item= $(this).parents('li');

        var has_icon_chevron_left;
        var icon_chevron_left = 'fa-chevron-left';
        var icon_chevron_down = 'fa-chevron-down';

        var $all_items = $item.parent('ul').find('li');
        var $this_nested_list = $item.find('.div_nested_list');

        // clear class .active in all items
        $all_items.removeClass('active');

        // if item it was not changed from last click
        if ($(this).hasClass(icon_chevron_left)) {
            has_icon_chevron_left = true;
        }

        // all_items_nested_list.slideToggle();

        // remove all icons in all items
        var $all_items_icons = $all_items.find('.switch_nested_list');
        $all_items_icons.removeClass(icon_chevron_left);
        $all_items_icons.removeClass(icon_chevron_down);

        // add icon_chevron_left to all items
        $all_items_icons.addClass(icon_chevron_left);

        // if item it was not changed from last click
        // add icon icon_chevron_down instead of icon_chevron_left
        // to this item
        if (has_icon_chevron_left === true) {

            $(this).removeClass(icon_chevron_left);
            $(this).addClass(icon_chevron_down);

            $item.addClass('active');

        }

        $item.parent().find('.div_nested_list').not($this_nested_list).slideUp();

        $this_nested_list.slideToggle();

    });

    /*

     */
    $('#sidebar_apps .nested_list li').click(function(event) {
        // $(this).toggleClass('nested_list_active_page');
    });

    /*
    Fullscree window
     */
    $('a#link_fullscreen').click(function(event) {

        function requestFullScreen(element) {
            // Supports most browsers and their versions.
            var requestMethod = element.requestFullScreen || element.webkitRequestFullScreen || element.mozRequestFullScreen || element.msRequestFullScreen;

            if (requestMethod) { // Native full screen.
                requestMethod.call(element);
            } else if (typeof window.ActiveXObject !== "undefined") { // Older IE.
                var wscript = new ActiveXObject("WScript.Shell");
                if (wscript !== null) {
                    wscript.SendKeys("{F11}");
                }
            }
        }

        var elem = document.body; // Make the body go full screen.
        requestFullScreen(elem);
    });


    /*

    */
    $('button.close.close_panel').bind({
        click: function(e){
            $(this).parents('div.panel').fadeOut('slow');
        },
    });

    $('button.close.hide_panel').bind({
        click: function(e){
            $(this).parents('div.panel').find('div.panel-body').slideUp('slow');
        },
    });

    $('button.close.show_panel').bind({
        click: function(e){
            $(this).parents('div.panel').find('div.panel-body').slideDown('slow');
        },
    });

});
