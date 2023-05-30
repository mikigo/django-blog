(function ($) {
    var $content_md = $(".form-row .field-content_md");
    var $content_ck = $(".form-row .field-content_ck");
    var $is_md = $("#id_is_md");
    console.log($content_ck)
    console.log($content_md)
    console.log($is_md)
    var switch_editor = function (is_md) {
        if (is_md) {
            $content_md.show();
            $content_ck.hide();
        } else {
            $content_md.hide();
            $content_ck.show();
        }
    };
    $is_md.on("click", function () {
        console.log("click")
        switch_editor($(this).is(":checked"));
    });
    console.log("no click")
    switch_editor($is_md.is(":checked"));
})(jQuery);