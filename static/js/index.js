import { Application } from 'stimulus';
import { definitionsFromContext } from 'stimulus/webpack-helpers';
import Turbolinks from 'turbolinks';
import '../js/others/hue'
import '@popperjs/core'
import 'moment'
import '../../assets/sass/style.scss'
import 'flatpickr/dist/flatpickr.css'
import '@primer/octicons/build/build.css'

const application = Application.start();
const context = require.context('./controllers', true, /\.js$/);
application.load(definitionsFromContext(context));
Turbolinks.start();