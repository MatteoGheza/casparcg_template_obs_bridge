import { io } from "socket.io-client";

var socket = io("http://127.0.0.1:5000");
socket.on('connect', function () {
    socket.emit('template_connect', {
        templateName: window.templateName ? window.templateName : location.pathname.substring(location.pathname.lastIndexOf('/') + 1),
        href: location.href
    });
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
    if (typeof (update) === "function") {
        update(data);
    } else {
        socket.emit('error', 'update function not found');
    }
});