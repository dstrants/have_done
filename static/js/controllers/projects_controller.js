import { Controller } from "stimulus"
import Noty from 'noty';
import Mousetrap from 'mousetrap';


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
  static targets = []

  connect() {
    this.refreshProjects()
    Mousetrap.bind('esc esc', () => this.refreshProjects())
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

  refreshProjects(){
    const projects = document.querySelector("#projects")
    fetch("/prod/projects/partial")
      .then( response => response.text() )
      .then( data => projects.innerHTML = data)
  }

  updateView(event) {
    const el = event.target
    const projectId = el.parentElement.dataset.projectId
    el.removeAttribute('data-action')
    fetch(`update/template/${projectId}`)
    .then( response => response.text())
    .then( data => {
      el.innerHTML = data
    })
  }

  toggleActive(event){
    const status = event.target.checked ? 1 : 0
    const pid = event.target.closest('li').dataset.projectId
    const updateLink = `/prod/projects/fu/${pid}/is_active/${status}`
    fetch(updateLink,
      {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then( data => {
      setTimeout( ()  =>{
        new Noty ({ text: data.message, type: data.result ? "success":"danger" }).show()
      }, 250)
    })
  }

  updateItemColor(event) {
    const tr = event.target.parentElement.parentElement
    // Update color of the row
    for (let el of tr.children){
        el.style.color = event.target.value
    }
    // Update label value
    event.target.nextElementSibling.innerText = event.target.value
  }

  saveColor(event){
    var anchor = event.target
    while (!(anchor instanceof HTMLAnchorElement)){
        anchor = anchor.parentElement
    }
    // Color Value
    const color = anchor.parentElement.querySelector("[type=color]").value
    const pid = anchor.parentElement.parentElement.dataset.projectId
    const updateLink = `/prod/projects/fu/${pid}/color/${color.split("#").join('')}`
    fetch(updateLink,
      {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then( data => {
      setTimeout( ()  =>{
        new Noty ({ text: data.message, type: data.result ? "success":"danger" }).show()
      }, 250)
    })
  }

  saveName(event){
    if (event.keyCode != 13) return null
    const newName = event.target.value
    const projectId = event.target.parentElement.parentElement.dataset.projectId
    const updateLink = `/prod/projects/fu/${projectId}/name/${newName}`

    fetch(updateLink,
      {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then( data => {
      setTimeout( ()  =>{
        new Noty ({ text: data.message, type: data.result ? "success":"danger" }).show()
      }, 250)
    })
    setTimeout( () => this.refreshProjects(), 250)
  }

  createNewProject(){
    fetch('/prod/projects/new', {method: "POST", headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
      .then(response => response.json())
      .then(data => {
        setTimeout( ()  =>{
          new Noty ({ text: "New project has been created", type: data.result ? "success":"danger" }).show()
        }, 250)
      })
    setTimeout( () => this.refreshProjects(), 250)
  }

  deleteProject(event){
    const initalEl = event.target
    const el = initalEl.nodeName == 'A' ? initalEl : initalEl.closest('li')
    const projectId = el.dataset.projectId
    fetch(`/prod/projects/delete/${projectId}`, {method: "POST", headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then(data => {
      setTimeout( ()  =>{
        new Noty ({ text: "Project has been deleted", type: data.result ? "success":"danger" }).show()
      }, 250)
    })
  setTimeout( () => this.refreshProjects(), 250)
  }
}