<script>
import { Styles, Form, FormGroup, FormText, Input, Label } from 'sveltestrap';
import { socket, waitSocketConnection } from './store';

let innerWidth;
let reloadAfterStop = true;

let clients = [];
socket.on('clients', (new_clients) => {
    clients = new_clients;
    console.log("clients", clients);
});

waitSocketConnection.then(() => {
    socket.emit('request_clients');
});

function play(sid) {
    socket.emit('template_play', sid);
}

function stop(sid) {
    socket.emit('template_stop', sid);
    if(reloadAfterStop) {
        setTimeout(() => {
            socket.emit('template_reload', sid);
        }, 5000);
    }
}

function update(sid, data) {
    socket.emit('template_update', sid, data);
}
</script>

<style>
@media only screen and (max-width: 500px) {
    .sid-column {
        display: none;
    }
}
</style>

<svelte:window bind:innerWidth={innerWidth} />

<Styles />

<header>
    <div class="navbar navbar-dark bg-dark shadow-sm">
        <div class="container">
            <i class="navbar-brand d-flex align-items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor"
                    stroke-linecap="round" stroke-linejoin="round" stroke-width="2" aria-hidden="true" class="me-2"
                    viewBox="0 0 24 24">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                    <circle cx="12" cy="13" r="4" />
                </svg>
                <strong>CasparCG template OBS bridge</strong>
            </i>
        </div>
    </div>
</header>

<main>

    <div class="album py-5 bg-light">
        <div class="container">
            <Form>
                <FormGroup>
                    <Input checked type="switch" label="Reload template page after stop" bind:value={reloadAfterStop} />
                </FormGroup>
            </Form>

            {#if innerWidth >= 630}
            <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
                {#each Object.entries(clients) as [sid, client]}
                <div class="col">
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">{sid}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{client.templateName}</h6>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="btn-group">
                                    <button on:click={() => { play(sid); }} type="button" class="btn btn-lg btn-outline-success">Play</button>
                                    <button on:click={() => { stop(sid); }} type="button" class="btn btn-lg btn-outline-danger">Stop</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {/each}
            </div>
            {:else}
            <table class="table">
                <tbody>
                    {#each Object.entries(clients) as [sid, client]}
                    <tr>
                        <td><b>{client.templateName}</b></td>
                        <td class="sid-column">{sid}</td>
                        <td>
                            <div class="btn-group">
                                <button on:click={() => { play(sid); }} type="button" class="btn btn-lg btn-outline-success">Play</button>
                                <button on:click={() => { stop(sid); }} type="button" class="btn btn-lg btn-outline-danger">Stop</button>
                            </div>
                        </td>
                    </tr>
                    {/each}
                </tbody>
            </table>
            {/if}
        </div>
    </div>

</main>
