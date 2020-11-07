//feedback form-----------------


//feedback form ends -----------------


// -----------consoleArea-------------------
var staticrec = 0;
var blurout = 0;
var rec1 = document.getElementById("recommend1");
var sinput = document.getElementById("textInput");
$("#recommend1").on("click touchend",".recommend-item",function(){
    var rt = $(this).text();
    sinput.value = rt;

});
//staticrec = rec1.addEventListener("mouseout",function(){return staticrec = 0;},false);

staticrec = sinput.addEventListener("focus",showrecommend,false);
staticrec = sinput.addEventListener("blur",function(){return staticrec= 0;},false);
if(staticrec==0){
    staticrec=rec1.addEventListener("mouseover",function(){return staticrec = 1;},false);
}
function showrecommend(){
    rec1.style.display="block";
    return staticrec = 1;
}
function hiderecommend(){
    rec1.style.display="none";
}
//-------------consoleArea-End----------------
var staticClickVar=0;
var staticKeyVar;
document.getElementById("bgimage").addEventListener("input",setbgcookie,false)
function setbgcookie(){
	document.cookie="name=background; file=khoj_logo.png; expire=16 Apr 2020 12:00:00 UTC; path=/";
	document.cookie="file=khoj_logo.png; expires=16 Apr 2020 12:00:00 UTC; path=/";
}
window.onclick=function(){
	staticClickVar+=1;
	if(staticClickVar>2){
		hideDrop();
	}
    if(staticrec == 0){
        hiderecommend();
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
var staticClickVar=0;

var resizeStaticVar=-1;
function resize(){
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
