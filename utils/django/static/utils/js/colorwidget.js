jQuery(document).ready(function($){

    var $input_color = $('div.colorfield > span.input-group-addon input[type="color"]');

    $input_color.bind({
        change: function(){
            var value = $(this).val();
            $(this).parent().next('input').val(value);
        },
    });

    $('div.colorfield > input[type="text"]').bind({
        click: function(){
            $input_color.click();
        },
    });

});
