let $ = (selector) => document.querySelector(selector);
var buttonList = []
async function addToQueue(e) {
  e.innerHTML = "Adding to queue..."
  e.disabled = true;
  let r = await axios.post('http://127.0.0.1:5555/queue', {'uri' : e.dataset.uri})
  if (r.status == 200) {
    e.innerHTML = "Added to queue"
    e.disabled = true;
    for (i of buttonList){
      i.disabled = true;
    }
  }
  return true
}
$('#form').addEventListener('submit', async (e)=>{
  console.log(e);
  e.preventDefault();
  let p = await axios.post('http://127.0.0.1:5555/search', {'query':`${$('#spotifySearch').value}`})
  console.log(p.data)
  let index = 0;
  $('#search_box').innerHTML = '';
  for (i of p.data.tracks.items) {
    index++
    let div = document.createElement('div');
    let albumart = document.createElement('div');
    let albumartimg = document.createElement('img');
    let titleCard = document.createElement('div');
    let titleCardText = document.createElement('span');
    let queueButtondiv = document.createElement('div');
    let queueButton = document.createElement('button');

    titleCard.className = 'titleCard';
    queueButtondiv.className = 'addtoqueue';
    queueButton.className = 'addtoqueuebtn';
    queueButton.style.width = '100%';
    queueButton.dataset.uri = i.uri
    queueButton.onclick = (e) => {addToQueue(e.srcElement)}
    buttonList.push(queueButton)
    albumart.className = 'albumart';
    titleCardText.innerHTML = i.name;
    titleCardText.style.fontSize = 'small';
    albumartimg.src = i.album.images[1].url;
    queueButtondiv.appendChild(queueButton);
    titleCard.appendChild(titleCardText);
    albumart.appendChild(albumartimg);
    queueButton.innerHTML = 'Add to queue';
    div.appendChild(albumart);
    div.appendChild(titleCard);
    div.appendChild(queueButtondiv);
    div.className = 'column-4';
    $('#search_box').appendChild(div);
  }
  console.log(buttonList)
  $('#searchResults').hidden = false;
  return true;
});
//async function getQueue(){
//  let queue = await axios.get('http://127.0.0.1:5555/queue')
//  for (i of queue.data.queue){
//    li = document.createElement('li');
//    li.innerHTML = `${i.name} - ${i.artists[0].name}`
//    $('#qlist').appendChild(li);
//  }
//  return queue.data
//}
