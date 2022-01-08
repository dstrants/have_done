import { Controller } from "stimulus"

const simpleIcons = require('simple-icons');

export default class extends Controller {
    static targets = ['color', 'icon']

    connect(){
        console.log('Connected')
        this.fillIconsInList()
    }

    _generateIconDiv(icon){
      var iconDiv = document.createElement('div')
      iconDiv.style.width = "20px"
      iconDiv.style.display = 'inline-block'
      iconDiv.style.marginRight = '10px'
      iconDiv.innerHTML = icon.svg
      iconDiv.firstElementChild.style.fill = "#" + icon.hex
      return iconDiv
    }

    getIcon(event){
      var icon = simpleIcons.get(event.target.value)
      var iconSpan = document.getElementById("icon_value")
      if (iconSpan.firstElementChild) iconSpan.removeChild(iconSpan.firstElementChild);
      if(icon) {
        const iconDiv = this._generateIconDiv(icon)
        iconSpan.append(iconDiv)
        this.color = icon.hex
      } else{
        this.color = ''
      }
    }


    fillIconsInList() {
      for (const icon of this.iconTargets){

        if (icon.childElementCount) continue

        var iconsvg = simpleIcons.get(icon.dataset.icon)
        if (iconsvg) {
          const iconDiv = this._generateIconDiv(iconsvg)
          icon.append(iconDiv)
          icon.parentElement.style = `border-color: #${iconsvg.hex}`
        }
      }
    }

    get color(){
        this.colorTarget.value
    }

    set color(col){
        return this.colorTarget.value = col
    }

}