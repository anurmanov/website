/**
 * Module in intended for adding features on each page:
 * - 'scroll to top' button
 * - empasizing current page in navigation menu
 */
(function IIFE(){
    function getScrollOffsets(w){
        w = w || window;
        //for all browsers acceot IE
        if (w.pageXOffset != null)
            return {x: w.pageXOffset, y: w.pageYOffset};
        //for IE (and other browsers) in standard mode
        var d = w.document;
        if (d.compatMode == 'CSS1Compat')
            return {x: d.documentElement.scrollLeft, y: d.documentElement.scrollTop};
        //for browsers in compatibility mode
        return {x: d.body.scrollLeft, y: d.body.scrollTop};
    }
    function scrollToTopSmoothly(step){
        clearInterval(scrollInterv);
        y = getScrollOffsets().y;
        step = step || 30;
        y -= step;
        step += 5;
        if (y < 0){
            window.scrollTo(0, 0);
            return;
        }
        window.scrollTo(0, y);
        scrollInterv = setInterval(scrollToTopSmoothly, 10, step);
    }
    $('#scroll_to_top_btn').click(function(event){
        event.preventDefault();
        event.stopPropagation();
        scrollToTopSmoothly(30);
    });
    $(window).on('scroll', function(){
        scrollOffsets = getScrollOffsets();
        (scrollOffsets.y > 200) ? $('#scroll_to_top_btn').css({display: 'block'}) : $('#scroll_to_top_btn').css({display: 'none'})
    });
    $('.MenuItem:not(#close_menu)').click(function(){
        document.location = $(this).children('a').attr('href');
    });
    $('#close_menu, #fade_panel, #menu_button', 'body').click(function(){
        var $fade_panel = $('#fade_panel');
        var $popup_menu = $('#popup_menu');
        $popup_menu.toggleClass('is-active').toggleClass('invisible');
        $fade_panel.toggleClass('is-active');                
    });
    var scrollInterv;
    //setting up active page in the navigation menu
    const path = document.location.pathname.match(/\/\w*\//);
    const p = path ? path[0] : document.location.pathname;
    $('.MenuItem', 'body').children('a[href="' + $.trim(p) + '"]').parent().addClass('active');
})()