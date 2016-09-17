function noticelist(containerID, autoStart){
	var $element = $('#'+containerID).find('.notice-list');
	var autoPlay = autoStart;
	var auto = null;
	var speed = 2000;
	var timer = null;

	var move = $element.children().outerHeight();
	var lastChild;

	lastChild = $element.children().eq(-1).clone(true);
	lastChild.prependTo($element);
	$element.children().eq(-1).remove();

	if($element.children().length == 1){
		$element.css('top', '0px');
	} else {
		$element.css('top', '-'+move+'px');
	}

	if(autoPlay){
		timer = setInterval(moveNextSlide, speed);
		auto = true;
	}

	$element.find('>li').bind({
		'mouseenter': function(){
			if(auto){
				clearInterval(timer);
			}
		},
		'mouseleave': function(){
			if(auto){
				timer = setInterval(moveNextSlide, speed);
			}
		}
	});

	function moveNextSlide(){
		$element.each(function(idx){
			var firstChild = $element.children().filter(':first-child').clone(true);
			firstChild.appendTo($element.eq(idx));
			$element.children().filter(':first-child').remove();
			$element.css('top', '0px');

			$element.eq(idx).animate({'top':'-'+move+'px'}, 'normal');
		});
	}
}
