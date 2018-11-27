var except=new Array();
function replaceelem()
{
	num=Math.floor((Math.random()*1000)%item.length);
	$(".result").empty();
	$(".result").text(item[num]);
}
$(".begin").click(function(){
	time=setInterval(replaceelem,20);
});
$(".end").click(function(){
	clearInterval(time);
	if(except.indexOf(num)>=0)
	{
		while(except.indexOf(num)>=0)
		{
			num=(num+1)%item.length;
		}
		except.push(num);
		$(".result").empty();
	    $(".result").text(item[num]);
		console.log(num);
	}
	else
	{
		except.push(num);
		console.log(num);
	}
});

// 下面是要返回给我的数据
// 数据格式是一个二维数组，二维数组的长度代表一共有多少个结果
// 每一个一维数组的第一个元素为图片的地址,第二个为商品详情页面的地址。
arr=null;
var index=0;
// 获取两个元素
image=document.getElementById("image");
link=document.getElementById("link");
// 改变元素
function changeelem(src,url)
{
    image=document.getElementById("image");
    link=document.getElementById("link");
    image.setAttribute("src",src);
    link.setAttribute("href",url)
}
// 运行函数
function run()
{
    var i=index%arr.length;
    index+=1;
    changeelem(arr[i][0],arr[i][1])
}