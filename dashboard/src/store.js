import io from 'socket.io-client';
import { SOCKET_ENDPOINT } from './constants';

export const socket = io(SOCKET_ENDPOINT);

export const waitSocketConnection = new Promise((resolve, reject) => {
    socket.on('connect', () => {
        resolve();
    });
});
