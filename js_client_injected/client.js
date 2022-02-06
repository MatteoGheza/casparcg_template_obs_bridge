import { io } from "socket.io-client";

var socket = io("http://127.0.0.1:5000");
socket.on('connect', () => {
    let data = {
        templateName: window.templateName ? window.templateName : location.pathname.substring(location.pathname.lastIndexOf('/') + 1),
        href: location.href
    };
    if(typeof localStorage.getItem('template_id') === "string") {
        data.id = localStorage.getItem('template_id');
    }
    socket.emit('template_connect', data);
});

socket.on('new_template_id', (new_id) => {
    localStorage.setItem('template_id', new_id);
});

socket.on('play', () => {
    if (typeof (play) === "function") {
        play();
    } else if (typeof (playAnimation) === "function") {
        playAnimation();
    } else {
        socket.emit('error', 'play function not found');
    }
});

socket.on('stop', () => {
    if (typeof (stop) === "function") {
        stop();
    } else if (typeof (stopAnimation) === "function") {
        stopAnimation();
    } else {
        socket.emit('error', 'stop function not found');
    }
});

socket.on('update', (data) => {
    console.log("received update", data);
    if (typeof (update) === "function") {
        update(JSON.stringify(data));
    } else {
        socket.emit('error', 'update function not found');
    }
});