/** 
 * Module adds slider feature to main page
*/
(function sliderIssues() {
    let sliderInterval;
    function nextSlide(evn) {
        let $slides = $('.slide');
        clearTimeout(sliderInterval);
        if (evn){
            $slides.children('img').stop();
        }
        $slides.each(function(index){
            let $this = $(this);
            if ($this.is('.visible, .active')){
                $this.removeClass('visible active').children('img').css({top: '0%'});
                let $next_slide = (index === ($slides.length - 1)) ? $slides.first() : $this.next();
                $next_slide.toggleClass('visible').toggleClass('active').children('img').css({top: '0%'}).animate({top: '-195%'}, 
                {
                    duration: 2000, 
                    complete: () => sliderInterval = setTimeout(nextSlide, 4000)
                });
                return false;
            }
        });
    }
    function prevSlide(evn) {
        var $slides = $('.slide');
        clearTimeout(sliderInterval);
        if (evn){
            $slides.children('img').stop();
        }
        $slides.each(function(index){
            var $this = $(this);
            if ($this.is('.visible, .active')){
                $this.removeClass('visible active').children('img').css({top: '0%'});
                var $prev_slide = (index === 0) ? $($slides.get($slides.length - 1)) : $this.prev();
                $prev_slide.toggleClass('visible').toggleClass('active').children('img').css({top: '0%'}).animate({top: '-195%'}, 
                {
                    duration: 2000, 
                    complete: () => sliderInterval = setTimeout(nextSlide, 4000)
                });
                return false;
            }
        });
    }
    /** Function for fetching slider images in ajax */
    function afterDocumentLoaded(){
        let sliderImgs;
        fetch('/slider_images', {method: 'GET'})
        .then(response => response.json())
        .then(response => sliderImgs = [...response])
        .then(() => {
            const $slider_imgs = $('.slide > img');
            $slider_imgs.one('load', (evn) => {
                this.image_loaded = true;
                let $slider_imgs = $('.slide > img');
                let j = 0;
                $slider_imgs.each(() => {
                    if (this.image_loaded)
                        j++;
                });
                //Slider starts showing slides after each slider image beeing loaded
                if (j == $slider_imgs.length){
                    $slider_imgs.first().parent().toggleClass('visible').toggleClass('active');
                    $('#loading_slider_img').hide();
                    if (!sliderInterval)
                        sliderInterval = setTimeout(nextSlide, 4000);
                }
            })
            .each((index, elem) => {elem.src = sliderImgs[index]});    
        });
    };
    $('#left_arrow > img').click(prevSlide);
    $('#right_arrow > img').click(nextSlide);
    $('.slide, .slider_nav_button').on('mouseenter mouseleave', (evn) => $('.slider_nav_button').toggleClass('invisible'));
    afterDocumentLoaded();
})();

