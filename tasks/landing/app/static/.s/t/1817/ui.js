"use strict";window.UcozApp={},window.UcozApp.comments=function(){var e,o=document.querySelectorAll(".e-comments");for(e=0;e<o.length;e++){var i=o[e].innerText.match(/\d+/g);o[e].innerText=i}},UcozApp.comments(),function(s){s.fn.uPlaginMenu=function(){s(".navItemMore",this).length||s(".uMenuRoot",this).append('<li class="navItemMore"><div class="nav_menu_toggler"><i class="material-icons">more_vert</i></div><ul class="overflow"></ul></li>'),s(".uMenuRoot li.navItemMore",this).before(s(".overflow > li",this));var e=s(".navItemMore",this),o=s(".uMenuRoot > li:not(.navItemMore)",this),i=e.width(),n=s("#uNMenuDiv1",this).width();for(o.each(function(){i+=s(this).width()}),n<i?e.show():e.hide();n<i&&960<window.innerWidth;)i-=o.last().width(),o.last().prependTo(".overflow",this),o.splice(-1,1);s(".uMenuRoot",this).css({visibility:"visible",overflow:"visible"})}}(jQuery);var nNmenu=function(){$("#catmenu").uPlaginMenu()};$(function(){$(".owl-slider-food").owlCarousel({loop:!0,margin:0,responsiveClass:!0,items:4,responsive:{0:{items:1,nav:!1,dots:!0},600:{items:2,nav:!1,dots:!0},700:{items:3,nav:!0,dots:!0},961:{items:4,nav:!0,dots:!0}}}),window.onresize=nNmenu,$(".show-menu").on("click",function(){$("#uNMenuDiv1").toggleClass("openMenu"),$("body").toggleClass("fixbody")});var e=$("li.uWithSubmenu");function o(){window.innerWidth<961?$("#catmenu li.uWithSubmenu i").each(function(){"keyboard_arrow_down"==$(this).html()&&$(this).html("add")}):$("#catmenu li.uWithSubmenu i").html("keyboard_arrow_down")}if($("> a",e).after('<i class="material-icons menu_tog">keyboard_arrow_down</i>'),$("> i",e).on("click",function(){window.innerWidth<961&&("add"==$(this).text()?($(this).parent().addClass("over"),$(this).text("remove")):($(this).parent().removeClass("over"),$(this).text("add")))}),o(),$(window).resize(function(){o()}),$('[id^="uNMenuDiv"]').append('<div class="close-menu"><i class="material-icons">close</i></div>'),$(".close-menu").on("click",function(){$("#uNMenuDiv1").removeClass("openMenu"),$("body").removeClass("fixbody")}),$("#uNMenuDiv1").on("click",function(e){e.target==this&&($("#uNMenuDiv1").removeClass("openMenu"),$("body").removeClass("fixbody"))}),$(".search-head .i_search").on("click",function(e){$(".uMenuRoot").css({overflow:"hidden"}),$(".searchForm form").toggleClass("open-form"),$(".searchForm form").hasClass("open-form")&&$(".search-head  input.queryField").focus()}),$(".searchForm form").on("transitionend webkitTransitionEnd oTransitionEnd",function(){nNmenu()}),$(".search-head  input.queryField").on("input",function(){/^\s*$/.test($(this)[0].value)?$(".search-head .search-box").css("z-index","89"):$(".search-head .search-box").css("z-index","99")}),$(".uTable,#shop-price-list, #order-table, #setsList, #invoice-table").wrap('<div class="x-scroll"></div>'),$(function(e){var o=e("#scrollup");e(window).scroll(function(){o["fade"+(100<e(this).scrollTop()?"In":"Out")](600)})}),$("#scrollup").on("click",function(){return $("body,html").animate({scrollTop:0},800),!1}),$("#cont-shop-invoices h1").length){var i=function(e){for(var o in e)$(o).attr("title",$(o).val()).addClass("material-icons").val(e[o])};$("#cont-shop-invoices h1 + table").addClass("status_table").after('<div class="fil_togg_wrapper"><div class="fil_togg_holder"><span class="material-icons">storage</span><span class="material-icons arrow">keyboard_arrow_down</span></div></div>').siblings("table, hr").addClass("filter_table");var n={"#invoice-form-export":"file_download","#invoice-form-print":"print","#invoice-form-send-el-goods":"forward"};i(n),$(document).ajaxComplete(function(){i(n)}),$(".fil_togg_holder").on("click",function(){var e=$(this).children(".arrow");$(".filter_table").fadeToggle(),e.text("keyboard_arrow_up"==e.text()?"keyboard_arrow_down":"keyboard_arrow_up")})}}),window.WebFontConfig={google:{families:["Fira+Sans+Condensed:400,600,700&amp;subset=cyrillic"]},active:nNmenu};