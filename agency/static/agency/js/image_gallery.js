'use strict';
var imagesList = document.querySelectorAll('#gallery-images div');
var items = new Array(imagesList.length);
for (var i = 0; i < imagesList.length; ++i) {
    items[i] = {
        src: imagesList[i].getAttribute("data-image"),
        w: imagesList[i].getAttribute("data-width"),
        h: imagesList[i].getAttribute("data-height")
    }
}

var thumbnailsList = document.querySelectorAll('#thumbnails img');
for (var i = 0; i < thumbnailsList.length; ++i)
    thumbnailsList[i].addEventListener('click', openInFullScreen)

var pswpElement = document.querySelectorAll('.pswp')[0];

function openInFullScreen(event) {
    var options = {
        index: +event.target.getAttribute("data-index"),
        bgOpacity: 0.85
    };
    var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
    gallery.init();
}