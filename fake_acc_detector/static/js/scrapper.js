function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}
function scrapper(){
    document.getElementById("output1").innerHTML='';
    document.getElementById("output").innerText="";
    document.getElementById("load").innerHTML='<div id="loading"></div>';
    document.getElementById("output").innerText="Collecting data ...";
    sleep(500).then(() => {
        document.getElementById("output").innerText="Populating data ...";
    });
    sleep(1000).then(() => {
        document.getElementById("output").innerText="Predicting Account...";
    })
    const url=document.getElementById("account").value;
    data={'input':url}
    console.log(data)
    fetch("/datacollector", {
    method: "POST", 
    headers: new Headers({'content-type': 'application/json'}),
    body: JSON.stringify(data)
    }).then(res => {
    return res.text().then((data) => {
            document.getElementById("output1").innerHTML=data;
            document.getElementById("load").innerHTML="";
        })
    });
}