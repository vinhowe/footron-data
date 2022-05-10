var img_list = {

    'flowers': 'imgs/byu-sign-flowers.jpeg',
    'cloudy': 'imgs/cloud-y.jpeg',
    'maeser': 'imgs/maeser-flowers.jpeg',
    'tmcb': 'imgs/tmcb-spring.jpeg',
    'valley': 'imgs/valley-sunset.jpeg',
    'winter': 'imgs/winter-campus.jpeg',
    'ymountain': 'imgs/y-mountain.jpeg',

    'ylogo': 'imgs/y-logo.jpeg',
    'basketball': 'imgs/basketball.jpg',

    'congrats': 'imgs/congrats.jpeg',
    'keyboard': 'imgs/keyboard.jpeg',
    'supercomputer': 'imgs/supercomputer.jpeg',

    'suchcongrats': 'imgs/such-congrats.jpeg',
    'kungfu': 'imgs/kung-fu.jpeg',
    'thing': 'imgs/a-thing.jpeg',

};

function messageHandler(message) {
    console.log( "GOT MESSAGE:", message );
    document.getElementById("optxt").style.display = "None";
    document.getElementById("opimg").style.opacity = 1.0;
    document.getElementById("opimg").style.backgroundImage = "url('" + img_list[ message ] + "')";
}

var client;
function start() {
    console.log( "Starting..." );
    client = new FootronMessaging.Messaging();
    client.mount();
    client.addMessageListener(messageHandler);
}

window.addEventListener("load", start);
