$(function(){
		$(".links").click(function(e){
			$("#mainContent").empty();
			$("#mainContent").load($(this).attr('href'));
			e.preventDefault();
		});
});