const qr = new QRCode(document.getElementById('qrcode'), {
    width: 256,
    height: 256,
    colorDark : '#4995be',
    colorLight : '#fff',
    correctLevel : QRCode.CorrectLevel.Q,
});

function generateQr(url){
    qr.clear();
    qr.makeCode(url);
}

const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
const ws = new WebSocket(`${protocol}://${location.host}/ws`);


ws.onmessage =  (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'qr')
        generateQr(data.url);
    else if (data.type === 'error')
        window.alert(data.message);
    else if (data.type === 'connection') {
        if (data.status === 'connected')
            location.replace("/");
        else
            window.alert("Unable to login");
    }
}
