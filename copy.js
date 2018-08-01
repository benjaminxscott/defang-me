<button onclick="copyToClipboard()">Copy to Clipboard</button>

<script>
function copyToClipboard()
{
 var copyText = document.getElementById("defanged_text");

  /* Select the text field */
  copyText.select();

  /* Copy the text inside the text field */
  try
  {
      document.execCommand("copy");
  }
  catch(err)
  {
      console.log('copy did not work')
  }
    
}
</script>