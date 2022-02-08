<script>
import { Form, FormGroup, InputGroup, Input } from 'sveltestrap';
import { createEventDispatcher } from 'svelte';

let name;
let data = [{ key: "", value: "" }];

async function handleAdd() {
  data = [...data, { key: "", value: "" }];
  console.log(data);
}

const dispatch = createEventDispatcher();

async function handleSave() {
    console.log(name, data);
    dispatch('submit', {name, data});
}
</script>

<div class="border">
    <Form class="m-3">
        <FormGroup>
            <Input placeholder="Update name" bind:value={name} />
        </FormGroup>
        <FormGroup>
            {#each data as {key, value}, index}
            <InputGroup>
                <Input bind:value={key} placeholder="f{index}" />
                <Input bind:value={value} placeholder="value{index}" />
            </InputGroup>
            {/each}
        </FormGroup>
        <FormGroup>
            <button on:click|preventDefault={handleAdd} type="button" class="btn btn-outline-primary">Add</button> <button on:click|preventDefault={handleSave} type="button" class="btn btn-outline-success">Save</button>
        </FormGroup>
    </Form>
</div>