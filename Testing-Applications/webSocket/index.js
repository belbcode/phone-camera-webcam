//https://reactnative.dev/docs/network#websocket-support

document.getElementById('button').addEventListener('click', () => {


    const url = 'ws://127.0.1.1:5050'
    webSocket = new WebSocket(url)


    webSocket.addEventListener('open', (event)=> {
        console.log('connection opened')
        // webSocket.send("12345678")
    })
    webSocket.addEventListener('message', (event) => {
        console.log('Message from server ', event.data);
    });

    // const timeOut = setInterval(() => {
    //     webSocket.send("I am pinging you every second")
    // }, 1000);


    // document.getElementById('stop-button').addEventListener('click', ()=> {
    //     console.log("stopping connection")
    //     clearInterval(timeOut)
    //     webSocket.send("!DISCONNECT")
    // })


})