let $ = (selector) => document.querySelector(selector);
$('#form').addEventListener('submit', async (e)=>{
  console.log(e);
  e.preventDefault();
  return true;
});
