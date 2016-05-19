function resize_images(ratio) {

var layers = [["blacks_layer","/svg/vesalius-outline-mask-blacks.gif"],["shading_layer","/svg/vesalius-outline-mask-shading.gif"]];


for (var i = 0; i < layers.length; i++) {
var c=document.getElementById(i[0]);
var ctx=c.getContext("2d");
c.width = img.width * ratio;
c.height = img.height * ratio;
ctx.drawImage(img, 0, 0, c.width, c.height);
img.src=i[1];
}

var c=document.getElementById("highlights_layer");
var ctx=c.getContext("2d");

var data = output-angular.svg;

var DOMURL = window.URL || window.webkitURL || window;

var img = new Image();
var svg = new Blob([data], {type: 'image/svg+xml;charset=utf-8'});
var url = DOMURL.createObjectURL(svg);

img.onload = function () {
	ctx.drawImage(img, 0, 0,img.width * ratio,img.height * ratio);
	DOMURL.revokeObjectURL(url);
}

img.src = url;

}



// Adapted from here: http://stackoverflow.com/questions/17861447/html5-canvas-drawimage-how-to-apply-antialiasing
// And here https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Drawing_DOM_objects_into_a_canvas


function cpresize() {
	
	var window_height = window.innerHeight;
	var window_width = window.innerWidth;
	var image_height = 3510;
	var image_width = 2222;
	var ratio = window_height/image_height;
	
	var skinman_div = document.getElementById("left");
	
	skinman_div.height = window_height;
	skinman_div.width = image_width*ratio;
	
	resize_images(ratio);
	
	var content_div = document.getElementById("right");
	content_div.height = window_height;
	content_div.width = window_height-skinman_div.width;		
};




window.onload = cpresize();
window.onresize = cpresize();