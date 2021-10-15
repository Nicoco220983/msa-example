export class HTMLMsaTestDbElement extends HTMLElement {

	connectedCallback(){
		this.initContent()
		this.initActions()
	}

	getHtml(){
		return `
			<div style="display:inline-flex; flex-direction:row; align-items: center; border: solid 1px grey; padding: .5em">
				<input type="text" class="id" style="margin-right: .5em" value="test" />
				<input type="number" class="value" style="margin-right: .5em" />
			</div>
		`
	}

	initContent(){
		const shdw = this.attachShadow({ mode: 'open' })
		shdw.innerHTML = this.getHtml()
		this.sync()
	}

	initActions(){
		this.shadowRoot.querySelector(".id").oninput = () => this.sync()
		this.shadowRoot.querySelector(".value").oninput = () => this.post()
	}

	post(){
        const shdw = this.shadowRoot
        const _id = shdw.querySelector(".id").value
        const value = shdw.querySelector(".value").value
		fetchJson(`/msa/test/db/${_id}`, {
			method: "POST",
            json: { value }
		})
		.then(() => this.sync())
	}

	async sync(){
        const shdw = this.shadowRoot
        const _id = shdw.querySelector(".id").value
		const res = await fetchJson(`/msa/test/db/${_id}`)
		shdw.querySelector(".value").value = res.data.value
	}
}
customElements.define("msa-test-db", HTMLMsaTestDbElement)

// utils

async function fetchJson(url, args) {
    if(args && args.json){
        args.headers = args.headers || {}
        args.headers['Content-Type'] = 'application/json'
        args.body = JSON.stringify(args.json)
        delete args.json
    }
	const res = await fetch(url, args)
	return await res.json()
}