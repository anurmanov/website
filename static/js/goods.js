/**
 * Module is intended for rearrange category list items in smooth construction
 */
(function relocateSubgroups(){
    var $capts = $('.item_caption');
    var max_width_of_caption = 0;
    $capts.each(function(index){
        var rect = this.getBoundingClientRect();
        max_width_of_caption = (max_width_of_caption < (rect.right - rect.left)) ? (rect.right - rect.left) : max_width_of_caption;
    });
    var $imgs = $('.item_img');
    $imgs.each(function(index){
        var rect = this.getBoundingClientRect();
        max_width_of_caption = (max_width_of_caption < (rect.right - rect.left)) ? (rect.right - rect.left) : max_width_of_caption;
    });
    var $items = $('.subgroup_item, .good_item');
    $items.each(function(index){
        var rect = this.getBoundingClientRect();
        max_width_of_caption = (max_width_of_caption < (rect.right - rect.left)) ? (rect.right - rect.left) : max_width_of_caption;
    });
    $items.css({width: max_width_of_caption +'px'});
    var max_height_of_subgrp = 0;
    $items.each(function(index){
        var rect = this.getBoundingClientRect();
        max_height_of_subgrp = (max_height_of_subgrp < (rect.bottom - rect.top)) ? (rect.bottom - rect.top) : max_height_of_subgrp;
    });
    $items.css({height: max_height_of_subgrp +'px'});
})();