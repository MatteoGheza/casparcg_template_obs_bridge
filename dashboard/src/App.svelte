<script>
import { Styles, Form, FormGroup, InputGroup, Input } from 'sveltestrap';
import TrashCan from "svelte-material-icons/TrashCan.svelte";
import { fade } from 'svelte/transition';
import { socket, waitSocketConnection } from './store';
import UpdateDataEditor from './components/UpdateDataEditor.svelte';

let innerWidth;
let reloadAfterStop = true;

let showUpdateDataEditor = false;

let clients = [];
socket.on('clients', (new_clients) => {
    clients = new_clients;
    console.log("clients", clients);
});

let update_sets = [];
socket.on('update_sets', (new_update_sets) => {
    update_sets = new_update_sets;
    console.log("update_sets", update_sets);
});

waitSocketConnection.then(() => {
    socket.emit('request_clients');
    socket.emit('request_update_sets');
});

function play(sid) {
    socket.emit('template_play', sid);
}

function stop(sid) {
    socket.emit('template_stop', sid);
    console.log("reloadAfterStop", reloadAfterStop);
    if(reloadAfterStop) {
        setTimeout(() => {
            socket.emit('template_reload', sid);
        }, 3000);
    }
}

function update(sid) {
    let data = getUpdateSetDataBySid(sid);
    let obj = {};
    data.forEach((el) => { obj[el.key] = el.value; });

    console.log("update", sid, obj);
    socket.emit('template_update', sid, obj);
}

let selectedUpdateSets = {};

function getUpdateSetDataBySid(sid) {
    let value = [];

    Object.keys(selectedUpdateSets).forEach((current_sid) => {
        if(current_sid === sid) {
            value = update_sets[Object.keys(update_sets).find((name) => selectedUpdateSets[current_sid] === name)];
        }
    });

    return value;
}

function handleUpdateEditorSubmit(event) {
    showUpdateDataEditor = false;

    let name = event.detail.name;
    let data = event.detail.data;

    console.log("handleUpdateEditorSubmit", name, data);
    socket.emit('add_update_set', name, data);
}

function remove_update_set(name) {
    socket.emit('remove_update_set', name);
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
                    <Input checked type="switch" label="Reload template page after stop" on:change={() => { reloadAfterStop = !reloadAfterStop; }} />
                </FormGroup>
            </Form>

            {#if innerWidth >= 630}
            <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3 mt-2">
                {#each Object.entries(clients) as [sid, client]}
                <div class="col">
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">{sid}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{client.templateName}</h6>
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <InputGroup>
                                    <Input type="select" bind:value={selectedUpdateSets[sid]}>
                                        <option selected disabled></option>
                                        {#each Object.entries(update_sets) as [name, data]}
                                        <option>{name}</option>
                                        {/each}
                                    </Input>
                                    <button on:click={() => { showUpdateDataEditor = true; }} type="button" class="btn btn-outline-primary">Add</button>
                                </InputGroup>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="btn-group">
                                    <button on:click={() => { update(sid); }} type="button" class="btn btn-md btn-outline-primary">Update</button>
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
            <table class="table mt-2">
                <tbody>
                    {#each Object.entries(clients) as [sid, client]}
                    <tr>
                        <td><b>{client.templateName}</b></td>
                        <td class="sid-column">{sid}</td>
                        <td>
                            <div class="btn-group">
                                <button on:click={() => { play(sid); }} type="button" class="btn btn-md btn-outline-success">Play</button>
                                <button on:click={() => { stop(sid); }} type="button" class="btn btn-md btn-outline-danger">Stop</button>
                            </div>
                        </td>
                    </tr>
                    {/each}
                </tbody>
            </table>
            {/if}

            {#if showUpdateDataEditor}
            <div transition:fade class="mt-2">
                <UpdateDataEditor on:submit={handleUpdateEditorSubmit} />
            </div>
            {/if}
        </div>
    </div>

    {#if innerWidth >= 630}
    <div class="container mt-2">
        <h4>Update sets:</h4>
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                    <td>Name</td>
                    <td>Data</td>
                    <td>Remove</td>
                </tr>
            </thead>
            <tbody>
                {#each Object.entries(update_sets) as [name, data]}
                <tr>
                    <td>{name}</td>
                    <td>
                        <table class="table mt-2">
                            <tbody>
                                {#each data as {key,value}}
                                <tr>
                                    <td><b>{key}</b></td>
                                    <td>{value}</td>
                                </tr>
                                {/each}
                            </tbody>
                        </table>
                    </td>
                    <td>
                        <button on:click={() => { remove_update_set(name); }} type="button" class="btn btn-md btn-outline-success">
                            <TrashCan size="1.5em" />
                        </button>
                    </td>
                </tr>
                {/each}
            </tbody>
        </table>
    </div>
    {/if}
</main>
