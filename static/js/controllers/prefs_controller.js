import { Controller } from "stimulus"
import Noty from 'noty';


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
  static targets = ["toggleInputs", "token", "message"]

  _getCookie(name) {
    if (!document.cookie) {
      return null;
    }
  
    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
  
    if (xsrfCookies.length === 0) {
      return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  }

  providers(event) {
    const checkbox = event.target
    const provider = checkbox.parentElement.parentElement.nextElementSibling
    console.log(provider)
    if (checkbox.checked){
      provider.classList.remove('hidden')
    }
    else{
      provider.classList.add('hidden')
    }
  }

  refreshToken() {
    fetch("/profile/refresh_token")
      .then( response => response.json())
      .then( data => {
        this.token = data.token
        this.showMessage("Token has been refreshed!")
      })
      .catch( () => {
        this.messageTarget.classList.add("text-danger")
        this.showMessage("Something went wrong. Please try again!")
      })
  }

  toggleToken(){
    status = this.tokenTarget.classList.toggle("blur")
    console.log(status)
    if(status == "true"){
      this.showMessage("Token Hidden!")
    }
    else {
      this.showMessage("Token Shown!")
    }
  }

  copyToken() {
    this.tokenTarget.select()
    this.tokenTarget.setSelectionRange(0, 99999)
    document.execCommand("copy")
    this.showMessage("Token Copied to Clipboard!", "text-success")
  }

  showMessage(message) {
    this.message = message
    setTimeout( () => {
      this.message = ""
      this.classList = ['ml-3', 'p-1']
    }, 2500)
  }

  get token() {
    return this.tokenTarget.value
  }

  set token(val) {
    this.tokenTarget.value = val
  }

  set message(mes) {
    this.messageTarget.innerText = mes
  }
  

}