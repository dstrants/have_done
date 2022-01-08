import { Controller } from "stimulus"
import {Color, Solver, hexToRgb } from  "../others/hue"
import Noty from 'noty';
import Mousetrap from 'mousetrap';
import { Modal } from '@coreui/coreui'
import flatpickr from 'flatpickr'


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
  static targets = [ "emoji", "project", "category", "projectName", "task", "filterable", "addonCard"]

  connect() {
    this._refreshTasks(this.date)
    Mousetrap.bind('n l',() => {
      var projectModal = this.projectModal
      projectModal.show()
    });
    Mousetrap.bind('n k', () => {
      var categoryModal = this.categoryModal
      categoryModal.show()
    })
    Mousetrap.bind('n t', () => {
      this.taskTarget.focus()
    })
    Mousetrap.bind('esc esc', () => {
      const calendar = document.getElementById('datepicker')
      this._refreshTasks(calendar.value)
    })
    if(this.ctx == 'today'){
      this.renderCalendar()
    }
  }

  renderCalendar() {
    const datepicker = document.getElementById('datepicker')
    const flat = flatpickr(datepicker, {
      onChange: (selectedDates, dateStr, instance) => {
        console.log(dateStr)
        this.date = dateStr
        this._refreshTasks(dateStr)
      },
      defaultDate: (new Date).toISOString().split("T")[0],
      maxDate: 'today'
    })
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

  fixSimpleIconColor(event){
    const element = event.target
    const rgb = hexToRgb(element.dataset.color);
    if (rgb.length < 3) {
      alert('Invalid format!');
      return;
    }
    const color = new Color(rgb[0], rgb[1], rgb[2]);
    const solver = new Solver(color);
    const result = solver.solve();
    element.style = result.filter
  }

  renderTasksUrl(date){
    switch(this.ctx){
      case 'today':
        return "/prod/today/refresh?date=" + date
      case 'defaults':
        return "/prod/tasks/project/default"
    }

  }

  _refreshTasks(date=null){
    var tasks = document.getElementById('tasks')
    if (!tasks.getAttribute("fetch")){
      return null
    }
    fetch(this.renderTasksUrl(date))
      .then( response => response.text())
      .then( data => {
        tasks.innerHTML = data
      })
      .catch( () => {
        new Noty ({ text: "There was an error loading the tasks please refresh the page", type: "error" }).show()
      })
  }

  filterProjectTasks(event){
    var project = event.target.dataset.tasksName
    if(project == 'all'){
      this.filterableTargets.forEach(task => {
        task.classList.remove('hidden')
      })
      return
    }
    this.filterableTargets.forEach( task => {
      task.classList.remove('hidden')
      task.classList.add(project == task.dataset.tasksProject ? 'f' : "hidden")
    })
  }

  createProject() {
    var name =  document.getElementById("project_name").value
    var color = document.getElementById("project_color").value
    fetch(`/prod/project/create?name=${name}&color=${color}`,
          {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
      .then(response => response.json())
      .then((data) => {
        var projectModal = Modal.getInstance(document.getElementById('project_modal'))
        projectModal.hide()
        new Noty ({ text: data.success, type: "success" }).show()
      })
      .catch( () => {
        new Noty ({ text: "Project was not created please try again", type: "error" }).show()
      })
  }

  updateView(event) {
    const el = event.target.classList.contains('model-container') ? event.target : event.target.closest(".model-container")
    const model = el.dataset.model
    el.removeAttribute('data-action')
    fetch(`/prod/${model}/list`)
    .then( response => response.text())
    .then( data => {
      el.innerHTML = data
    })
  }


  taskFastUpdate(event) {
    const fieldContainer = event.target.closest(".field-container")
    const task = event.target.closest("li.tsk").dataset.task
    const fieldType = fieldContainer.dataset.field
    const fieldId = fieldContainer.value

    if (fieldType == "task" && event.keyCode != 13) return null

    const updateLink = `/prod/tasks/fu/${task}/${fieldType}/${fieldId}`
    fetch(updateLink,
      {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then( data => {
      setTimeout( ()  =>{
        new Noty ({ text: data.message, type: data.result ? "success":"danger" }).show()
      }, 250)
    })
    var date = null
    if(this.ctx == 'today'){
      const calendar = document.getElementById('datepicker')
      date = calendar.value
    }
    try{
      setTimeout( () => {
        new Date(date)
        this._refreshTasks(date)
      }, 150 )
    }
    finally{}
  }

  searchProject() {
    var regexp = /\B\#\w\w+\b/g
    var result = this.task.match(regexp);
    result = result == null ? [] : result
    if (result.length != []){
        var pro = result[0].split("#")[1]
        fetch("/prod/project/find?pro=" + pro)
             .then(response => response.json())
             .then(data => {
                 if(data != 'Not Found'){
                     this.projectNameTarget.textContent = data[0].fields.name
                     this.project = data[0].pk
                     this.task = this.task.replace(/\B\#\w\w+\b/g, "")
                 }
                 else{
                   document.getElementById('help').innerHTML = 'Project Not Found'
                 }
                })
    }
 }

createCategory() {
  var name =  document.getElementById("category_name").value
  var emoji = document.getElementById("category_emoji").value
  fetch(`/prod/category/create?name=${name}&emoji=${emoji}`,
        {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
    .then(response => response.json())
    .then(data => {
      var categoryModal = Modal.getInstance(document.getElementById('category_modal'))
      categoryModal.hide()
      new Noty ({ text: data.success, type: "success" }).show()
    })
    .catch( () => {
      new Noty ({ text: "Category was not created please try again", type: "error" }).show()
    })
}


 searchCategory(){
  var regexp = /\B\@\w\w+\b/g
  var result = this.task.match(regexp);
  result = result == null ? [] : result
  if (result.length != []){
      var cat = result[0].split("@")[1]
      fetch("/prod/category/find?cat=" + cat)
           .then(response => response.json())
           .then(data => {
               if(data != 'Not Found'){
                   this.emojiTarget.textContent = data[0].fields.emoji
                   this.category = data[0].pk
                   this.task = this.task.replace(/\B\@\w\w+\b/g, "")
               }
               else{
                 this.emojiTarget.innerHTML = '<i class="fa fa-question"></i>';
               }
              })
          .catch(error => {
            console.log(error)
          })
  }
 }

 createTask(event){
    if (event.keyCode != 13) return null
    if (this.category && this.project && this.task.length > 0){
        fetch(`/prod/tasks/create?name=${this.task}&cat_id=${this.category}&pro=${this.project}`,
              {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
          .then(response => response.text())
          .then(data =>{
            document.getElementById("tasks").innerHTML = data
          })
          .catch(function(error){
            console.log(error)
          })
    }
    else if (!this.category){
      return new Noty ({ text: "Please add a category", type: "error" }).show()
    }
    else if (this.task.length <= 0 ){
      return new Noty ({ text: "Please add a task description", type: "error" }).show()
    }
    else if (!this.project){
      return new Noty ({ text: "Please add a project", type: "error" }).show()
    }
 }

 deleteTask(event) {
   const initalEl = event.target
   const el = initalEl.nodeName == 'A' ? initalEl : initalEl.closest('a')
   const taskId = el.dataset.taskid
   fetch(`/prod/tasks/delete?task=${taskId}`, {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
   .then(response => response.data)
   .then(data => {
     this._refreshTasks()
     return new Noty ({text: data.message, type: "success"})
   })
   .catch( (error) => console.log(error))
 }

 get task(){
  return this.taskTarget.value
 }

 get category(){
   return this.categoryTarget.value
 }

 get project(){
   return this.projectTarget.value
 }

get projectModal(){
  return new Modal(document.getElementById('project_modal'))
}

get categoryModal(){
  return new Modal(document.getElementById('category_modal'))
}

get ctx(){
  return document.getElementById('tasks').getAttribute("fetch")
}

get date(){
  const params = new URLSearchParams(location.search)
  return params.has("date") ? params.get("date") : null
}

 set task(val){
   this.taskTarget.value = val
 }

 set project(val){
   this.projectTarget.value = val
 }

 set category(val){
   this.categoryTarget.value = val
 }

 set date(val){
  const params = new URLSearchParams(location.search)
  params.set("date", val)
  history.pushState(null, null, "?"+params.toString())
 }
}