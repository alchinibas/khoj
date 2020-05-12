// -----------consoleArea-------------------
//-------------consoleArea-End----------------
var staticClickVar=0;
var staticKeyVar;
if(document.cookie){
	var cookies=document.cookie.split(";");
	console.log(cookies.length)
}
var recact=document.getElementById("textInput");
recact.addEventListener("focusout",hiderecommend,false);
recact.addEventListener("focus",showrecommend,false);
function showrecommend(){
    document.getElementById("recommend1").style.display="block";
}
function hiderecommend(){
    document.getElementById("recommend1").style.display="none";
}
document.getElementById("bgimage").oninput=setbgcookie;
function setbgcookie(){
	document.cookie="name=background; file=khoj_logo.png; expire=16 Apr 2020 12:00:00 UTC; path=/";
	document.cookie="file=khoj_logo.png; expires=16 Apr 2020 12:00:00 UTC; path=/";
}
window.onclick=function(){
	staticClickVar+=1;
	if(staticClickVar>2){
		hideDrop();
	}
}
window.onkeyup=function(e){
	staticKeyVar=e.keyCode?e.keyCode:e.which;
	if(staticKeyVar==27){
		if(staticClickVar1==1){
			var covers=document.getElementsByClassName("cover1");
			for(var tmp2=0;tmp2<covers.length;tmp2++){
				covers[tmp2].classList.remove("feedbackShow");
				covers[tmp2].classList.add("feedbackHide");
			}
			scrolleffects();
			staticClickVar==0;
		}
	}
}
document.getElementById("bgmode").addEventListener("touchend",changebg,false);
document.getElementById("bgmode").addEventListener("click",changebg,false);

var itmHeaderContainer=document.getElementsByClassName("custom-container")[0];
var itmRecommendArea=document.getElementsByClassName("recommend-area")[0];
var itmResultArea=document.getElementsByClassName("result-area")[0];
var itmUrlArea=document.getElementsByClassName("url-area")[0];

var dropDowns=document.getElementsByClassName("dropdown-menu");
var dropOption=document.getElementsByClassName("option-group");
for(var tmp2=0;tmp2<dropDowns.length;tmp2++){
	staticClickVar=dropDowns[tmp2].onclick=toggleMenu;
	staticClickVar=dropDowns[tmp2].addEventListener("touchend",toggleMenu,false);
	staticClickVar=dropOption[tmp2].onclick=toggleMenu;
	staticClickVar=dropOption[tmp2].addEventListener("touchend",toggleMenu,false);
	staticClickVar=dropOption[tmp2].onfocusout=hideDrop;
}
function changebg(){
	var body=document.body;
	if(this.getAttribute("data-target")=="night"){
		body.classList.remove("bglight1");
		body.classList.add("bgdark2");
		itmHeaderContainer.classList.add("bgdark3");
		itmResultArea.classList.add("bglight2");
		itmRecommendArea.classList.add("bglight2");
		itmResultArea.classList.remove("bglight1");
		itmHeaderContainer.classList.remove("bglight3");
		itmRecommendArea.classList.remove("bglight1");
		
		this.setAttribute("data-target","day")
		this.innerHTML="Day Mode";

	}
	else{
		body.classList.add("bglight1");
		itmResultArea.classList.add("bglight1");
		itmHeaderContainer.classList.add("bglight3");
		itmRecommendArea.classList.add("bglight1");
		itmHeaderContainer.classList.remove("bgdark3");
		itmResultArea.classList.remove("bglight2");
		itmRecommendArea.classList.remove("bglight2");
		body.classList.remove("bgdark2");
		
		this.setAttribute("data-target","night");
		this.innerHTML="Night Mode";
	}
}
function hideDrop(){
	for(var tmp3=0;tmp3<dropDowns.length;tmp3++){
		var main=dropDowns[tmp3];
		var arr=main.getAttribute("class").split(" ");
		if(arr.includes("show")){
			main.classList.remove("show");
			main.classList.add("hide");
		}
	}
}
function toggleMenu(){
	var arr=this.getAttribute("class").split(" ");
	if(arr.includes("option-group")){
		var node=this.children[1];
		var main=node;
		arr=main.getAttribute("class").split(" ");
	}
	else{
		var main=this;
	}
	if(arr.includes("hide")){
		main.classList.remove("hide");
		main.classList.add("show")
		return staticClickVar=1;
	}
	else{
		main.classList.remove("show");
		main.classList.add("hide");
		return staticClickVar=0;
	}	
}

window.onload=initializer;
window.onresize=resize;
window.onscroll=scrolleffects;
var staticClickVar=0;
var closer=document.getElementsByClassName("close");
for(var c1=0;c1<closer.length;c1++){
	closer[c1].addEventListener("click",closefn,false);
	closer[c1].addEventListener("touchend",closefn,false);
}
staticClickVar1=document.getElementsByClassName("feedback-button")[0].addEventListener("click",openfn,false);
staticClickVar1=document.getElementsByClassName("feedback-button")[0].addEventListener("touchend",openfn,false);

function openfn(){
	var block=this.getAttribute("data-target");
	var ele=document.getElementById(block);
	if(ele==undefined)ele=this;
	ele.classList.remove("feedbackHide");
	ele.classList.add("feedbackShow");
	ele.style.zIndex="2008";
	scrolleffects();
	return staticClickVar1=1;
}
function closefn(){
	var block=this.getAttribute("data-dismiss");
	var ele=document.getElementById(block);
	if(ele==undefined){
		ele=this;

	}
	ele.classList.remove("feedbackShow");
	ele.classList.add("feedbackHide");
	scrolleffects();
	return staticClickVar1=2;
}
function scrolleffects(){
	if(document.getElementsByClassName("feedbackShow").length!=0){
		document.body.style.overflow="hidden";
	}
	else{
		document.body.style.overflow="auto";
	}
}
var resizeStaticVar=-1;
function resize(){
	document.getElementById("fluid").style.height=window.screen.height+"px";
	var fdform=document.getElementById("feedbackForm");
	fdform.style.top=window.screen.height/2+"px";
	fdform.style.transform="translate(-50%,-80%)";
	if(document.body.offsetWidth<=576){
		if(resizeStaticVar!=1){
			var rows=document.getElementsByClassName("ff");
			var result=document.getElementsByClassName("result-area")[0];
			var recommend=document.getElementsByClassName("recommend-area")[0];
			for(var row=0;row<rows.length;row++){
				rows[row].style.display="none";
				result.classList.add("order-first");
				result.classList.add("order-last");
			}
			/*--------------dropoption-----------------*/
			var drop=document.getElementsByClassName("option-group");
			for(var tmp1=0;tmp1<drop.length;tmp1++){
				var menuid=drop[tmp1].getAttribute("data-target");
				var menuW=document.getElementById(menuid);
				var shift=drop[tmp1].getBoundingClientRect().width;
				menuW.style.transform="translate(0,-2px)";
				menuW.style.left=0+"px";
			}
			/*--------------dropoption-----------------*/
			resizeStaticVar=1;
		}
	}
	else{
		if(resizeStaticVar!=0){
			var rows=document.getElementsByClassName("ff");
			var result=document.getElementsByClassName("result-area")[0];
			var recommend=document.getElementsByClassName("recommend-area")[0];
			resizeStaticVar=0;
			for(var row=0;row<rows.length;row++){
				rows[row].style.display="inline-block";
				result.classList.remove("order-first");
				result.classList.remove("order-last");
			}
			/*--------------dropoption-----------------*/
			var drop=document.getElementsByClassName("option-group");
			for(var tmp1=0;tmp1<drop.length;tmp1++){
				var menuid=drop[tmp1].getAttribute("data-target");
				var menuW=document.getElementById(menuid);
				var shift=drop[tmp1].getBoundingClientRect().width;
				menuW.style.transform="translate(-100%,-2px)";
				menuW.style.left=shift+"px";
			}
			/*--------------dropoption-----------------*/
		}
	}
}
function initializer(){
		resize();
		var deviceHeights=document.getElementsByClassName("device-height");
		var i=0;
		var height=0;
		for(i=0;i<deviceHeights.length;i++){
			height=parseInt(deviceHeights[i].getAttribute("data-heightp"));
			if(!height)height=60;
			deviceHeights[i].style.minHeight=window.screen.height*height/100+"px";
		}
	}
