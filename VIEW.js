var row = (event) => {
	targets = document.querySelectorAll("td." + event.target.classList[0])
	targets.forEach(tg=>{
		tg.classList.toggle("row_hide")
	})
}

var colmun = (event) => {
	targets = document.querySelectorAll("." + event.target.classList[2])
	targets.forEach(tg=>{
		tg.classList.toggle("colmun_hide")
	})
}

console.log("register event listner")

document.querySelectorAll("th").forEach(header => {header.addEventListener("click",row)})
document.querySelectorAll("td").forEach(item_id => {item_id.addEventListener("click",colmun)})