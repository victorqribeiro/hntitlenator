const $ = _ => document.querySelector(_)
const $c = _ => document.createElement(_)
const init = async _ => {
	let request = await fetch('js/words_vector_plus1.json')
	let words = await request.json()
	request = await fetch('js/nn.json')
	let data = await request.json()
	const nn = new Dejavu()
	nn.load( data )
	console.log( nn )
	const divForm = $c('div')
	const inp = $c('input')
	inp.placeholder = 'Title'
	const btn = $c('button')
	btn.innerText = 'Ok'
	btn.addEventListener('click', e => {
		const final = Array(20).fill(0)
		const tmp = inp.value.match(/\w+/g).filter(w=>!/\d/.test(w)).map(w=>w in words?words[w]:0)
		for(let i = 0; i < tmp.length; i++)
			final[i] = tmp[i]
		status.innerText = nn.predict(final).data
	})
	divForm.appendChild( inp )
	divForm.appendChild( btn )
	const status = $c('div')
	$('#main').innerHTML = ''
	$('#main').appendChild( divForm )
	$('#main').appendChild( status )

}
window.onload = _ => init()
