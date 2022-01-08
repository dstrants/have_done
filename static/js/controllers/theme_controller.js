import { Controller } from "stimulus"
import Cookies from 'js-cookie'

export default class extends Controller {
  static targets = [ "switch" ]

  connect(){
    this.checkBlur()
      this.checkTheme()
  }

  checkTheme(){
    if( Cookies.get('dark') == 'true' ) {
        this.body.classList.add('c-dark-theme')
    }
  }

  checkBlur(){
    if( Cookies.get('blur') == 'true') {
      var vals  = document.querySelectorAll('.price')
      vals.forEach( (el) => {
        el.classList.add('blur')
      })
    }
  }
  
  switchTheme(){
    this.body.classList.toggle('c-dark-theme')
    Cookies.set('dark', this.body.classList.contains('c-dark-theme'))
  }

  
  blurPrices(){
    var vals  = document.querySelectorAll('.price')
    vals.forEach( (el) => {
      el.classList.toggle('blur')
    })
    Cookies.set('blur', Cookies.get('blur') == 'true' ? 'false' : 'true')
  }

  get body(){
      return document.querySelector('body')
  }
}