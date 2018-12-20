/**
 * 
 * Opencrunch Javascript
 * 
 */

var Opencrunch = {
		version : '0.1',
		
		Window : {
			
			Modal : {
				modal : null,
				
				Init : function () {
					this.modal = $( "#modal" ).dialog({ 
						autoOpen: false,
						modal: true,
						resizable: false,
						width: Opencrunch.Utils.em2px(40)
					});
				},
				
				loadContent : function(url, data, title) {
					
					var action = 'POST';
					if (data == null) action = 'GET';
					
					$.ajax({
						url : url,
						data : data,
						type : action,
						success : function(result) {
							Opencrunch.Window.Modal.modal.html(result);
							Opencrunch.Window.Modal.prepContent(title);
						}
					});
				},
				
				prepContent : function (title) {
					this.modal.dialog('option', 'title', title);
					this.modal.dialog('open');
					this.modal.find("input[type=submit]").button();
					this.modal.find("#id_dateMade").attr('type', 'date');
					
					modal.find("form").submit(function(e) {
						
						e.preventDefault();
						var form = modal.find('form');
						var url = form.attr('action')
						var data = form.serialize();
					});
				},
			},
		},
		
		Init : function() {
			$("input[type=submit], .widget a, .widget button, .btn, .report-table a").button();
			
			this.Window.Modal.Init();
			
			$('a.modal').click(this.Events.modalLinkClick);
			
			$( "#tabs" ).tabs();
		},
		
		Events : {
			modalLinkClick : function (e) {
				e.preventDefault();
				
				Opencrunch.Window.Modal.loadContent(e.currentTarget.href, null, e.currentTarget.title);
			},
			
			chargeDeleteClick : function (e){
	  				
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
									$('.contact-list li.id_' + id).find('.ent-bal').text(item + ' €');
								});
								
								Opencrunch.Entities.getHistory(Opencrunch.Entities.activeEntity);
							}
						});
	  				}
			},
		},
			
		Categories : {
			
			/**
			 * Plonks a progress bar on the category list items
			 */
			showPercentage  : function() {
				$( ".cat-percent" ).each(function(idx, item) {
					
					a = parseFloat($(item).children().attr('percent'))
					
					$(item).progressbar({
						value: a,
					})
				})
			},
		},
		
		Entities : {
			
			historyTempalate : null,
			activeEntity : null,
			
			Init : function() {
				
				if($('.entities-history-template').length) {
					
					this.historyTemplate = $('.entities-history-template');
					this.historyTemplate.detach();
				  	
				  	$('.contact-list li').click(function(e) {
				  		entityId = e.currentTarget.id.replace('f', '').replace('d', '').replace('c', '');
				  		Opencrunch.Entities.getHistory(entityId);
				  	});
				}
			},
		
			getHistory : function(eid) {
				
				this.activeEntity = eid;
				
				$('#entities-history').hide();
		  		$('.entities-history-template').remove();
				
		  		Opencrunch.Charges.forEntity(eid, this.fillHistory);
			},
			
			fillHistory: function(data) {
				
				$('.contact-list li.id_' + entityId).find('.ent-bal').text(data.balance + ' €');
				
				$.each(data.items, function(index, charge) {
					
	  				t = Opencrunch.Entities.historyTemplate.clone();
	  				fields = [charge.date, charge.description, charge.quantity, charge.category, charge.balance]
	  				
	  				t.data('id', charge.id);
	  				
	  				t.children().each(function(idx, elem){
	  					
	  					$(elem).text(
	  						fields[idx]
	  					);
	  				});
	  				
	  	  			$('#entities-history table').append(t);
	  	  			
	  	  			t.find('.charge-delete').click(Opencrunch.Events.chargeDeleteClick);
				});
				
				$('#entities-history').show();
			},
		},
		
		Charges : {
			
			forEntity : function (eid, cb) {
				$.getJSON("/balance/X/".replace('X', eid), cb);
			},
		},
		
		Utils : {
			
			getCookie : function (cname) {
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
			},

			getDefaultFontSize : function (parentElement) {
			    parentElement = parentElement || document.body;
			    var div = document.createElement('div');
			    div.style.width = "1000em";
			    parentElement.appendChild(div);
			    var pixels = div.offsetWidth / 1000;
			    parentElement.removeChild(div);
			    return pixels;
			},

			em2px : function (ems) {
					return Math.round(ems * this.getDefaultFontSize())
			}
		},
}

$(function() {
	Opencrunch.Init();
	Opencrunch.Entities.Init();
});

