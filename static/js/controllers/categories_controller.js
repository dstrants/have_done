import { Controller } from "stimulus"
import Noty from 'noty';
import { Picker } from 'emoji-picker-element';
import Mousetrap from 'mousetrap';

Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
  static targets = []

  connect(){
      this.refreshCategories()
      Mousetrap.bind('esc esc', () => this.refreshCategories())
  }

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

  refreshCategories(){
    const cats = document.querySelector("#categories")
    fetch("/prod/categories/partial")
      .then( response => response.text() )
      .then( data => cats.innerHTML = data)
  }

  createEmojiPicker(event) {
    var picker = new Picker();
    event.target.appendChild(picker);
    document.addEventListener('keypress', event => {console.log(event); if (event.key == 27) picker.classList.add("hidden")} )
    picker.addEventListener('emoji-click', event => this.updateEmoji(event))
  }

  showEmojiPicker(event){
    var picker  = event.target.querySelector("emoji-picker")
    if (picker == null){
        return this.createEmojiPicker(event)
    }
    picker.classList.toggle("hidden")
  }

  updateEmoji(event){
      console.log("Event Target: " + event.target)
      event.target.value = event.detail.unicode
      event.keyCode = 13
      console.log(event.target.value)
      console.log(event.keyCode)
      this.saveField(event)
  }

  updateView(event) {
    const el = event.target
    const categoryId = el.parentElement.dataset.categoryId
    const field = el.dataset.field
    el.removeAttribute('data-action')
    fetch(`update/template/${categoryId}/${field}`)
    .then( response => response.text())
    .then( data => {
      el.innerHTML = data
    })
  }

  saveField(event){
    if (event.keyCode != 13) return null
    const el = event.target
    const newValue = el.value
    const categoryId = el.parentElement.parentElement.dataset.categoryId
    const field = el.parentElement.dataset.field
    const updateLink = `/prod/categories/fu/${categoryId}/${field}/${newValue}`

    fetch(updateLink,
      {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then( data => {
      setTimeout( ()  =>{
        new Noty ({ text: data.message, type: data.result ? "success":"danger" }).show()
      }, 250)
    })
    setTimeout( () => this.refreshCategories(), 250)
  }

  createNewCategory(){
    fetch('/prod/categories/new', {method: "POST", headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
      .then(response => response.json())
      .then(data => {
        setTimeout( ()  =>{
          new Noty ({ text: "New project has been created", type: data.result ? "success":"danger" }).show()
        }, 250)
      })
    setTimeout( () => this.refreshCategories(), 250)
  }

  deleteCategory(event){
    const initialEl = event.target
    const el = initialEl.nodeName == 'A' ? initialEl : initialEl.closest('li')
    const categoryId = el.dataset.categoryId
    fetch(`/prod/categories/delete/${categoryId}`, {method: "POST", headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then(data => {
      setTimeout( ()  =>{
        new Noty ({ text: "Category has been deleted", type: data.result ? "success":"danger" }).show()
      }, 250)
    })
  setTimeout( () => this.refreshCategories(), 250)
  }
}