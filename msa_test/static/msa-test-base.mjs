export class HTMLMsaTestBaseElement extends HTMLElement {

	connectedCallback(){
		this.initContent()
		this.initActions()
	}

	getHtml(){
		return `
			<div style="display:flex; flex-direction:row; align-items: center; border: solid 1px grey; padding: .5em">
				<button class="test_me">Test me !</button>
				<span class="counter" style="margin-left: .5em"></span>
			</div>
		`
	}

	initContent(){
		const shdw = this.attachShadow({ mode: 'open' })
		shdw.innerHTML = this.getHtml()
		this.sync()
	}

	initActions(){
		this.shadowRoot.querySelector(".test_me").onclick = () => { this.postTest() }
	}

	postTest(){
		fetchJson('/msa/test/base/counter', {
			method: "POST"
		})
		.then(() => this.sync())
	}

	async sync(){
		const res = await fetchJson('/msa/test/base/counter')
		this.shadowRoot.querySelector(".counter").textContent = res.counter
	}
}
customElements.define("msa-test-base", HTMLMsaTestBaseElement)

// utils

async function fetchJson(...args) {
	const res = await fetch(...args)
	return await res.json()
}