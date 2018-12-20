$( function() {
	$(".widget input[type=submit], .widget a, .widget button, .btn").button();
	
	modal = $( "#modal" ).dialog({ 
		autoOpen: false,
		modal: true,
		resizable: false,
		width: em2px(40)
	});
	
	$('a.modal').click(function(e) {
		e.preventDefault();
		
		$('#modal').load(e.currentTarget.href, function() {
			modal.dialog('option', 'title', e.currentTarget.title);
			modal.dialog('open');
			modal.find("input[type=submit]").button();
			modal.find("#id_dateMade").attr('type', 'date');
			
			modal.find("input[type=submit]").click(function(e) {
				
				e.preventDefault();
				var form = modal.find('form');
				var url = form.attr('action')
				var data = form.serialize();
				
				$.ajax({
					url: url,
					data: data,
					type: 'POST',
					success: function(result) {
						modal.html(result)
					}
				})
				
				return false;
			})
			
			return false;
		});
	});
	
	$( "#tabs" ).tabs();
  	
	if($('.entities-history-template').length) {
	
		template = $('.entities-history-template');
		template.detach();
	  	
	  	$('.contact-list li').click(function(e) {
	  		
	  		$('#entities-history').hide();
	  		
	  		entityId = e.currentTarget.id.replace('f', '').replace('d', '').replace('c', '');
	  		$('.entities-history-template').remove();
	  		
	  		$.getJSON("/balance/0/".replace('0', entityId), function(data) {
	  			
	  			$('#entities-history').show();
	  			
	  			$('.contact-list li.id_' + entityId).find('.ent-bal').text(data.balance + ' €');
	  			
	  			$.each(data.items, function(index, charge) {
	  				t = template.clone();
	  				fields = [charge.date, charge.description, charge.quantity, charge.category, charge.balance]
	  				
	  				t.data('id', charge.id);
	  				
	  				t.children().each(function(idx, elem){
	  					
	  					$(elem).text(
	  						fields[idx]
	  					);
	  				});
	  				
	  	  			$('#entities-history table').append(t);
	  	  			
	  	  			t.find('.charge-delete').click(function (e){
	  	  				
	  	  				e.preventDefault();
	  	  				
	  	  				if (confirm("Do you really want to delete this?")) {
		  	  				
	  	  					elem = $(e.target).parent().parent()
	  	  					
		  	  				$.ajax({
								url: '/charge/delete/' + elem.data('id') + '/',
								type: 'POST',
								beforeSend: function(xhr) {
							        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
							    },
								success: function(result) {
									elem.remove();
									
									$.each(result, function(id, item) {
										$('.entities-history-template').remove();
										// TODO: Fix double load bug
										$('.contact-list li.id_' + id).click();
										$('.contact-list li.id_' + id).find('.ent-bal').text(item + ' €');
									});
								}
							});
	  	  				}
	  	  			});
	  			});
	  		});
	  	});
	}
});

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function getDefaultFontSize(parentElement)
{
    parentElement = parentElement || document.body;
    var div = document.createElement('div');
    div.style.width = "1000em";
    parentElement.appendChild(div);
    var pixels = div.offsetWidth / 1000;
    parentElement.removeChild(div);
    return pixels;
}

function em2px(ems) {
	return Math.round(ems * getDefaultFontSize())
}