import { Controller } from "stimulus"
import { createPopper } from '@popperjs/core';
import Noty from 'noty';


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
  static targets = ["addonCard"]

  show(){
    if (this.hasAddonCardTarget){
        this.addonCardTarget.classList.remove('hidden')
    }
    else{
      fetch(this.element.dataset.url)
        .then( (response) => response.text())
        .then( (html) => {
          const fragment = document.createRange()
                                  .createContextualFragment(html);
          this.element.appendChild(fragment)
          createPopper(this.element, this.addonCardTarget, {
              placement: 'top'
          })          
        })
        .catch( (error) => {
          console.log(error)
        })
    }
   }

   hide(){
    if (this.hasAddonCardTarget){
        this.addonCardTarget.classList.add('hidden')
    }
   }

   disconnect() {
    if (this.hasAddonCardTarget) {
      this.addonCardTarget.remove();
    }
  }
}