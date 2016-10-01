jQuery(document).ready(function($){

    $('div.colorfield input[type="color"]').change(function(){
        var color = $(this).val();
        var $color_display = $(this).parent().find('input[type="text"]')
        $color_display.val(color);
    });

    $('div.colorfield input[type="color"]').change();

});
