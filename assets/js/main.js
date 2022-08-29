let $ = (selector) => document.querySelector(selector);
$('#form').addEventListener('submit', async (e)=>{
  console.log(e);
  e.preventDefault();
  let p = await axios.post('http://127.0.0.1:5555/search', {'query':`${$('#spotifySearch').value}`})
  console.log(p.data)
  let index = 0;
  for (i of p.data.tracks.items) {
    index++
    if (index <= 10) {
      $(`#albumartimg${index}`).src = i.album.images[1].url
      $(`#trackTitle${index}`).innerHTML = i.name
    }
  }
  return true;
});
